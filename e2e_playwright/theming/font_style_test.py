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


import json
import os

import pytest  # type: ignore
from playwright.sync_api import Page, expect  # type: ignore

from e2e_playwright.conftest import ImageCompareFunction
from e2e_playwright.shared.app_utils import expect_font


@pytest.fixture(scope="module")
@pytest.mark.early
def configure_notosans_font():
    """Configure NotoSans font with regular and italic variants."""
    os.environ["STREAMLIT_THEME_FONT_FACES"] = json.dumps(
        [
            {
                "family": "Noto Sans",
                "url": "https://fonts.gstatic.com/s/notosans/v30/o-0IIpQlx3QUlC5A4PNr5TRA.woff2",
                "weight": 400,
                "style": "normal",
            },
            {
                "family": "Noto Sans",
                "url": "https://fonts.gstatic.com/s/notosans/v30/o-0OIpQlx3QUlC5A4PNr5TRG.woff2",
                "weight": 400,
                "style": "italic",
            },
        ]
    )
    os.environ["STREAMLIT_THEME_FONT"] = (
        '"Noto Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
    )
    os.environ["STREAMLIT_THEME_BASE_FONT_SIZE"] = "16"
    os.environ["STREAMLIT_CLIENT_TOOLBAR_MODE"] = "minimal"
    yield
    del os.environ["STREAMLIT_THEME_FONT_FACES"]
    del os.environ["STREAMLIT_THEME_FONT"]
    del os.environ["STREAMLIT_THEME_BASE_FONT_SIZE"]
    del os.environ["STREAMLIT_CLIENT_TOOLBAR_MODE"]


@pytest.mark.usefixtures("configure_notosans_font")
def test_font_style(app: Page, assert_snapshot: ImageCompareFunction):
    # Make sure that all elements are rendered and no skeletons are shown
    expect(app.get_by_test_id("stSkeleton")).to_have_count(0, timeout=25000)

    # Verify Noto Sans font is loaded
    expect_font(app, "Noto Sans")

    # Take snapshots of each text element individually inside their containers
    normal_text = app.locator(
        '[data-testid="stContainer"][key="normal_text_container"] [data-testid="stMarkdown"]'
    )
    assert_snapshot(normal_text, name="notosans_normal_text")

    italic_text = app.locator(
        '[data-testid="stContainer"][key="italic_text_container"] [data-testid="stMarkdown"]'
    )
    assert_snapshot(italic_text, name="notosans_italic_text")

    mixed_text = app.locator(
        '[data-testid="stContainer"][key="mixed_text_container"] [data-testid="stMarkdown"]'
    )
    assert_snapshot(mixed_text, name="notosans_mixed_text")

    code_italic = app.locator(
        '[data-testid="stContainer"][key="code_italic_container"] [data-testid="stMarkdown"]'
    )
    assert_snapshot(code_italic, name="notosans_code_italic")

    long_paragraph = app.locator(
        '[data-testid="stContainer"][key="long_paragraph_container"] [data-testid="stMarkdown"]'
    )
    assert_snapshot(long_paragraph, name="notosans_long_paragraph")
