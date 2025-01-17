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

from typing import (
    TYPE_CHECKING,
    Final,
    Iterator,
    Mapping,
    NoReturn,
    Union,
)

from streamlit import config, runtime
from streamlit.auth_util import (
    encode_provider_token,
    get_secrets_auth_section,
    is_authlib_installed,
    validate_auth_credentials,
)
from streamlit.errors import StreamlitAPIException, StreamlitAuthError
from streamlit.proto.ForwardMsg_pb2 import ForwardMsg
from streamlit.runtime.metrics_util import gather_metrics
from streamlit.runtime.scriptrunner_utils.script_run_context import (
    get_script_run_ctx as _get_script_run_ctx,
)
from streamlit.url_util import make_url_path

if TYPE_CHECKING:
    from streamlit.runtime.scriptrunner_utils.script_run_context import UserInfo


AUTH_LOGIN_ENDPOINT: Final = "/auth/login"
AUTH_LOGOUT_ENDPOINT: Final = "/auth/logout"


@gather_metrics("login")
def login(provider: str | None = None) -> None:
    """Initiate the login flow for the given provider.

    This command redirects the user to an OpenID Connect (OIDC) provider. After
    the user authenticates their identity, they are redirected back to the
    home page of your app. This creates a new session where the user's identity
    is available through |st.experimental_user|_. Call ``st.logout()`` to
    remove the user's information from ``st.experimental_user`` and start a new
    session.

    You can use any OpenID Connect (OIDC) provider, including GitHub, Google,
    Microsoft, Okta, and more. You must configure the provider through secrets
    management. Although OIDC is an extension of OAuth 2.0, you can't use
    generic OAuth providers. Furthermore, you can only access the user's
    identity information and not their underlying OAuth token. Therefore, this
    command will not allow your app to act on behalf of a user in a secure
    system.

    For all providers, there are two common settings, ``auth.redirect_uri`` and
    ``auth.cookie_secret``, which you must specify in the ``[auth]`` dictionary
    in ``secrets.toml``. Other settings must be defined as described in the
    ``provider`` parameter.

    - ``auth.redirect_uri`` is your app's URL with the pathname
      ``/oauth2callback``.
    - ``auth.cookie_secret`` should be a strong, randomly generated secret.

    .. Important::
        - You must install ``Authlib>=1.3.2`` to use this command.
        - Your authentication configuration is dependent on your host location.
          When you deploy your app, remember to update your ``redirect_uri``
          both within your app and within your provider.
        - Streamlit will automatically enable CORS and XSRF protection when you
          use ``st.login()``, overriding configuration options in
          ``config.toml``.
        - For security reasons, authentication is not supported for embedded
          apps.

    .. |st.experimental_user| replace:: ``st.experimental_user``
    .. _st.experimental_user: https://docs.streamlit.io/develop/api-reference/utilities/st.experimental_user

    Parameters
    ----------
    provider: str or None
        The name of your provider configuration to use for login.

        If ``provider`` is ``None`` (default), Streamlit will use all settings
        in the ``[auth]`` dictionary within your app's ``secrets.toml`` file.
        Otherwise, use an ``[auth.<provider>]`` dictionary for the named
        provider, as shown in the examples that follow. When you pass a string
        to ``provider``, Streamlit will use ``auth.redirect_uri`` and
        ``auth.cookie_secret``, while ignoring any other values in the
        ``[auth]`` dictionary.

    Examples
    --------

    **Example 1: Use a single, default identity provider**

    If you do not specify a name for your provider, specify all settings within
    the ``[auth]`` dictionary of your ``secrets.toml`` file. The following
    example configures Google as the default provider. For information about
    using OIDC with Google, see `Google Identity
    <https://developers.google.com/identity/openid-connect/openid-connect>`_.

    ``.streamlit/secrets.toml``:

    >>> [auth]
    >>> redirect_uri = "http://localhost:8501/oauth2callback"
    >>> cookie_secret = "xxx"
    >>> client_id = "xxx"
    >>> client_secret = "xxx"
    >>> server_metadata_url = (
    ...     "https://accounts.google.com/.well-known/openid-configuration"
    ... )

    Your app code:

    >>> import streamlit as st
    >>> if not st.experimental_user.is_logged_in:
    >>>     if st.button("Log in"):
    >>>         st.login()
    >>> else:
    >>>     if st.button("Log out"):
    >>>         st.logout()
    >>>     st.write(f"Hello, {st.experimental_user.name}!")

    **Example 2: Use a named identity provider**

    If you specify a name for your provider, save the common settings in the
    ``[auth]`` dictionary of your ``secrets.toml`` file, and save the other
    settings in an ``[auth.<provider>]`` dictionary, where ``<provider>`` is
    the name of your provider. The following example configures Microsoft as
    the provider. The example uses ``provider="microsoft"``, but you can use
    any name. This name is internal to Streamlit and used to match the login
    command to its configuration. For information about using OIDC with
    Microsoft, `Microsoft Entra ID
    <https://learn.microsoft.com/en-us/power-pages/security/authentication/openid-settings>`_.
    To configure your ``{tenant}`` value in ``server_metadata_url``, see
    `Microsoft identity platform
    <https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc#find-your-apps-openid-configuration-document-uri>`_.

    ``.streamlit/secrets.toml``:

    >>> [auth]
    >>> redirect_uri = "http://localhost:8501/oauth2callback"
    >>> cookie_secret = "xxx"
    >>>
    >>> [auth.microsoft]
    >>> client_id = "xxx"
    >>> client_secret = "xxx"
    >>> server_metadata_url = "https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration"

    Your app code:

    >>> import streamlit as st
    >>> if not st.experimental_user.is_logged_in:
    >>>     st.login("microsoft")
    >>> else:
    >>>     st.write(f"Hello, {st.experimental_user.name}!")

    **Example 3: Use multiple, named providers**

    If you want to give your users a choice of authentication methods,
    configure multiple providers and give them each a unique name. The
    following example offers users the opportunity to log in through Okta or
    Auth0.

    >>> [auth]
    >>> redirect_uri = "http://localhost:8501/oauth2callback"
    >>> cookie_secret = "xxx"
    >>>
    >>> [auth.okta]
    >>> client_id = "xxx"
    >>> client_secret = "xxx"
    >>> server_metadata_url = "https://{subdomain}.okta.com/oauth2/default/.well-known/openid-configuration"
    >>>
    >>> [auth.auth0]
    >>> client_id = "xxx"
    >>> client_secret = "xxx"
    >>> server_metadata_url = (
    ...     "{account}.{region}.auth0.com/.well-known/openid-configuration"
    ... )

    Your app code:

    >>> import streamlit as st
    >>> if st.button("Internal login"):
    >>>     st.login("okta")
    >>> if st.button("External login"):
    >>>     st.login("auth0")
    >>> if st.experimental_user.is_logged_in:
    >>>     st.write(f"Hello, {st.experimental_user.name}!)

    **Examplt 4: Change the default connection settings**

    By default, Streamlit sets ``scope="openid profile email"`` and
    ``prompt="select_account"``. You can change these and other OIDC parameters
    by defining ``client_kwargs``. For more information about OIDC parameters,
    see `OpenID Connect Core
    <https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest>`_ and
    your provider's documentation.

    ``.streamlit/secrets.toml``:

    >>> [auth]
    >>> redirect_uri = "http://localhost:8501/oauth2callback"
    >>> cookie_secret = "xxx"
    >>>
    >>> [auth.google]
    >>> client_id = "xxx"
    >>> client_secret = "xxx"
    >>> server_metadata_url = (
    ...     "https://accounts.google.com/.well-known/openid-configuration"
    ... )
    >>> client_kwargs = {
            "prompt" = "select_account consent",
            "scope" = "openid profile"
        }

    Your app code:

    >>> import streamlit as st
    >>> if not st.experimental_user.is_logged_in:
    >>>     st.login("google")
    >>> else:
    >>>     st.write(f"Hello, {st.experimental_user.name}!")

    """
    if provider is None:
        provider = "default"

    context = _get_script_run_ctx()
    if context is not None:
        if not is_authlib_installed():
            raise StreamlitAuthError(
                """To use authentication features, you need to install """
                """Authlib>=1.3.2, e.g. via `pip install Authlib`."""
            )
        validate_auth_credentials(provider)
        fwd_msg = ForwardMsg()
        fwd_msg.auth_redirect.url = generate_login_redirect_url(provider)
        context.enqueue(fwd_msg)


@gather_metrics("logout")
def logout() -> None:
    """Logout the current user."""
    context = _get_script_run_ctx()
    if context is not None:
        context.user_info.clear()
        session_id = context.session_id

        if runtime.exists():
            instance = runtime.get_instance()
            instance.clear_user_info_for_session(session_id)

        base_path = config.get_option("server.baseUrlPath")

        fwd_msg = ForwardMsg()
        fwd_msg.auth_redirect.url = make_url_path(base_path, AUTH_LOGOUT_ENDPOINT)
        context.enqueue(fwd_msg)


def generate_login_redirect_url(provider: str) -> str:
    """Generate the login redirect URL for the given provider."""
    provider_token = encode_provider_token(provider)
    base_path = config.get_option("server.baseUrlPath")
    login_path = make_url_path(base_path, AUTH_LOGIN_ENDPOINT)
    return f"{login_path}?provider={provider_token}"


def _get_user_info() -> UserInfo:
    ctx = _get_script_run_ctx()
    if ctx is None:
        # TODO: Add appropriate warnings when ctx is missing
        return {}
    context_user_info = ctx.user_info.copy()

    auth_section_exists = get_secrets_auth_section()
    if "is_logged_in" not in context_user_info and auth_section_exists:
        context_user_info["is_logged_in"] = False
    return context_user_info


class UserInfoProxy(Mapping[str, Union[str, bool, None]]):
    """
    A read-only, dict-like object for accessing information about current user.

    ``st.experimental_user`` is dependent on the host platform running the
    Streamlit app. If the host platform has not configured the function, it
    will behave as it does in a locally running app.

    Properties can be accessed via key or attribute notation. For example,
    ``st.experimental_user["email"]`` or ``st.experimental_user.email``.

    """

    def __getitem__(self, key: str) -> str | bool | None:
        try:
            return _get_user_info()[key]
        except KeyError:
            raise KeyError(f'st.experimental_user has no key "{key}".')

    def __getattr__(self, key: str) -> str | bool | None:
        try:
            return _get_user_info()[key]
        except KeyError:
            raise AttributeError(f'st.experimental_user has no attribute "{key}".')

    def __setattr__(self, name: str, value: str | None) -> NoReturn:
        raise StreamlitAPIException("st.experimental_user cannot be modified")

    def __setitem__(self, name: str, value: str | None) -> NoReturn:
        raise StreamlitAPIException("st.experimental_user cannot be modified")

    def __iter__(self) -> Iterator[str]:
        return iter(_get_user_info())

    def __len__(self) -> int:
        return len(_get_user_info())

    def to_dict(self) -> UserInfo:
        """
        Get user info as a dictionary.

        This method primarily exists for internal use and is not needed for
        most cases. ``st.experimental_user`` returns an object that inherits from
        ``dict`` by default.

        Returns
        -------
        Dict[str,str]
            A dictionary of the current user's information.
        """
        return _get_user_info()
