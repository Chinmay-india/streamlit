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

from e2e_playwright.conftest import ImageCompareFunction
from e2e_playwright.shared.app_utils import check_top_level_class


def select_selectbox_option(page: Page, option: str) -> None:
    """Select an option from a selectbox.

    Parameters
    ----------
    page : Page
        The page to interact with.
    option : str
        The option to select.
    """
    # Find the selectbox input
    selectbox = page.locator('select:has-text("Select floating button to display:")')
    # Open the dropdown
    selectbox.click()
    # Select the option
    page.locator(f'option:has-text("{option}")').click()
    # Wait for the app to reload
    page.wait_for_load_state("networkidle")


def test_floating_button_rendering(
    themed_app: Page, assert_snapshot: ImageCompareFunction
):
    """Test that the floating button is correctly rendered via screenshot matching."""
    # Default button
    floating_button = themed_app.get_by_test_id("stFloatingButton")
    expect(floating_button).to_be_visible()
    assert_snapshot(floating_button, name="st_floating_button-default")

    # Primary button
    select_selectbox_option(themed_app, "Primary Button")
    floating_button = themed_app.get_by_test_id("stFloatingButton")
    expect(floating_button).to_be_visible()
    assert_snapshot(floating_button, name="st_floating_button-primary")

    # Secondary button
    select_selectbox_option(themed_app, "Secondary Button")
    floating_button = themed_app.get_by_test_id("stFloatingButton")
    expect(floating_button).to_be_visible()
    assert_snapshot(floating_button, name="st_floating_button-secondary")

    # Button with emoji icon
    select_selectbox_option(themed_app, "Button with Icon")
    floating_button = themed_app.get_by_test_id("stFloatingButton")
    expect(floating_button).to_be_visible()
    assert_snapshot(floating_button, name="st_floating_button-with_emoji_icon")

    # Button with material icon
    select_selectbox_option(themed_app, "Button with Material Icon")
    floating_button = themed_app.get_by_test_id("stFloatingButton")
    expect(floating_button).to_be_visible()
    assert_snapshot(floating_button, name="st_floating_button-with_material_icon")

    # Disabled button
    select_selectbox_option(themed_app, "Disabled Button")
    floating_button = themed_app.get_by_test_id("stFloatingButton")
    expect(floating_button).to_be_visible()
    assert_snapshot(floating_button, name="st_floating_button-disabled")


def test_floating_button_positioning(app: Page):
    """Test that the floating button is positioned at the bottom right corner."""
    # Get the floating button element
    floating_button = app.get_by_test_id("stFloatingButton")
    expect(floating_button).to_be_visible()

    # Get viewport size
    viewport_size = app.viewport_size
    if viewport_size is None:
        # Skip the test if viewport size can't be determined
        return

    viewport_width = viewport_size["width"]
    viewport_height = viewport_size["height"]

    # Get the bounding box of the floating button
    bounding_box = floating_button.bounding_box()
    if bounding_box is None:
        # Skip the test if bounding box can't be determined
        return

    # Check that the button is positioned at the bottom right (with some margin)
    # Allowing for margins, the button should be at most 100px from the edges
    assert bounding_box["x"] + bounding_box["width"] > viewport_width - 100
    assert bounding_box["y"] + bounding_box["height"] > viewport_height - 100


def test_floating_button_tooltip(app: Page, assert_snapshot: ImageCompareFunction):
    """Test that the floating button shows a tooltip when hovered."""
    # Select button with tooltip
    select_selectbox_option(app, "Button with Tooltip")

    # Get the floating button element
    floating_button = app.get_by_test_id("stFloatingButton")
    expect(floating_button).to_be_visible()

    # Hover over the button to show the tooltip
    floating_button.hover()

    # Check that the tooltip is visible
    tooltip = app.get_by_test_id("stTooltipContent")
    expect(tooltip).to_be_visible()
    expect(tooltip).to_have_text("This is a floating action button with a tooltip")

    # Take a screenshot of the button with tooltip
    assert_snapshot(floating_button, name="st_floating_button-with_tooltip")


def test_floating_button_click(app: Page):
    """Test that clicking the floating button triggers the expected action."""
    # Select button with callback
    select_selectbox_option(app, "Button with Callback")

    # Before clicking, there should be no success message
    success_message = app.get_by_test_id("stSuccessMessage")
    expect(success_message).to_have_count(0)

    # Get the floating button element and click it
    floating_button = app.get_by_test_id("stFloatingButton")
    expect(floating_button).to_be_visible()
    floating_button.click()

    # After clicking, there should be a success message indicating the button was clicked
    success_message = app.get_by_test_id("stSuccessMessage")
    expect(success_message).to_be_visible()
    expect(success_message).to_contain_text("Button was clicked! Click count: 1")

    # Click again to verify the counter increases
    floating_button.click()
    success_message = app.get_by_test_id("stSuccessMessage")
    expect(success_message).to_contain_text("Button was clicked! Click count: 2")


def test_check_top_level_class(app: Page):
    """Check that the top level class is correctly set."""
    check_top_level_class(app, "stFloatingButton")


def test_floating_button_stays_fixed_on_scroll(app: Page):
    """Test that the floating button stays fixed while scrolling."""
    # Get the initial position of the floating button
    floating_button = app.get_by_test_id("stFloatingButton")
    expect(floating_button).to_be_visible()

    initial_position = floating_button.bounding_box()
    if initial_position is None:
        # Skip the test if position can't be determined
        return

    # Scroll down to the bottom of the page
    app.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    # Get the new position of the floating button
    new_position = floating_button.bounding_box()
    if new_position is None:
        # Skip the test if position can't be determined
        return

    # The Y position relative to the viewport should remain approximately the same
    # allowing for minor variations due to viewport resizing
    y_diff = abs(initial_position["y"] - new_position["y"])
    assert y_diff < 50, "Floating button should stay fixed vertically while scrolling"

    x_diff = abs(initial_position["x"] - new_position["x"])
    assert x_diff < 50, "Floating button should stay fixed horizontally while scrolling"
