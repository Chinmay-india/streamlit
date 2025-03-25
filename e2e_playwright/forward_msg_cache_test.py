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

from typing import TYPE_CHECKING, Final

import pytest
from playwright.sync_api import expect

from e2e_playwright.conftest import rerun_app, wait_for_app_loaded
from e2e_playwright.shared.app_utils import (
    click_button,
    click_toggle,
    fill_number_input,
)

if TYPE_CHECKING:
    from playwright.sync_api import Page


def test_forward_msg_cache_receives_msg(app: Page):
    app.evaluate("window.streamlitDebug.clearForwardMsgCache()")
    rerun_app(app)
    expect(app.get_by_role("dialog")).not_to_be_visible()

    app.expect_request("**/_stcore/message/")


def _rerun_app(app: Page, times: int):
    for _ in range(times):
        click_button(app, "Re-run")


@pytest.mark.performance
@pytest.mark.repeat(2)  # only repeat 2 times since otherwise it would take too long
def test_simulate_large_data_usage_performance(app: Page):
    # Rerun app a couple of times:
    _rerun_app(app, 5)

    # Show dataframe:
    click_toggle(app, "Show dataframes")
    # Rerun app a couple of times:
    _rerun_app(app, 5)

    # # Set 50k rows:
    fill_number_input(app, "Number of rows", 50000)

    # Rerun app a couple of times:
    _rerun_app(app, 5)

    # Show more text messages:
    fill_number_input(app, "Number of small messages", 100)

    # Rerun app a couple of times:
    _rerun_app(app, 10)


@pytest.mark.performance
@pytest.mark.repeat(2)  # only repeat 2 times since otherwise it would take too long
def test_simulate_many_small_messages_performance(app: Page):
    # Show 150 unique texts with 50kb each:
    fill_number_input(app, "Number of small messages", 150)
    _rerun_app(app, 5)

    # Reduce the size of every message to 15KB:
    fill_number_input(app, "Message KB size", 15)
    _rerun_app(app, 10)


def test_check_websocket_message_size(page: Page, app_port: int):
    TOTAL_WEBSOCKET_SENT_SIZE_THRESHOLD_MB: Final = 0.1
    TOTAL_WEBSOCKET_RECEIVED_SIZE_THRESHOLD_MB: Final = 55

    total_received_size_bytes = 0
    total_sent_size_bytes = 0

    def on_web_socket(ws):
        print(f"WebSocket opened: {ws.url}")

        def on_frame_sent(payload: str | bytes):
            nonlocal total_sent_size_bytes
            if isinstance(payload, str):
                payload = payload.encode("utf-8")
            total_sent_size_bytes += len(payload)

        def on_frame_received(payload: str | bytes):
            nonlocal total_received_size_bytes
            if isinstance(payload, str):
                payload = payload.encode("utf-8")
            total_received_size_bytes += len(payload)

        ws.on("framesent", on_frame_sent)
        ws.on("framereceived", on_frame_received)
        ws.on("close", lambda _: print("WebSocket closed"))

    # Register websocket handler
    page.on("websocket", on_web_socket)

    page.goto(f"http://localhost:{app_port}/")
    wait_for_app_loaded(page)
    # Wait until all dependent resources are loaded:
    page.wait_for_load_state()

    # Rerun app a couple of times:
    _rerun_app(page, 5)

    # Show dataframe:
    click_toggle(page, "Show dataframes")
    # Rerun app a couple of times:
    _rerun_app(page, 5)

    # # Set 50k rows:
    fill_number_input(page, "Number of rows", 50000)

    # Rerun fragment a couple of times:
    click_button(page, "Rerun fragment")
    click_button(page, "Rerun fragment")
    click_button(page, "Rerun fragment")
    click_button(page, "Rerun fragment")
    click_button(page, "Rerun fragment")
    # -> Running fragments should not clear cached messages of non-fragments

    # Rerun app a couple of times:
    _rerun_app(page, 5)

    # Show more text messages:
    fill_number_input(page, "Number of small messages", 100)

    # Rerun app a couple of times:
    _rerun_app(page, 10)

    # Assert that the total size of websocket messages is under the threshold:
    assert (
        total_received_size_bytes
        < TOTAL_WEBSOCKET_RECEIVED_SIZE_THRESHOLD_MB * 1024 * 1024
    ), (
        f"Total received size of websocket messages "
        f"({total_received_size_bytes / 1024 / 1024:.2f}MB) "
        "exceeds the configured threshold "
        f"({TOTAL_WEBSOCKET_RECEIVED_SIZE_THRESHOLD_MB}MB)"
        "In case this is expected and justified, you can change the "
        "threshold in the test."
    )
    assert (
        total_sent_size_bytes < TOTAL_WEBSOCKET_SENT_SIZE_THRESHOLD_MB * 1024 * 1024
    ), (
        "Total sent size of websocket messages "
        f"({total_sent_size_bytes / 1024 / 1024:.2f}MB) "
        "exceeds the configured threshold "
        f"({TOTAL_WEBSOCKET_SENT_SIZE_THRESHOLD_MB}MB)"
        "In case this is expected and justified, you can change the "
        "threshold in the test."
    )
