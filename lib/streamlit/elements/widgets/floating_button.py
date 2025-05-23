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

"""Floating Button element."""

from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent
from typing import TYPE_CHECKING, Literal, cast

from streamlit.elements.lib.utils import compute_and_register_element_id, to_key
from streamlit.errors import StreamlitAPIException
from streamlit.proto.FloatingButton_pb2 import FloatingButton as FloatingButtonProto
from streamlit.runtime.metrics_util import gather_metrics
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.runtime.state import (
    WidgetArgs,
    WidgetCallback,
    WidgetKwargs,
    register_widget,
)
from streamlit.string_util import validate_icon_or_emoji

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator


@dataclass
class FloatingButtonSerde:
    def serialize(self, v: bool) -> bool:
        return bool(v)

    def deserialize(self, ui_value: bool | None, widget_id: str = "") -> bool:
        return ui_value or False


class FloatingButtonMixin:
    @gather_metrics("floating_button")
    def floating_button(
        self,
        label: str,
        key: str | None = None,
        help: str | None = None,
        on_click: WidgetCallback | None = None,
        args: WidgetArgs | None = None,
        kwargs: WidgetKwargs | None = None,
        *,  # keyword-only arguments:
        type: Literal["primary", "secondary"] = "primary",
        icon: str | None = None,
        disabled: bool = False,
    ) -> bool:
        r"""Display a floating action button in the bottom right corner of the app.

        A floating action button appears as a circular icon floating above the UI and
        is used for a promoted action.

        Parameters
        ----------
        label : str
            A short label explaining to the user what this button is for.
            The label can optionally contain GitHub-flavored Markdown of the
            following types: Bold, Italics, Strikethroughs, Inline Code, Links,
            and Images. Images display like icons, with a max height equal to
            the font height.

            Unsupported Markdown elements are unwrapped so only their children
            (text contents) render. Display unsupported elements as literal
            characters by backslash-escaping them. E.g.,
            ``"1\. Not an ordered list"``.

            See the ``body`` parameter of |st.markdown|_ for additional,
            supported Markdown directives.

            .. |st.markdown| replace:: ``st.markdown``
            .. _st.markdown: https://docs.streamlit.io/develop/api-reference/text/st.markdown

        key : str or int
            An optional string or integer to use as the unique key for the widget.
            If this is omitted, a key will be generated for the widget
            based on its content. No two widgets may have the same key.

        help : str or None
            A tooltip that gets displayed when the button is hovered over. If
            this is ``None`` (default), no tooltip is displayed.

            The tooltip can optionally contain GitHub-flavored Markdown,
            including the Markdown directives described in the ``body``
            parameter of ``st.markdown``.

        on_click : callable
            An optional callback invoked when this button is clicked.

        args : tuple
            An optional tuple of args to pass to the callback.

        kwargs : dict
            An optional dict of kwargs to pass to the callback.

        type : "primary" or "secondary"
            An optional string that specifies the button type. This can be one
            of the following:

            - ``"primary"`` (default): The button's background is the app's primary color
              for additional emphasis.
            - ``"secondary"``: The button's background coordinates
              with the app's background color for normal emphasis.

        icon : str or None
            An optional emoji or icon to display next to the button label. If ``icon``
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

        disabled : bool
            An optional boolean that disables the button if set to ``True``.
            The default is ``False``.

        Returns
        -------
        bool
            True if the button was clicked on the last run of the app,
            False otherwise.

        Example
        -------
        >>> import streamlit as st
        >>>
        >>> if st.floating_button("Chat", icon=":material/chat:"):
        ...     st.write("Button was clicked")
        >>>
        """

        # Checks whether the entered button type is one of the allowed options
        if type not in ["primary", "secondary"]:
            raise StreamlitAPIException(
                'The type argument to st.floating_button must be "primary" or "secondary". '
                f'\nThe argument passed was "{type}".'
            )

        return self._floating_button(
            label,
            key,
            help,
            on_click=on_click,
            args=args,
            kwargs=kwargs,
            disabled=disabled,
            type=type,
            icon=icon,
        )

    def _floating_button(
        self,
        label: str,
        key: str | None,
        help: str | None,
        on_click: WidgetCallback | None = None,
        args: WidgetArgs | None = None,
        kwargs: WidgetKwargs | None = None,
        *,  # keyword-only arguments:
        type: Literal["primary", "secondary"] = "primary",
        icon: str | None = None,
        disabled: bool = False,
    ) -> bool:
        key = to_key(key)
        ctx = get_script_run_ctx()

        element_id = compute_and_register_element_id(
            "floating_button",
            user_key=key,
            form_id=None,  # Floating buttons can't be in forms
            label=label,
            icon=icon,
            help=help,
            type=type,
        )

        floating_button_proto = FloatingButtonProto()
        floating_button_proto.id = element_id
        floating_button_proto.label = label
        floating_button_proto.type = type
        floating_button_proto.disabled = disabled

        if help is not None:
            floating_button_proto.help = dedent(help)

        if icon is not None:
            floating_button_proto.icon = validate_icon_or_emoji(icon)

        serde = FloatingButtonSerde()

        button_state = register_widget(
            floating_button_proto.id,
            on_change_handler=on_click,
            args=args,
            kwargs=kwargs,
            deserializer=serde.deserialize,
            serializer=serde.serialize,
            ctx=ctx,
            value_type="trigger_value",
        )

        self.dg._enqueue("floating_button", floating_button_proto)

        return button_state.value

    @property
    def dg(self) -> DeltaGenerator:
        """Get our DeltaGenerator."""
        return cast("DeltaGenerator", self)
