# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
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

import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from streamlit.proto.Html_pb2 import Html as HtmlProto
from streamlit.runtime.metrics_util import gather_metrics
from streamlit.string_util import clean_text
from streamlit.type_util import SupportsReprHtml

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator


class HtmlMixin:
    @gather_metrics("html")
    def html(
        self,
        body: str | Path | Any,
    ) -> DeltaGenerator:
        """Insert HTML into your app.

        Adding custom HTML to your app impacts safety, styling, and
        maintainability. We sanitize HTML with `DOMPurify
        <https://github.com/cure53/DOMPurify>`_, but inserting HTML remains a
        developer risk. Passing untrusted code to ``st.html`` or dynamically
        loading external code can increase the risk of vulnerabilities in your
        app.

        ``st.html`` content is **not** iframed. Executing JavaScript is not
        supported at this time.

        Parameters
        ----------
        body : str, Path, Any
            The HTML code to insert, or path to an HTML code file which is
            loaded and inserted.

            If the provided string is the path of a local file, Streamlit will
            load the file and render its contents as HTML. Otherwise, Streamlit
            will render the string directly as HTML.

            If anything other than a string or file path is passed, it will
            be converted to a string behind the scenes by calling
            `body._repr_html_()`, if present, and `str(body)`, otherwise.

        Example
        -------
        >>> import streamlit as st
        >>>
        >>> st.html(
        ...     "<p><span style='text-decoration: line-through double red;'>Oops</span>!</p>"
        ... )

        .. output::
           https://doc-html.streamlit.app/
           height: 300px

        """
        html_proto = HtmlProto()

        # If body supports _repr_html_, use that.
        if isinstance(body, SupportsReprHtml):
            html_proto.body = body._repr_html_()

        # If body is a str that doesn't look liek a file path, use that.
        # (This avoids a filesystem lookup later on. Premature optimization, I know. But
        # it feels right!)
        elif _is_str_but_unlikely_a_path(body):
            html_proto.body = clean_text(body)

        # Check if the body is a file path. May include filesystem lookup.
        elif isinstance(body, Path) or _is_file(body):
            with open(body, encoding="utf-8") as f:
                html_proto.body = f.read()

        # OK, let's just try converting to string and hope for the best.
        else:
            html_proto.body = clean_text(body)

        return self.dg._enqueue("html", html_proto)

    @property
    def dg(self) -> DeltaGenerator:
        """Get our DeltaGenerator."""
        return cast("DeltaGenerator", self)


def _is_file(obj: Any) -> bool:
    try:
        return os.path.isfile(obj)
    except TypeError:
        return False


def _is_str_but_unlikely_a_path(obj: Any) -> bool:
    if not isinstance(obj, str):
        return False

    # Cheap test of whether a string that could be HTML looks like a file path. File
    # paths are extremely unlikely to have "<" or "\n", so if they're present we assume
    # HTML. This is not guaranteed to be correct, but it's probably 100% of times in
    # real-world use cases, so it feels like a good tradeoff.
    return any(c in obj for c in ["<", "\n"])
