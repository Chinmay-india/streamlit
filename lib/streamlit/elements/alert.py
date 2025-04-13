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

from typing import TYPE_CHECKING, Literal, Union, cast

from typing_extensions import TypeAlias

from streamlit.errors import StreamlitAPIException
from streamlit.proto.Alert_pb2 import Alert as AlertProto
from streamlit.runtime.metrics_util import gather_metrics
from streamlit.string_util import clean_text, validate_icon_or_emoji

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator
    from streamlit.type_util import SupportsStr

Width: TypeAlias = Union[int, Literal["stretch"]]


class AlertMixin:
    @gather_metrics("error")
    def error(
        self,
        body: SupportsStr,
        *,  # keyword-only args:
        icon: str | None = None,
        width: Width = "stretch",
        scale: float | int = 1,
    ) -> DeltaGenerator:
        """Display error message.

        Parameters
        ----------
        body : str
            The text to display as GitHub-flavored Markdown. Syntax
            information can be found at: https://github.github.com/gfm.

            See the ``body`` parameter of |st.markdown|_ for additional,
            supported Markdown directives.

            .. |st.markdown| replace:: ``st.markdown``
            .. _st.markdown: https://docs.streamlit.io/develop/api-reference/text/st.markdown
        icon : str, None
            An optional emoji or icon to display next to the alert. If ``icon``
            is ``None`` (default), no icon is displayed. If ``icon`` is a
            string, the following options are valid:

            - A single-character emoji. For example, you can set ``icon="🚨"``
              or ``icon="🔥"``. Emoji short codes are not supported.

            - An icon from the Material Symbols library (rounded style) in the
              format ``":material/icon_name:"`` where "icon_name" is the name
              of the icon in snake case.

              For example, ``icon=":material/thumb_up:"`` will display the
              Thumb Up icon. Find additional icons in the `Material Symbols \
              <https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded>`_
              font library.

        width : "stretch" or int
            The width of the alert. If "stretch" (default), the alert will expand
            to fill the available width in its container. If an int, the alert will
            have the given width in pixels.

        scale : float or int
            A scale factor to multiply the width by. This parameter only has an
            effect when width="stretch" and the parent container is a horizontal
            container. Default is 1.0.

        Example
        -------
        >>> import streamlit as st
        >>>
        >>> st.error('This is an error', icon="🚨")

        """
        alert_proto = AlertProto()

        alert_proto.icon = validate_icon_or_emoji(icon)
        alert_proto.body = clean_text(body)
        alert_proto.format = AlertProto.ERROR

        # Handle width parameter
        alert_proto.width = str(width)

        # Handle scale parameter
        if isinstance(scale, (int, float)) and scale > 0:
            alert_proto.scale = float(scale)
        else:
            raise StreamlitAPIException(
                f"'{str(scale)}' is not an accepted value. scale must be a positive number."
            )

        return self.dg._enqueue("alert", alert_proto)

    @gather_metrics("warning")
    def warning(
        self,
        body: SupportsStr,
        *,  # keyword-only args:
        icon: str | None = None,
        width: Width = "stretch",
        scale: float | int = 1,
    ) -> DeltaGenerator:
        """Display warning message.

        Parameters
        ----------
        body : str
            The text to display as GitHub-flavored Markdown. Syntax
            information can be found at: https://github.github.com/gfm.

            See the ``body`` parameter of |st.markdown|_ for additional,
            supported Markdown directives.

            .. |st.markdown| replace:: ``st.markdown``
            .. _st.markdown: https://docs.streamlit.io/develop/api-reference/text/st.markdown
        icon : str, None
            An optional emoji or icon to display next to the alert. If ``icon``
            is ``None`` (default), no icon is displayed. If ``icon`` is a
            string, the following options are valid:

            - A single-character emoji. For example, you can set ``icon="🚨"``
              or ``icon="🔥"``. Emoji short codes are not supported.

            - An icon from the Material Symbols library (rounded style) in the
              format ``":material/icon_name:"`` where "icon_name" is the name
              of the icon in snake case.

              For example, ``icon=":material/thumb_up:"`` will display the
              Thumb Up icon. Find additional icons in the `Material Symbols \
              <https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded>`_
              font library.

        width : "stretch" or int
            The width of the alert. If "stretch" (default), the alert will expand
            to fill the available width in its container. If an int, the alert will
            have the given width in pixels.

        scale : float or int
            A scale factor to multiply the width by. This parameter only has an
            effect when width="stretch" and the parent container is a horizontal
            container. Default is 1.0.

        Example
        -------
        >>> import streamlit as st
        >>>
        >>> st.warning('This is a warning', icon="⚠️")

        """
        alert_proto = AlertProto()
        alert_proto.body = clean_text(body)
        alert_proto.icon = validate_icon_or_emoji(icon)
        alert_proto.format = AlertProto.WARNING

        # Handle width parameter
        alert_proto.width = str(width)

        # Handle scale parameter
        if isinstance(scale, (int, float)) and scale > 0:
            alert_proto.scale = float(scale)
        else:
            raise StreamlitAPIException(
                f"'{str(scale)}' is not an accepted value. scale must be a positive number."
            )

        return self.dg._enqueue("alert", alert_proto)

    @gather_metrics("info")
    def info(
        self,
        body: SupportsStr,
        *,  # keyword-only args:
        icon: str | None = None,
        width: Width = "stretch",
        scale: float | int = 1,
    ) -> DeltaGenerator:
        """Display an informational message.

        Parameters
        ----------
        body : str
            The text to display as GitHub-flavored Markdown. Syntax
            information can be found at: https://github.github.com/gfm.

            See the ``body`` parameter of |st.markdown|_ for additional,
            supported Markdown directives.

            .. |st.markdown| replace:: ``st.markdown``
            .. _st.markdown: https://docs.streamlit.io/develop/api-reference/text/st.markdown
        icon : str, None
            An optional emoji or icon to display next to the alert. If ``icon``
            is ``None`` (default), no icon is displayed. If ``icon`` is a
            string, the following options are valid:

            - A single-character emoji. For example, you can set ``icon="🚨"``
              or ``icon="🔥"``. Emoji short codes are not supported.

            - An icon from the Material Symbols library (rounded style) in the
              format ``":material/icon_name:"`` where "icon_name" is the name
              of the icon in snake case.

              For example, ``icon=":material/thumb_up:"`` will display the
              Thumb Up icon. Find additional icons in the `Material Symbols \
              <https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded>`_
              font library.

        width : "stretch" or int
            The width of the alert. If "stretch" (default), the alert will expand
            to fill the available width in its container. If an int, the alert will
            have the given width in pixels.

        scale : float or int
            A scale factor to multiply the width by. This parameter only has an
            effect when width="stretch" and the parent container is a horizontal
            container. Default is 1.0.

        Example
        -------
        >>> import streamlit as st
        >>>
        >>> st.info('This is a purely informational message', icon="ℹ️")

        """

        alert_proto = AlertProto()
        alert_proto.body = clean_text(body)
        alert_proto.icon = validate_icon_or_emoji(icon)
        alert_proto.format = AlertProto.INFO

        # Handle width parameter
        alert_proto.width = str(width)

        # Handle scale parameter
        if isinstance(scale, (int, float)) and scale > 0:
            alert_proto.scale = float(scale)
        else:
            raise StreamlitAPIException(
                f"'{str(scale)}' is not an accepted value. scale must be a positive number."
            )

        return self.dg._enqueue("alert", alert_proto)

    @gather_metrics("success")
    def success(
        self,
        body: SupportsStr,
        *,  # keyword-only args:
        icon: str | None = None,
        width: Width = "stretch",
        scale: float | int = 1,
    ) -> DeltaGenerator:
        """Display a success message.

        Parameters
        ----------
        body : str
            The text to display as GitHub-flavored Markdown. Syntax
            information can be found at: https://github.github.com/gfm.

            See the ``body`` parameter of |st.markdown|_ for additional,
            supported Markdown directives.

            .. |st.markdown| replace:: ``st.markdown``
            .. _st.markdown: https://docs.streamlit.io/develop/api-reference/text/st.markdown
        icon : str, None
            An optional emoji or icon to display next to the alert. If ``icon``
            is ``None`` (default), no icon is displayed. If ``icon`` is a
            string, the following options are valid:

            - A single-character emoji. For example, you can set ``icon="🚨"``
              or ``icon="🔥"``. Emoji short codes are not supported.

            - An icon from the Material Symbols library (rounded style) in the
              format ``":material/icon_name:"`` where "icon_name" is the name
              of the icon in snake case.

              For example, ``icon=":material/thumb_up:"`` will display the
              Thumb Up icon. Find additional icons in the `Material Symbols \
              <https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded>`_
              font library.

        width : "stretch" or int
            The width of the alert. If "stretch" (default), the alert will expand
            to fill the available width in its container. If an int, the alert will
            have the given width in pixels.

        scale : float or int
            A scale factor to multiply the width by. This parameter only has an
            effect when width="stretch" and the parent container is a horizontal
            container. Default is 1.0.

        Example
        -------
        >>> import streamlit as st
        >>>
        >>> st.success('This is a success message!', icon="✅")

        """
        alert_proto = AlertProto()
        alert_proto.body = clean_text(body)
        alert_proto.icon = validate_icon_or_emoji(icon)
        alert_proto.format = AlertProto.SUCCESS

        # Handle width parameter
        alert_proto.width = str(width)

        # Handle scale parameter
        if isinstance(scale, (int, float)) and scale > 0:
            alert_proto.scale = float(scale)
        else:
            raise StreamlitAPIException(
                f"'{str(scale)}' is not an accepted value. scale must be a positive number."
            )

        return self.dg._enqueue("alert", alert_proto)

    @property
    def dg(self) -> DeltaGenerator:
        """Get our DeltaGenerator."""
        return cast("DeltaGenerator", self)
