# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2025)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import asyncio
import contextlib
import errno
import socket
import sys
from typing import TYPE_CHECKING, Any, Final, cast

import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response
from starlette.routing import Mount, Route, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from streamlit import cli_util, config, file_util, util
from streamlit.config_option import ConfigOption
from streamlit.logger import get_logger
from streamlit.runtime import Runtime, RuntimeConfig, RuntimeState
from streamlit.runtime.memory_media_file_storage import MemoryMediaFileStorage
from streamlit.runtime.memory_uploaded_file_manager import MemoryUploadedFileManager
from streamlit.runtime.uploaded_file_manager import UploadedFileRec
from streamlit.web.cache_storage_manager_config import (
    create_default_cache_storage_manager,
)
from streamlit.web.server.asgi_browser_websocket_handler import (
    ASGIBrowserWebSocketHandler,
)
from streamlit.web.server.asgi_routes import (
    ASGIHealthHandler,
    ASGIHostConfigHandler,
    MediaFileHandler,
)
from streamlit.web.server.server_util import DEVELOPMENT_PORT

if TYPE_CHECKING:
    from collections.abc import Awaitable

    from starlette.requests import Request

_LOGGER: Final = get_logger(__name__)

# When server.port is not available it will look for the next available port
# up to MAX_PORT_SEARCH_RETRIES.
MAX_PORT_SEARCH_RETRIES: Final = 100

# When server.address starts with this prefix, the server will bind
# to an unix socket.
UNIX_SOCKET_PREFIX: Final = "unix://"

MEDIA_ENDPOINT: Final = "/media"
UPLOAD_FILE_ENDPOINT: Final = "/_stcore/upload_file"
ACTUAL_UPLOAD_FILE_ENDPOINT = "/_stcore/upload_file/{session_id:str}/{file_id:str}"
STARLETTE_STREAM_ENDPOINT: Final = "/_stcore/stream"
METRIC_ENDPOINT: Final = r"(?:st-metrics|_stcore/metrics)"
MESSAGE_ENDPOINT: Final = r"_stcore/message"
HEALTH_ENDPOINT: Final = r"(?:healthz|_stcore/health)"
HOST_CONFIG_ENDPOINT: Final = r"_stcore/host-config"
NEW_HEALTH_ENDPOINT: Final = "_stcore/health"
SCRIPT_HEALTH_CHECK_ENDPOINT: Final = (
    r"(?:script-health-check|_stcore/script-health-check)"
)


class RetriesExceeded(Exception):
    pass


def server_port_is_manually_set() -> bool:
    return config.is_manually_set("server.port")


def server_address_is_unix_socket() -> bool:
    address = config.get_option("server.address")
    return address is not None and address.startswith(UNIX_SOCKET_PREFIX)


def get_available_port() -> int:
    """Returns the first available port starting from the configured port."""
    call_count = 0

    port = None
    while call_count < MAX_PORT_SEARCH_RETRIES:
        address = config.get_option("server.address") or "localhost"
        port = config.get_option("server.port")

        if int(port) == DEVELOPMENT_PORT:
            _LOGGER.warning(
                "Port %s is reserved for internal development. "
                "It is strongly recommended to select an alternative port "
                "for `server.port`.",
                DEVELOPMENT_PORT,
            )

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex((address, port)) == 0:
                    raise OSError(errno.EADDRINUSE, "Address already in use")
                else:
                    break  # It worked! So let's break out of the loop.

        except OSError as e:
            if e.errno == errno.EADDRINUSE:
                if server_port_is_manually_set():
                    _LOGGER.error("Port %s is already in use", port)
                    sys.exit(1)
                else:
                    _LOGGER.debug(
                        "Port %s already in use, trying to use the next one.", port
                    )
                    port += 1
                    # Don't use the development port here:
                    if port == DEVELOPMENT_PORT:
                        port += 1

                    config.set_option(
                        "server.port", port, ConfigOption.STREAMLIT_DEFINITION
                    )
                    call_count += 1
            else:
                raise

    if call_count >= MAX_PORT_SEARCH_RETRIES:
        raise RetriesExceeded(
            f"Cannot start Streamlit server. Port {port} is already in use, and "
            f"Streamlit was unable to find a free port after {MAX_PORT_SEARCH_RETRIES} attempts.",
        )
    return cast("int", port)


def create_uvicorn_config(app: Starlette) -> uvicorn.Config:
    # TODO: [Kajarenc] instead of searching for available port and then ask uvicorn to run
    # on that port, we can bind uvicorn an existing socket we found in get_available_port.
    return uvicorn.Config(
        app=app,
        host=config.get_option("server.address"),
        port=get_available_port(),
        # log_level=config.get_option("global.logLevel"),
        # loop="asyncio",
        # log_config=None,
        # access_log=False,
        use_colors=True,
        # NOTE:[kajarenc] Settings log_level to "critical" is a temporary fix to avoid
        # uvicorn logging cancelled error in console in development mode,
        # when ^C pressed.
        log_level="info",
    )


def create_uvicorn_server(app: Starlette) -> uvicorn.Server:
    return uvicorn.Server(
        config=create_uvicorn_config(app),
    )


def main_mount_streamlit_app(
    parent_app: Starlette, script_path: str, url_to_mount
) -> None:
    old_lifespan = parent_app.router.lifespan_context
    my_server = Server(script_path, False)

    @contextlib.asynccontextmanager
    async def create_lifespan(app: Starlette):
        await my_server._runtime.start()

        async with old_lifespan(app) as cm1, my_server.create_lifespan(app) as cm2:
            yield {**(cm1 or {}), **cm2}

        my_server._runtime.stop()

    parent_app.router.lifespan_context = create_lifespan

    streamlit_app = my_server.create_exported_app()

    parent_app.mount(url_to_mount, streamlit_app)


class Server:
    def __init__(self, main_script_path: str, is_hello: bool):
        """Create the server. It won't be started yet."""

        self._main_script_path = main_script_path

        # Initialize MediaFileStorage and its associated endpoint
        media_file_storage = MemoryMediaFileStorage(MEDIA_ENDPOINT)

        self._media_file_storage = media_file_storage
        # MediaFileHandler.initialize_storage(media_file_storage)

        uploaded_file_mgr = MemoryUploadedFileManager(UPLOAD_FILE_ENDPOINT)

        self._runtime = Runtime(
            RuntimeConfig(
                script_path=main_script_path,
                command_line=None,
                media_file_storage=media_file_storage,
                uploaded_file_manager=uploaded_file_mgr,
                cache_storage_manager=create_default_cache_storage_manager(),
                is_hello=is_hello,
            ),
        )

        self._runtime.stats_mgr.register_provider(media_file_storage)

    def __repr__(self) -> str:
        return util.repr_(self)

    @property
    def main_script_path(self) -> str:
        return self._main_script_path

    async def start(self) -> None:
        """Start the server.

        When this returns, Streamlit is ready to accept new sessions.
        """

        _LOGGER.debug("Starting server...")

        # TODO: [Kajarenc], DONE!
        # Idea: Prepare uvicorn config, create uvicorn server, start
        # uvicorn server.serve as a event loop task and remember this task.
        # At this point we can return we can return from this coroutine.

        app: Starlette = self._create_app()
        uvicorn_server = create_uvicorn_server(app)

        self.server_task = asyncio.create_task(
            uvicorn_server.serve(), name="UvicornSERVER" * 10
        )

        port = config.get_option("server.port")
        _LOGGER.debug("Server started on port %s", port)

        await self._runtime.start()

    @property
    def stopped(self) -> Awaitable[None]:
        """A Future that completes when the Server's run loop has exited."""
        return self._runtime.stopped

    @contextlib.asynccontextmanager
    async def create_lifespan(self, app: Starlette):
        await self._runtime.wait_started()
        yield {
            "runtime": self._runtime,
            "media_file_storage": self._media_file_storage,
        }

    async def upload_file_endpoint(self, request: Request):
        """
        Handles file upload for Streamlit using Starlette.
        Expects a multipart/form-data or octet-stream request containing the file, plus `session_id` and `file_id` as form fields.
        Supports PUT (upload) and OPTIONS (CORS preflight).
        """

        if request.method == "OPTIONS":
            # CORS preflight response: 204 No Content with headers
            headers = {
                "Access-Control-Allow-Methods": "PUT, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Origin": "*",
            }
            return Response(status_code=204, headers=headers)

        if request.method == "DELETE":
            """Delete file request handler."""
            session_id = request.path_params["session_id"]
            file_id = request.path_params["file_id"]

            request.state.runtime.uploaded_file_mgr.remove_file(
                session_id=session_id, file_id=file_id
            )
            return Response(status_code=204)

        if request.method != "PUT":
            return JSONResponse(
                {"error": "Only PUT and OPTIONS are allowed"}, status_code=405
            )

        form = await request.form()

        file_upload = None
        for _, value in form.multi_items():
            if hasattr(value, "read"):
                file_upload = value
                break

        if not file_upload:
            return JSONResponse(
                {"error": "No file part in the request"},
                status_code=HTTP_400_BAD_REQUEST,
            )

        session_id = request.path_params["session_id"]
        file_id = request.path_params["file_id"]

        if not session_id or not file_id:
            return JSONResponse(
                {"error": "sessionId and fileId must be provided"},
                status_code=HTTP_400_BAD_REQUEST,
            )

        contents = await file_upload.read()

        file_mgr: MemoryUploadedFileManager = request.state.runtime.uploaded_file_mgr

        uploaded_file_rec = UploadedFileRec(
            file_id=file_id,
            name=file_upload.filename,  # type: ignore[union-attr, arg-type]
            type=file_upload.content_type,  # type: ignore[union-attr, arg-type]
            data=contents,
        )

        file_mgr.add_file(session_id=session_id, file=uploaded_file_rec)

        return JSONResponse({"status": "ok"}, status_code=HTTP_201_CREATED)

    def _create_routes(self) -> list[Route]:
        starlette_routes: list[Any] = [
            WebSocketRoute("/_stcore/stream", endpoint=ASGIBrowserWebSocketHandler),
            Route("/healthz", ASGIHealthHandler),
            Route("/_stcore/health", ASGIHealthHandler),
            Route("/_stcore/host-config", ASGIHostConfigHandler),
            # Add the media file route with a path parameter
            Route(MEDIA_ENDPOINT + "/{path:path}", endpoint=MediaFileHandler),
            Route(
                ACTUAL_UPLOAD_FILE_ENDPOINT,
                endpoint=self.upload_file_endpoint,
                methods=["PUT", "OPTIONS"],
            ),
        ]

        # if config.get_option("global.developmentMode"):
        #     _LOGGER.debug("Serving static content from the Node dev server")
        # else:
        starlette_routes.append(
            Mount(
                "/",
                app=StaticFiles(
                    directory=file_util.get_static_dir(),
                    html=True,
                ),
            ),
        )

        return starlette_routes

    def _create_app(self) -> Starlette:
        """Create our Starlette web app."""
        config.get_option("server.baseUrlPath")

        starlette_routes = self._create_routes()

        return Starlette(
            debug=True,
            routes=starlette_routes,
            lifespan=self.create_lifespan,
            middleware=[Middleware(CORSMiddleware, allow_origins=["*"])],
            # cookie_secret=config.get_option("server.cookieSecret"),
            # xsrf_cookies=config.get_option("server.enableXsrfProtection"),
            # # Set the websocket message size. The default value is too low.
            # websocket_max_message_size=get_max_message_size_bytes(),
            # **TORNADO_SETTINGS,  # type: ignore[arg-type]
        )

    def create_exported_app(self) -> Starlette:
        """Create the exported app."""

        starlette_routes = self._create_routes()

        return Starlette(
            debug=True,
            routes=starlette_routes,
            middleware=[Middleware(CORSMiddleware, allow_origins=["*"])],
            # cookie_secret=config.get_option("server.cookieSecret"),
            # xsrf_cookies=config.get_option("server.enableXsrfProtection"),
            # # Set the websocket message size. The default value is too low.
            # websocket_max_message_size=get_max_message_size_bytes(),
            # **TORNADO_SETTINGS,  # type: ignore[arg-type]
        )

    @property
    def browser_is_connected(self) -> bool:
        return self._runtime.state == RuntimeState.ONE_OR_MORE_SESSIONS_CONNECTED

    @property
    def is_running_hello(self) -> bool:
        from streamlit.hello import streamlit_app

        return self._main_script_path == streamlit_app.__file__

    def stop(self) -> None:
        # TODO: [Kajarenc], continuetion of IDEA, implemented
        # stop uvicorn server task here.
        cli_util.print_to_cli("  Stopping...", fg="blue")
        self.server_task.cancel()
        self._runtime.stop()
