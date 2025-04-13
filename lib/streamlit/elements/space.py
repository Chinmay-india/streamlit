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

from typing import TYPE_CHECKING, Literal, cast

from streamlit.proto.Space_pb2 import Space as SpaceProto
from streamlit.runtime.metrics_util import gather_metrics

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator


class SpaceMixin:
    @gather_metrics("space")
    def space(
        self,
        *,
        size: Literal["stretch"] | int = "stretch",
    ) -> DeltaGenerator:
        """Insert a flexible space.

        Parameters
        ----------
        size : "stretch" or int
            The size of the space. The behavior depends on the parent container's direction:

            - In vertical containers (default):
              - If an integer, creates a space with that many pixels of height.
              - If "stretch", creates a space that pushes content apart vertically.

            - In horizontal containers:
              - If an integer, creates a space with that many pixels of width.
              - If "stretch", creates a space that pushes content apart horizontally.

            Default is 50 pixels.

        Example
        -------
        >>> import streamlit as st
        >>>
        >>> # In vertical layout (default):
        >>> st.write("This text is before the space.")
        >>> st.space(size=100)  # 100px tall space
        >>> st.write("This text is after the space.")
        >>>
        >>> # Using "stretch" to push content to the edges of a container
        >>> with st.container(height=200):
        >>>     st.write("Top")
        >>>     st.space(size="stretch")  # Pushes content to top and bottom
        >>>     st.write("Bottom")
        >>>
        >>> # In horizontal layout:
        >>> with st.container(direction="horizontal"):
        >>>     st.write("Left")
        >>>     st.space(size=50)  # 50px wide space
        >>>     st.write("Middle")
        >>>     st.space(size="stretch")  # Pushes "Middle" to the left and "Right" to the right
        >>>     st.write("Right")

        """
        space_proto = SpaceProto()

        # Set size parameter as string
        space_proto.size = str(size)

        return self.dg._enqueue("space", space_proto)

    @property
    def dg(self) -> DeltaGenerator:
        """Get our DeltaGenerator."""
        return cast("DeltaGenerator", self)
