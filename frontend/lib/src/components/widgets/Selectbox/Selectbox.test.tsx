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

import {
  act,
  fireEvent,
  screen,
  within,
  waitFor,
} from "@testing-library/react"

import { Selectbox as SelectboxProto } from "@streamlit/protobuf"
import { ElementNode } from "~lib/AppNode"

import { render } from "~lib/test_util"
import { WidgetStateManager } from "~lib/WidgetStateManager"
import ElementNodeRenderer from "~lib/components/core/Block/ElementNodeRenderer"
import { ScriptRunState } from "~lib/ScriptRunState"
import { FlexContextProvider } from "~lib/components/core/Flex/FlexContext"

import Selectbox, { Props } from "./Selectbox"

const getProps = (
  elementProps: Partial<SelectboxProto> = {},
  widgetProps: Partial<Props> = {}
): Props => ({
  element: SelectboxProto.create({
    id: "1",
    label: "Label",
    default: 0,
    options: ["a", "b", "c"],
    ...elementProps,
  }),
  disabled: false,
  widgetMgr: new WidgetStateManager({
    sendRerunBackMsg: vi.fn(),
    formsDataChanged: vi.fn(),
  }),
  ...widgetProps,
})

// Helper to create an ElementNode with a SelectboxProto
const createSelectboxElementNode = (
  selectboxProps: Partial<SelectboxProto> = {}
): ElementNode => {
  const element = SelectboxProto.create({
    id: "selectbox-id",
    label: "Test Label",
    default: 0,
    options: ["a", "b", "c"],
    ...selectboxProps,
  })

  return {
    id: "test-node-id",
    element: {
      type: "selectbox",
      selectbox: element,
      toJSON: () => JSON.stringify({ type: "selectbox", selectbox: element }),
    },
    scriptRunId: "test-run-id",
    reportId: "test-report-id",
    fragmentId: undefined,
    quiverElement: null,
    vegaLiteChartElement: null,
  } as unknown as ElementNode
}

const getElementNodeRendererProps = (elementNode: any): any => ({
  node: elementNode,
  width: "100%",
  widgetMgr: new WidgetStateManager({
    sendRerunBackMsg: vi.fn(),
    formsDataChanged: vi.fn(),
  }),
  scriptRunState: ScriptRunState.RUNNING,
  scriptRunId: "test-run-id",
  widgetsDisabled: false,
  endpoints: {
    buildMediaURL: () => "",
    buildMediaQueryString: () => "",
    buildComponentURL: () => "",
    setStaticConfigUrl: vi.fn(),
    buildAppPageURL: vi.fn().mockReturnValue(""),
    uploadFileUploaderFile: vi
      .fn()
      .mockResolvedValue({ fileId: "test-file-id", fileName: "test.jpg" }),
    fetchCachedForwardMsg: vi.fn().mockResolvedValue({}),
  },
  uploadClient: {} as any,
  formsData: {
    submitReportId: "",
    formsWithUploads: new Set<string>(),
    formsWithPendingChanges: new Set<string>(),
    submitButtons: new Map<string, any>(),
  },
  disableFullscreenMode: false,
  componentRegistry: {} as any,
})

const pickOption = (selectbox: HTMLElement, value: string): void => {
  // TODO: Utilize user-event instead of fireEvent
  // eslint-disable-next-line testing-library/prefer-user-event
  fireEvent.click(selectbox)
  const valueElement = screen.getByText(value)
  // TODO: Utilize user-event instead of fireEvent
  // eslint-disable-next-line testing-library/prefer-user-event
  fireEvent.click(valueElement)
}

describe("Selectbox widget", () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it("renders without crashing", () => {
    const props = getProps()
    render(<Selectbox {...props} />)
    const selectbox = screen.getByTestId("stSelectbox")
    expect(selectbox).toBeInTheDocument()
    expect(selectbox).toHaveClass("stSelectbox")
  })

  it("sets widget value on mount", () => {
    const props = getProps()
    vi.spyOn(props.widgetMgr, "setStringValue")

    render(<Selectbox {...props} />)
    expect(props.widgetMgr.setStringValue).toHaveBeenCalledWith(
      props.element,
      props.element.options[props.element.default ?? 0],
      { fromUi: false },
      undefined
    )
  })

  it("gets correct value from proto", () => {
    const props = getProps({
      rawValue: "c",
      setValue: true,
    })
    render(<Selectbox {...props} />)

    const selectbox = screen.getByTestId("stSelectbox")
    expect(within(selectbox).getByText("c")).toBeVisible()
  })

  it("can pass fragmentId to setStringValue", () => {
    const props = getProps(undefined, { fragmentId: "myFragmentId" })
    vi.spyOn(props.widgetMgr, "setStringValue")

    render(<Selectbox {...props} />)
    expect(props.widgetMgr.setStringValue).toHaveBeenCalledWith(
      props.element,
      props.element.options[props.element.default ?? 0],
      { fromUi: false },
      "myFragmentId"
    )
  })

  it("handles the onChange event", () => {
    const props = getProps()
    vi.spyOn(props.widgetMgr, "setStringValue")
    vi.spyOn(Utils, "convertRemToPx").mockImplementation(mockConvertRemToPx)

    render(<Selectbox {...props} />)

    const selectbox = screen.getByRole("combobox")

    pickOption(selectbox, "b")

    expect(props.widgetMgr.setStringValue).toHaveBeenLastCalledWith(
      props.element,
      "b",
      { fromUi: true },
      undefined
    )
    expect(screen.queryByText("a")).not.toBeInTheDocument()
    expect(screen.getByText("b")).toBeInTheDocument()
  })

  it("resets its value when form is cleared", () => {
    // Create a widget in a clearOnSubmit form
    const props = getProps({ formId: "form" })
    props.widgetMgr.setFormSubmitBehaviors("form", true)

    vi.spyOn(props.widgetMgr, "setStringValue")
    vi.spyOn(Utils, "convertRemToPx").mockImplementation(mockConvertRemToPx)

    render(<Selectbox {...props} />)

    const selectbox = screen.getByRole("combobox")
    pickOption(selectbox, "b")

    expect(props.widgetMgr.setStringValue).toHaveBeenLastCalledWith(
      props.element,
      "b",
      { fromUi: true },
      undefined
    )

    // "Submit" the form
    act(() => {
      props.widgetMgr.submitForm("form", undefined)
    })

    // Our widget should be reset, and the widgetMgr should be updated
    expect(screen.getByText("a")).toBeInTheDocument()
    expect(screen.queryByText("b")).not.toBeInTheDocument()
    expect(props.widgetMgr.setStringValue).toHaveBeenLastCalledWith(
      props.element,
      props.element.options[props.element.default ?? 0],
      {
        fromUi: true,
      },
      undefined
    )
  })

  it("renders a placeholder with null default", () => {
    const props = getProps({
      placeholder: "Please select an option...",
      default: null,
    })
    render(<Selectbox {...props} />)

    expect(screen.getByText("Please select an option...")).toBeInTheDocument()
  })

  describe("width and scale parameters", () => {
    beforeEach(() => {
      // Setup any test requirements if needed
      // For testing styles, we don't need special mocks -
      // the testing-library's toHaveStyle helper will work with the DOM directly
    })

    it("renders with width='stretch' as expected", async () => {
      // Using ElementNodeRenderer to test the complete pipeline
      const elementNode = createSelectboxElementNode({
        width: "stretch",
        scale: 2,
      })

      // Wrap in FlexContextProvider with row direction to simulate horizontal container
      render(
        <FlexContextProvider direction="row" parentContainerDirection="row">
          <ElementNodeRenderer {...getElementNodeRendererProps(elementNode)} />
        </FlexContextProvider>
      )

      // Wait for the actual selectbox to render
      await waitFor(() => {
        within(screen.getByTestId("stElementContainer")).getByTestId(
          "stSelectbox"
        )
      })

      // Find the container element which should have the width style
      const elementContainer = screen.getByTestId("stElementContainer")

      expect(elementContainer).toHaveStyle("width: 100%")
      expect(elementContainer).toHaveStyle("flex-grow: 2")
    })

    it("renders with a fixed pixel width as expected", async () => {
      // Test with ElementNodeRenderer
      const elementNode = createSelectboxElementNode({ width: "200" })

      // Wrap in FlexContextProvider with row direction to simulate horizontal container
      render(
        <FlexContextProvider direction="row" parentContainerDirection="row">
          <ElementNodeRenderer {...getElementNodeRendererProps(elementNode)} />
        </FlexContextProvider>
      )

      // Wait for the actual selectbox to render
      await waitFor(() => {
        within(screen.getByTestId("stElementContainer")).getByTestId(
          "stSelectbox"
        )
      })

      // Find the container element which should have the width style
      const elementContainer = screen.getByTestId("stElementContainer")

      // Based on useLayoutStyles, a numeric width gets converted to "{width}px"
      expect(elementContainer).toHaveStyle("width: 200px")
    })
  })
})
