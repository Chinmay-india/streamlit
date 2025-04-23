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

from parameterized import parameterized

import streamlit as st
from streamlit.errors import StreamlitAPIException
from streamlit.proto.Layout_pb2 import Width as WidthProto
from tests.delta_generator_test_case import DeltaGeneratorTestCase


class StTextAPITest(DeltaGeneratorTestCase):
    """Test st.text API."""

    def test_st_text(self):
        """Test st.text."""
        st.text("some text")

        el = self.get_delta_from_queue().new_element
        assert el.text.body == "some text"

    def test_st_text_with_help(self):
        """Test st.text with help."""
        st.text("some text", help="help text")
        el = self.get_delta_from_queue().new_element
        assert el.text.body == "some text"
        assert el.text.help == "help text"

    @parameterized.expand(
        [
            (500, WidthProto.PIXEL, 500),
            ("stretch", WidthProto.STRETCH, 0),
            ("content", WidthProto.CONTENT, 0),
            (None, WidthProto.CONTENT, 0),
        ]
    )
    def test_st_text_with_width(
        self, width_value, expected_width_type, expected_pixel_width
    ):
        """Test st.text with different width types."""
        if width_value is None:
            st.text("some text")
        else:
            st.text("some text", width=width_value)

        el = self.get_delta_from_queue().new_element
        self.assertEqual(el.text.body, "some text")
        self.assertEqual(el.text.width_type, expected_width_type)
        self.assertEqual(el.text.pixel_width, expected_pixel_width)

    @parameterized.expand(
        [
            (
                "invalid",
                "Invalid width value: 'invalid'. Width must be either an integer (pixels), 'stretch', or 'content'.",
            ),
            (
                -100,
                "Invalid width value: -100. Width must be either an integer (pixels), 'stretch', or 'content'.",
            ),
        ]
    )
    def test_st_text_with_invalid_width(self, width_value, expected_error_message):
        """Test st.text with invalid width values."""
        with self.assertRaises(StreamlitAPIException) as exc:
            st.text("some text", width=width_value)

        self.assertEqual(expected_error_message, str(exc.exception))
