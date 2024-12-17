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

import re
import urllib.parse

from playwright.sync_api import Page, expect

from e2e_playwright.conftest import wait_for_app_run, wait_until


def navigate_to_page(app: Page, index: int):
    app.get_by_test_id("stSidebarNav").locator("a").nth(index).click()
    wait_for_app_run(app)
    # Move the mouse to the top left corner to prevent any weird hover effects
    # in the screenshots
    app.mouse.move(0, 0)


def navigate_to_page_via_page_link(app: Page, index: int):
    app.get_by_test_id("stPageLink").locator("a").nth(index).click()
    wait_for_app_run(app)
    # Move the mouse to the top left corner to prevent any weird hover effects
    # in the screenshots
    app.mouse.move(0, 0)


def navigate_to_page_via_button(app: Page, index: int):
    app.get_by_test_id("stButton").locator("button").nth(index).click()
    wait_for_app_run(app)
    # Move the mouse to the top left corner to prevent any weird hover effects
    # in the screenshots
    app.mouse.move(0, 0)


def check_query_params_printout(app: Page, markdown: str) -> None:
    expect(
        app.get_by_test_id("stMarkdownContainer")
        .locator("p", has_text=re.compile("^Query params"))
        .nth(0)
    ).to_contain_text(markdown)


def check_query_string(app: Page, entries: dict[str, list[str]]):
    def _has_query_string_matching_entries():
        appurl = urllib.parse.urlparse(app.url)
        url_query_string = urllib.parse.parse_qs(appurl.query)
        if not (url_query_string.keys() == entries.keys()):
            return False
        if not all(
            set(url_query_string.get(key) or []) == set(entries[key]) for key in entries
        ):
            return False
        return True

    wait_until(app, _has_query_string_matching_entries)


def test_navigation_via_page_link(app: Page) -> None:
    """Test that navigating via switch_page induces the correct query params change."""
    # Take the first page_link to page 14
    navigate_to_page_via_page_link(app, 0)

    check_query_params_printout(
        app, "Query params: {'navigation': 'from page link on page 1'}"
    )
    check_query_string(app, {"navigation": ["from page link on page 1"]})


def test_navigation_via_page_link_with_embed_params(app: Page) -> None:
    """Test that navigating via a page link preserves embed options in the query params."""
    # start with embed options
    app.goto(app.url + "?embed=true&embed_options=option1")
    # Take the first page_link to page 14
    navigate_to_page_via_page_link(app, 0)

    check_query_params_printout(
        app,
        "Query params: {'navigation': 'from page link on page 1', 'embed': 'true', 'embed_options': 'option1'}",
    )
    check_query_string(
        app,
        {
            "navigation": ["from page link on page 1"],
            "embed": ["true"],
            "embed_options": ["option1"],
        },
    )


def test_navigation_to_same_page_via_sidebar(app: Page) -> None:
    """Test that navigating to the same page via the sidebar clears the query params from the URL."""
    # Take the first page_link to page 14
    navigate_to_page_via_page_link(app, 0)
    # simulate re-clicking on the page 14 sidebar nav, this should _clear_ the query params
    navigate_to_page(app, 13)

    check_query_params_printout(app, "Query params: {}")
    check_query_string(app, {})


def test_navigation_to_new_page_via_sidebar(app: Page) -> None:
    """Test that navigating to a new page via the sidebar clears the query params from the URL."""
    # Take the first page_link to page 14
    navigate_to_page_via_page_link(app, 0)
    # simulate going back to page 1 via sidebar nav, this should _clear_ the query params
    navigate_to_page(app, 0)

    check_query_string(app, {})


# TODO: this test is flaky, indicative of a real problem that still needs to be understood
def test_navigation_via_switch_page(app: Page) -> None:
    """Test that navigating via switch_page induces the correct query params change."""
    # Take the first switch_page to page 14
    navigate_to_page_via_button(app, 0)

    check_query_params_printout(
        app, "Query params: {'navigation': 'from switch page on page 1'}"
    )
    check_query_string(app, {"navigation": ["from switch page on page 1"]})


def test_navigation_via_switch_page_with_embed_params(app: Page) -> None:
    """Test that navigating via switch_page induces the correct query params change."""
    # start with embed options
    app.goto(app.url + "?embed=true&embed_options=option1")
    # Take the first switch_page to page 14
    navigate_to_page_via_button(app, 0)

    check_query_params_printout(
        app,
        "Query params: {'navigation': 'from switch page on page 1'}",
    )
    check_query_string(
        app,
        {
            "navigation": ["from switch page on page 1"],
            "embed": ["true"],
            "embed_options": ["option1"],
        },
    )
