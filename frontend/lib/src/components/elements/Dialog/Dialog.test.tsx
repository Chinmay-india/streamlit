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

import React from "react"

import { screen } from "@testing-library/react"
import { userEvent } from "@testing-library/user-event"

import { Block as BlockProto } from "@streamlit/protobuf"

import { render } from "~lib/test_util"

import Dialog, { Props as DialogProps } from "./Dialog"

const getProps = (
  elementProps: Partial<BlockProto.Dialog> = {},
  props: Partial<DialogProps> = {}
): DialogProps => ({
  element: BlockProto.Dialog.create({
    title: "StreamlitDialog",
    isOpen: true,
    dismissible: true,
    ...elementProps,
  }),
  ...props,
})

describe("Dialog container", () => {
  it("renders without crashing", () => {
    const props = getProps()
    render(
      <Dialog {...props}>
        <div>test</div>
      </Dialog>
    )

    const dialogContainer = screen.getByTestId("stDialog")
    expect(dialogContainer).toBeInTheDocument()
    expect(dialogContainer).toHaveClass("stDialog")
  })

  it("should render the text when open", () => {
    const props = getProps()
    render(
      <Dialog {...props}>
        <div>test</div>
      </Dialog>
    )

    expect(screen.getByText("test")).toBeVisible()
  })

  it("should not render the text when closed", () => {
    const props = getProps({ isOpen: false })
    render(
      <Dialog {...props}>
        <div>test</div>
      </Dialog>
    )

    expect(screen.queryByText("test")).not.toBeInTheDocument()
  })

  it("should close when dismissible", async () => {
    const user = userEvent.setup()
    const props = getProps()
    render(
      <Dialog {...props}>
        <div>test</div>
      </Dialog>
    )

    expect(screen.getByText("test")).toBeVisible()
    await user.click(screen.getByLabelText("Close"))
    // dialog should be closed by clicking outside and, thus, the content should be gone
    expect(screen.queryByText("test")).not.toBeInTheDocument()
  })

  it("should not close when not dismissible", () => {
    const props = getProps({ dismissible: false })
    render(
      <Dialog {...props}>
        <div>test</div>
      </Dialog>
    )

    expect(screen.getByText("test")).toBeVisible()
    // close button - and hence dismiss - does not exist
    expect(screen.queryByLabelText("Close")).not.toBeInTheDocument()
  })

  it("should reset internal state when initialIsOpen changes", async () => {
    const user = userEvent.setup()

    // Initial render with dialog open
    const initialProps = getProps({ isOpen: true })
    const { rerender } = render(
      <Dialog {...initialProps}>
        <div>test content</div>
      </Dialog>
    )

    // Close the dialog by clicking the close button
    expect(screen.getByText("test content")).toBeVisible()
    await user.click(screen.getByLabelText("Close"))
    expect(screen.queryByText("test content")).not.toBeInTheDocument()

    // Change initialIsOpen prop to true again, which should reset the internal state
    const updatedProps = getProps({ isOpen: false })
    rerender(
      <Dialog {...updatedProps}>
        <div>test content</div>
      </Dialog>
    )

    // Dialog should remain closed as the new initialIsOpen is false
    expect(screen.queryByText("test content")).not.toBeInTheDocument()

    // Change initialIsOpen back to true, which should open the dialog again
    const reopenProps = getProps({ isOpen: true })
    rerender(
      <Dialog {...reopenProps}>
        <div>test content</div>
      </Dialog>
    )

    // Dialog should be open again
    expect(screen.getByText("test content")).toBeVisible()
  })

  it("should reset internal state when deltaMsgReceivedAt changes", async () => {
    const user = userEvent.setup()

    // Initial render with dialog open and a timestamp
    const initialProps = getProps(
      { isOpen: true },
      { deltaMsgReceivedAt: 1000 }
    )
    const { rerender } = render(
      <Dialog {...initialProps}>
        <div>test content</div>
      </Dialog>
    )

    // Close the dialog by clicking the close button
    expect(screen.getByText("test content")).toBeVisible()
    await user.click(screen.getByLabelText("Close"))
    expect(screen.queryByText("test content")).not.toBeInTheDocument()

    // Change deltaMsgReceivedAt prop, which should reset the internal state
    const updatedProps = getProps(
      { isOpen: true },
      { deltaMsgReceivedAt: 2000 }
    )
    rerender(
      <Dialog {...updatedProps}>
        <div>test content</div>
      </Dialog>
    )

    // Dialog should be open again because initialIsOpen is true and the key changed
    expect(screen.getByText("test content")).toBeVisible()
  })

  it("should reset internal state when both initialIsOpen and deltaMsgReceivedAt change", async () => {
    const user = userEvent.setup()

    // Initial render with dialog open and a timestamp
    const initialProps = getProps(
      { isOpen: true },
      { deltaMsgReceivedAt: 1000 }
    )
    const { rerender } = render(
      <Dialog {...initialProps}>
        <div>test content</div>
      </Dialog>
    )

    // Close the dialog by clicking the close button
    expect(screen.getByText("test content")).toBeVisible()
    await user.click(screen.getByLabelText("Close"))
    expect(screen.queryByText("test content")).not.toBeInTheDocument()

    // Change both initialIsOpen and deltaMsgReceivedAt props
    const updatedProps = getProps(
      { isOpen: false },
      { deltaMsgReceivedAt: 2000 }
    )
    rerender(
      <Dialog {...updatedProps}>
        <div>test content</div>
      </Dialog>
    )

    // Dialog should remain closed as the new initialIsOpen is false
    expect(screen.queryByText("test content")).not.toBeInTheDocument()

    // Change both props again, with initialIsOpen now true
    const reopenProps = getProps(
      { isOpen: true },
      { deltaMsgReceivedAt: 3000 }
    )
    rerender(
      <Dialog {...reopenProps}>
        <div>test content</div>
      </Dialog>
    )

    // Dialog should be open again
    expect(screen.getByText("test content")).toBeVisible()
  })

  it("should not show dialog when deltaMsgReceivedAt changes but initialIsOpen is false", async () => {
    // Initial render with dialog closed and a timestamp
    const initialProps = getProps(
      { isOpen: false },
      { deltaMsgReceivedAt: 1000 }
    )
    const { rerender } = render(
      <Dialog {...initialProps}>
        <div>test content</div>
      </Dialog>
    )

    // Dialog should be closed
    expect(screen.queryByText("test content")).not.toBeInTheDocument()

    // Change deltaMsgReceivedAt prop, but keep initialIsOpen as false
    const updatedProps = getProps(
      { isOpen: false },
      { deltaMsgReceivedAt: 2000 }
    )
    rerender(
      <Dialog {...updatedProps}>
        <div>test content</div>
      </Dialog>
    )

    // Dialog should still be closed
    expect(screen.queryByText("test content")).not.toBeInTheDocument()
  })

  it("should handle when deltaMsgReceivedAt changes from undefined to defined", async () => {
    const user = userEvent.setup()

    // Initial render with dialog open and no timestamp
    const initialProps = getProps({ isOpen: true })
    const { rerender } = render(
      <Dialog {...initialProps}>
        <div>test content</div>
      </Dialog>
    )

    // Close the dialog by clicking the close button
    expect(screen.getByText("test content")).toBeVisible()
    await user.click(screen.getByLabelText("Close"))
    expect(screen.queryByText("test content")).not.toBeInTheDocument()

    // Add deltaMsgReceivedAt prop, which should reset the internal state
    const updatedProps = getProps(
      { isOpen: true },
      { deltaMsgReceivedAt: 1000 }
    )
    rerender(
      <Dialog {...updatedProps}>
        <div>test content</div>
      </Dialog>
    )

    // Dialog should be open again
    expect(screen.getByText("test content")).toBeVisible()
  })
})
