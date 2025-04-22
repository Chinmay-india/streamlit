/**
 * Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2025)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// Type for the debounced function including the cancel method
interface DebouncedFunc<T extends unknown[]> {
  (...args: T): void;
  cancel: () => void;
}

// Simple debounce function
function debounce<T extends unknown[]>(
  func: (...args: T) => void,
  wait: number
): DebouncedFunc<T> {
  let timeout: ReturnType<typeof setTimeout> | null;

  const debounced = (...args: T): void => {
    if (timeout) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(() => {
      timeout = null;
      func(...args);
    }, wait);
  };

  debounced.cancel = (): void => {
    if (timeout) {
      clearTimeout(timeout);
      timeout = null;
    }
  };

  return debounced;
}

/**
 * Manages iframe height reporting and watching.
 */
export class IframeSizer {
  protected lastFrameHeight: number | undefined;

  protected resizeObserver: ResizeObserver | undefined;

  protected mutationObserver: MutationObserver | undefined;

  protected debouncedUpdateHeight: DebouncedFunc<[]> | undefined;

  protected readonly setHeightCallback: (height: number) => void;

  /**
   * Initializes the iframe sizing utility.
   * @param options - Configuration options.
   * @param options.setHeightCallback - The function to call when the height needs to be updated.
   */
  constructor(options: { setHeightCallback: (height: number) => void }) {
    this.setHeightCallback = options.setHeightCallback;
  }

  /**
   * Report the element's height.
   * This should be called every time the element changes its DOM - that is,
   * when it's first loaded, and any time it updates.
   * @param height The height to set. Defaults to the scrollHeight of the element.
   * @param element The target element. Defaults to document.body.
   */
  public setFrameHeight(
    height?: number,
    element: HTMLElement = document.body
  ): void {
    if (!element) {
      return;
    }

    if (height === undefined) {
      // `height` is optional. If undefined, it defaults to the full height of the element
      // including its margins.
      height = this.getElementFullHeight(element);
    }

    if (height === this.lastFrameHeight) {
      // Don't bother updating if our height hasn't changed.
      return;
    }

    this.lastFrameHeight = height;
    this.setHeightCallback(height);
  }

  /**
   * Watch the frame height and update the component's height when it changes.
   * This should be called only once when the component is mounted.
   *
   * @param element The target element to watch. Defaults to document.body.
   * @returns A function to stop watching the frame height.
   */
  public watchFrameHeight(element: HTMLElement = document.body): () => void {
    if (!element) {
      return () => {};
    }

    if (this.resizeObserver || this.mutationObserver) {
      this.stopWatchingFrameHeight();
    }

    // Define the updateHeight function
    const updateHeight = (): void => {
      // Calculate the full height of the element. Note that infinite update loops
      // are prevented by the check in setFrameHeight that avoids updates when
      // height hasn't changed.
      const newHeight = this.getElementFullHeight(element);

      // Pass the element to setFrameHeight as well
      this.setFrameHeight(newHeight, element);
    };

    // Debounce the updateHeight function for observer callbacks
    this.debouncedUpdateHeight = debounce(updateHeight, 100);

    // Use ResizeObserver to efficiently detect direct size changes.
    this.resizeObserver = new ResizeObserver(() => {
      this.debouncedUpdateHeight?.();
    });
    this.resizeObserver.observe(element);

    // Use MutationObserver to catch other changes (e.g., adding/removing children)
    // that might affect scrollHeight.
    this.mutationObserver = new MutationObserver(() => {
      this.debouncedUpdateHeight?.();
    });
    this.mutationObserver.observe(element, {
      attributes: true, // Catch style changes
      childList: true, // Catch added/removed elements
      subtree: true, // Observe the entire subtree
      characterData: true, // Catch text content changes
    });

    // Initial height check (not debounced) - call updateHeight immediately
    updateHeight();

    // Return the stopWatchingFrameHeight method bound to this instance
    return () => this.stopWatchingFrameHeight();
  }

  /**
   * Calculate the full height of an element including its margins.
   * @param element The element to calculate height for.
   * @returns The element's scrollHeight plus top and bottom margins.
   */
  protected getElementFullHeight(element: HTMLElement): number {
    const computedStyle = window.getComputedStyle(element);
    const marginTop = parseInt(computedStyle.marginTop, 10) || 0;
    const marginBottom = parseInt(computedStyle.marginBottom, 10) || 0;
    return element.scrollHeight + marginTop + marginBottom;
  }

  /**
   * Stop watching the frame height.
   * Should be called when the component is unmounted via the
   * returned function from `watchFrameHeight`.
   */
  protected stopWatchingFrameHeight(): void {
    if (this.resizeObserver) {
      this.resizeObserver.disconnect();
      this.resizeObserver = undefined;
    }

    if (this.mutationObserver) {
      this.mutationObserver.disconnect();
      this.mutationObserver = undefined;
    }

    // Setting lastFrameHeight to undefined ensures the next setFrameHeight call will always trigger
    this.lastFrameHeight = undefined;

    // Cancel any pending debounced calls
    if (this.debouncedUpdateHeight) {
      this.debouncedUpdateHeight.cancel();
      this.debouncedUpdateHeight = undefined;
    }
  }
}
