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

from playwright.sync_api import Page, expect

from e2e_playwright.conftest import ImageCompareFunction, wait_for_app_loaded


def test_static_app(page: Page, app_port: int, assert_snapshot: ImageCompareFunction):
    """Test that a static app can be loaded"""
    page.goto(f"http://localhost:{app_port}/?staticNotebookId=Load_CSV_from_S3")
    wait_for_app_loaded(page, True)

    app_cells = page.get_by_test_id("stExpander")
    expect(app_cells).to_have_count(20)

    first_cell = app_cells.nth(0)
    assert_snapshot(first_cell, name="example_static_app")
