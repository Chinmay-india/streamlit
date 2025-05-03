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

"""media.py unit tests that are common to st.audio + st.video"""

from enum import Enum
from pathlib import Path
from unittest import mock

from parameterized import parameterized

import streamlit as st
from streamlit.cursor import make_delta_path
from streamlit.elements.media import MediaData
from streamlit.errors import StreamlitInvalidWidthError
from streamlit.proto.RootContainer_pb2 import RootContainer
from tests.delta_generator_test_case import DeltaGeneratorTestCase
from tests.streamlit.elements.layout_test_utils import WidthConfigFields


class MockMediaKind(Enum):
    AUDIO = "audio"
    VIDEO = "video"


class MediaTest(DeltaGeneratorTestCase):
    @parameterized.expand(
        [
            ("foo.wav", "audio/wav", MockMediaKind.AUDIO, False),
            (Path("foo.wav"), "audio/wav", MockMediaKind.AUDIO, False),
            ("path/to/foo.wav", "audio/wav", MockMediaKind.AUDIO, False),
            (Path("path/to/foo.wav"), "audio/wav", MockMediaKind.AUDIO, False),
            (b"fake_audio_data", "audio/wav", MockMediaKind.AUDIO, False),
            ("https://foo.com/foo.wav", "audio/wav", MockMediaKind.AUDIO, True),
            ("foo.mp4", "video/mp4", MockMediaKind.VIDEO, False),
            (Path("foo.mp4"), "video/mp4", MockMediaKind.VIDEO, False),
            ("path/to/foo.mp4", "video/mp4", MockMediaKind.VIDEO, False),
            (Path("path/to/foo.mp4"), "video/mp4", MockMediaKind.VIDEO, False),
            (b"fake_video_data", "video/mp4", MockMediaKind.VIDEO, False),
            ("https://foo.com/foo.mp4", "video/mp4", MockMediaKind.VIDEO, True),
        ]
    )
    def test_add_bytes_and_filenames_to_mediafilemanager(
        self,
        media_data: MediaData,
        mimetype: str,
        media_kind: MockMediaKind,
        is_url: bool,
    ):
        """st.audio + st.video should register bytes and filenames with the
        MediaFileManager. URL-based media does not go through the MediaFileManager.
        """
        with (
            mock.patch(
                "streamlit.runtime.media_file_manager.MediaFileManager.add"
            ) as mock_mfm_add,
            mock.patch("streamlit.runtime.caching.save_media_data"),
        ):
            mock_mfm_add.return_value = "https://mockoutputurl.com"

            if media_kind is MockMediaKind.AUDIO:
                st.audio(media_data, mimetype)
                element = self.get_delta_from_queue().new_element
                element_url = element.audio.url
            else:
                st.video(media_data, mimetype)
                element = self.get_delta_from_queue().new_element
                element_url = element.video.url

            if is_url:
                # URLs should be returned as-is, and should not result in a call to
                # MediaFileManager.add
                self.assertEqual(media_data, element_url)
                mock_mfm_add.assert_not_called()
            else:
                # Other strings, Path objects, and audio/video data, should be passed to
                # MediaFileManager.add
                expected_media_data = (
                    str(media_data) if isinstance(media_data, Path) else media_data
                )
                mock_mfm_add.assert_called_once_with(
                    expected_media_data,
                    mimetype,
                    str(make_delta_path(RootContainer.MAIN, (), 0)),
                )
                self.assertEqual("https://mockoutputurl.com", element_url)

    @parameterized.expand(
        [
            (MockMediaKind.AUDIO,),
            (MockMediaKind.VIDEO,),
        ]
    )
    def test_width_config_default(self, media_kind: MockMediaKind):
        """Test that default width is 'stretch'."""
        if media_kind is MockMediaKind.AUDIO:
            st.audio("foo.mp3")
            c = self.get_delta_from_queue().new_element.audio
        else:
            st.video("foo.mp4")
            c = self.get_delta_from_queue().new_element.video

        self.assertEqual(
            c.width_config.WhichOneof("width_spec"), WidthConfigFields.USE_STRETCH.value
        )
        self.assertTrue(c.width_config.use_stretch)

    @parameterized.expand(
        [
            (MockMediaKind.AUDIO,),
            (MockMediaKind.VIDEO,),
        ]
    )
    def test_width_config_pixel(self, media_kind: MockMediaKind):
        """Test that pixel width works properly."""
        if media_kind is MockMediaKind.AUDIO:
            st.audio("foo.mp3", width=200)
            c = self.get_delta_from_queue().new_element.audio
        else:
            st.video("foo.mp4", width=200)
            c = self.get_delta_from_queue().new_element.video

        self.assertEqual(
            c.width_config.WhichOneof("width_spec"), WidthConfigFields.PIXEL_WIDTH.value
        )
        self.assertEqual(c.width_config.pixel_width, 200)

    @parameterized.expand(
        [
            (MockMediaKind.AUDIO,),
            (MockMediaKind.VIDEO,),
        ]
    )
    def test_width_config_stretch(self, media_kind: MockMediaKind):
        """Test that 'stretch' width works properly."""
        if media_kind is MockMediaKind.AUDIO:
            st.audio("foo.mp3", width="stretch")
            c = self.get_delta_from_queue().new_element.audio
        else:
            st.video("foo.mp4", width="stretch")
            c = self.get_delta_from_queue().new_element.video

        self.assertEqual(
            c.width_config.WhichOneof("width_spec"), WidthConfigFields.USE_STRETCH.value
        )
        self.assertTrue(c.width_config.use_stretch)

    @parameterized.expand(
        [
            (MockMediaKind.AUDIO, "invalid"),
            (MockMediaKind.AUDIO, -100),
            (MockMediaKind.AUDIO, 0),
            (MockMediaKind.AUDIO, 100.5),
            (MockMediaKind.AUDIO, None),
            (MockMediaKind.VIDEO, "invalid"),
            (MockMediaKind.VIDEO, -100),
            (MockMediaKind.VIDEO, 0),
            (MockMediaKind.VIDEO, 100.5),
            (MockMediaKind.VIDEO, None),
        ]
    )
    def test_invalid_width(self, media_kind: MockMediaKind, width):
        """Test that invalid width values raise exceptions."""
        with self.assertRaises(StreamlitInvalidWidthError):
            if media_kind is MockMediaKind.AUDIO:
                st.audio("foo.mp3", width=width)
            else:
                st.video("foo.mp4", width=width)
