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

import unittest
from http.cookies import Morsel
from unittest.mock import MagicMock, patch

from parameterized import parameterized
from tornado.httputil import HTTPHeaders

import streamlit as st
from streamlit.runtime.context import (
    _normalize_header,
    maybe_add_page_path,
    maybe_trim_page_path,
)


class StContextTest(unittest.TestCase):
    mocked_cookie = Morsel()
    mocked_cookie.set("cookieName", "cookieValue", "cookieValue")

    @patch(
        "streamlit.runtime.context._get_request",
        MagicMock(
            return_value=MagicMock(headers=HTTPHeaders({"the-header": "header-value"}))
        ),
    )
    def test_context_headers(self):
        """Test that `st.context.headers` returns headers from ScriptRunContext"""
        assert st.context.headers.to_dict() == {"The-Header": "header-value"}

    @patch(
        "streamlit.runtime.context._get_request",
        MagicMock(return_value=MagicMock(cookies={"cookieName": mocked_cookie})),
    )
    def test_context_cookies(self):
        """Test that `st.context.cookies` returns cookies from ScriptRunContext"""
        assert st.context.cookies.to_dict() == {"cookieName": "cookieValue"}

    @patch(
        "streamlit.runtime.context._get_request",
        MagicMock(return_value=MagicMock(remote_ip="8.8.8.8")),
    )
    def test_ip_address(self):
        """Test that `st.context.ip_address` returns remote_ip from Tornado request"""
        assert st.context.ip_address == "8.8.8.8"

    @patch(
        "streamlit.runtime.context._get_request",
        MagicMock(return_value=MagicMock(remote_ip="127.0.0.1")),
    )
    def test_ip_address_localhost(self):
        """Test that `st.context.ip_address` returns None if run on localhost"""
        assert st.context.ip_address is None

    @patch(
        "streamlit.runtime.context.get_script_run_ctx",
        MagicMock(return_value=None),
    )
    def test_url_none_context(self):
        """Test that `st.context.url` returns None if context is None"""
        assert st.context.url is None

    @patch("streamlit.runtime.context.get_script_run_ctx")
    def test_url_none_context_info(self, mock_get_script_run_ctx):
        """Test that `st.context.url` returns None if context_info is None"""
        # Create a mock context with None context_info
        mock_ctx = MagicMock()
        mock_ctx.context_info = None
        mock_get_script_run_ctx.return_value = mock_ctx

        assert st.context.url is None

    @patch("streamlit.runtime.context.get_script_run_ctx")
    @patch("streamlit.runtime.context.maybe_trim_page_path")
    @patch("streamlit.runtime.context.maybe_add_page_path")
    def test_url(self, mock_add_path, mock_trim_path, mock_get_script_run_ctx):
        """Test that `st.context.url` returns the URL from the context after processing"""
        # Create a mock context with a URL
        mock_context_info = MagicMock()
        mock_context_info.url = "https://example.com/original"

        mock_ctx = MagicMock()
        mock_ctx.context_info = mock_context_info
        mock_get_script_run_ctx.return_value = mock_ctx

        # Mock the page manager
        mock_ctx.pages_manager = MagicMock()

        # Set up the mock return values for the URL processing functions
        mock_trim_path.return_value = "https://example.com/trimmed"
        mock_add_path.return_value = "https://example.com/trimmed/added"

        # Test that the URL is processed by both functions
        result = st.context.url

        # Verify the result
        assert result == "https://example.com/trimmed/added"

        # Verify that the functions were called with the correct arguments
        mock_trim_path.assert_called_once_with(
            "https://example.com/original", mock_ctx.pages_manager
        )
        mock_add_path.assert_called_once_with(
            "https://example.com/trimmed", mock_ctx.pages_manager
        )

    @parameterized.expand(
        [
            ("coNtent-TYPE", "Content-Type"),
            ("coNtent-type", "Content-Type"),
            ("Content-Type", "Content-Type"),
            ("Content-Type", "Content-Type"),
            ("Cache-Control", "Cache-Control"),
            ("Cache-control", "Cache-Control"),
            ("cache-control", "Cache-Control"),
            ("cache-CONTROL", "Cache-Control"),
            ("Access-Control-Max-Age", "Access-Control-Max-Age"),
            ("Access-control-max-age", "Access-Control-Max-Age"),
            ("access-control-MAX-age", "Access-Control-Max-Age"),
        ]
    )
    def test_normalize_header(self, name, expected):
        """Test that `_normalize_header` normalizes header names"""
        assert _normalize_header(name) == expected

    @parameterized.expand(
        [
            # Test case: URL with no page path
            ("https://example.com", {}, "https://example.com"),
            # Test case: URL with page path that matches a page
            (
                "https://example.com/page1",
                {"hash1": {"url_pathname": "page1"}},
                "https://example.com/",
            ),
            # Test case: URL with page path that doesn't match any page
            (
                "https://example.com/unknown",
                {"hash1": {"url_pathname": "page1"}},
                "https://example.com/unknown",
            ),
            # Test case: URL with trailing slash
            (
                "https://example.com/page1/",
                {"hash1": {"url_pathname": "page1"}},
                "https://example.com/",
            ),
            # Test case: URL with multiple segments where the last segment matches a page
            (
                "https://example.com/path/to/page1",
                {"hash1": {"url_pathname": "page1"}},
                "https://example.com/path/to/",
            ),
            # Test case: URL with empty page path in pages
            (
                "https://example.com",
                {"hash1": {"url_pathname": ""}},
                "https://example.com",
            ),
            # Test case: URL with multiple pages, one matching
            (
                "https://example.com/page2",
                {
                    "hash1": {"url_pathname": "page1"},
                    "hash2": {"url_pathname": "page2"},
                    "hash3": {"url_pathname": "page3"},
                },
                "https://example.com/",
            ),
        ]
    )
    def test_maybe_trim_page_path(self, url, pages, expected):
        """Test that `maybe_trim_page_path` correctly trims page paths from URLs"""
        # Create a mock PagesManager
        mock_page_manager = MagicMock()
        mock_page_manager.get_pages.return_value = pages

        # Call the function and check the result
        result = maybe_trim_page_path(url, mock_page_manager)
        assert result == expected

    @parameterized.expand(
        [
            # Test case: URL with no current page
            ("https://example.com", "", {}, "https://example.com"),
            # Test case: URL with the current page that has a url_pathname
            (
                "https://example.com",
                "hash1",
                {"hash1": {"url_pathname": "page1"}},
                "https://example.com/page1",
            ),
            # Test case: URL with current page that has no url_pathname
            (
                "https://example.com",
                "hash1",
                {"hash1": {"page_name": "Page 1"}},
                "https://example.com",
            ),
            # Test case: URL with current page that has empty url_pathname
            (
                "https://example.com",
                "hash1",
                {"hash1": {"url_pathname": ""}},
                "https://example.com",
            ),
            # Test case: URL with trailing slash
            (
                "https://example.com/",
                "hash1",
                {"hash1": {"url_pathname": "page1"}},
                "https://example.com/page1",
            ),
            # Test case: URL with current page hash that doesn't exist in pages
            (
                "https://example.com",
                "unknown",
                {"hash1": {"url_pathname": "page1"}},
                "https://example.com",
            ),
        ]
    )
    def test_maybe_add_page_path(self, url, current_hash, pages, expected):
        """Test that `maybe_add_page_path` correctly adds page paths to URLs"""
        # Create a mock PagesManager
        mock_page_manager = MagicMock()
        mock_page_manager.current_page_script_hash = current_hash
        mock_page_manager.get_pages.return_value = pages

        # Call the function and check the result
        result = maybe_add_page_path(url, mock_page_manager)
        assert result == expected
