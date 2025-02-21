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
import time


def wait_for_bounding_box(locator, condition_fn, timeout=5.0, interval=0.1):
    """Wait for a locator's bounding box to satisfy a given condition.

    Args:
        locator: A Playwright locator object.
        condition_fn: A function that takes a bounding box and returns a boolean.
        timeout: Maximum time to wait in seconds (default: 5.0).
        interval: Time between checks in seconds (default: 0.1).

    Returns:
        The bounding box that satisfied the condition.

    Raises:
        AssertionError: If the condition is not met within the timeout period.
    """
    start = time.time()
    while time.time() - start < timeout:
        bbox = locator.bounding_box()
        if bbox is not None and condition_fn(bbox):
            return bbox
        time.sleep(interval)
    raise AssertionError("Timeout waiting for bounding box condition")
