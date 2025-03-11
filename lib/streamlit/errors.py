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

import os
from typing import Any, Literal

from streamlit import util


class Error(Exception):
    """The base class for all exceptions thrown by Streamlit.

    Should be used for exceptions raised due to user errors (typically via
    StreamlitAPIException) as well as exceptions raised by Streamlit's internal
    code.
    """

    pass


class CustomComponentError(Error):
    """Exceptions thrown in the custom components code path."""

    pass


class DeprecationError(Error):
    pass


class FragmentStorageKeyError(Error, KeyError):
    """A KeyError raised when a KeyError is encountered during a FragmentStorage
    operation."""

    pass


class FragmentHandledException(Exception):
    """An exception that is raised by the fragment
    when it has handled the exception itself.
    """

    pass


class NoStaticFiles(Error):
    pass


class NoSessionContext(Error):
    pass


class MarkdownFormattedException(Error):
    """Exceptions with Markdown in their description.

    Instances of this class can use markdown in their messages, which will get
    nicely formatted on the frontend.
    """

    pass


class StreamlitAPIException(MarkdownFormattedException):
    """Base class for Streamlit API exceptions.

    An API exception should be thrown when user code interacts with the
    Streamlit API incorrectly. (That is, when we throw an exception as a
    result of a user's malformed `st.foo` call, it should be a
    StreamlitAPIException or subclass.)

    When displaying these exceptions on the frontend, we strip Streamlit
    entries from the stack trace so that the user doesn't see a bunch of
    noise related to Streamlit internals.

    """

    def __repr__(self) -> str:
        return util.repr_(self)


class DuplicateWidgetID(StreamlitAPIException):
    pass


class StreamlitAuthError(StreamlitAPIException):
    pass


class StreamlitDuplicateElementId(DuplicateWidgetID):
    """An exception raised when the auto-generated ID of an element is not unique."""

    def __init__(self, element_type: str):
        super().__init__(
            f"There are multiple `{element_type}` elements with the same "
            "auto-generated ID. When this element is created, it is assigned an "
            "internal ID based on the element type and provided parameters. Multiple "
            "elements with the same type and parameters will cause this error.\n\n"
            "To fix this error, please pass a unique `key` argument to the "
            f"`{element_type}` element."
        )


class StreamlitDuplicateElementKey(DuplicateWidgetID):
    """An exception raised when the key of an element is not unique."""

    def __init__(self, user_key: str):
        super().__init__(
            f"There are multiple elements with the same `key='{user_key}'`. "
            "To fix this, please make sure that the `key` argument is unique for "
            "each element you create."
        )


class UnserializableSessionStateError(StreamlitAPIException):
    pass


class StreamlitAPIWarning(StreamlitAPIException, Warning):
    """Used to display a warning.

    Note that this should not be "raised", but passed to st.exception
    instead.
    """

    def __init__(self, *args):
        super().__init__(*args)
        import inspect
        import traceback

        f = inspect.currentframe()
        self.tacked_on_stack = traceback.extract_stack(f)

    def __repr__(self) -> str:
        return util.repr_(self)


class StreamlitModuleNotFoundError(StreamlitAPIWarning):
    """Print a pretty message when a Streamlit command requires a dependency
    that is not one of our core dependencies."""

    def __init__(self, module_name, *args):
        message = (
            f'This Streamlit command requires module "{module_name}" to be installed.'
        )
        super().__init__(message, *args)


class LocalizableStreamlitException(StreamlitAPIException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message.format(**kwargs))
        self._exec_kwargs = kwargs

    @property
    def exec_kwargs(self) -> dict[str, Any]:
        return self._exec_kwargs


# st.set_page_config
class StreamlitSetPageConfigMustBeFirstCommandError(LocalizableStreamlitException):
    """Exception raised when the set_page_config command is not the first executed streamlit command."""

    def __init__(self):
        super().__init__(
            "`set_page_config()` can only be called once per app page, "
            "and must be called as the first Streamlit command in your script.\n\n"
            "For more information refer to the [docs]"
            "(https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config)."
        )


class StreamlitInvalidPageLayoutError(LocalizableStreamlitException):
    """Exception raised when an invalid value is specified for layout."""

    def __init__(self, layout: str):
        super().__init__(
            '`layout` must be `"centered"` or `"wide"` (got `"{layout}"`)',
            layout=layout,
        )


class StreamlitInvalidSidebarStateError(LocalizableStreamlitException):
    """Exception raised when an invalid value is specified for `initial_sidebar_state`."""

    def __init__(self, initial_sidebar_state: str):
        super().__init__(
            '`initial_sidebar_state` must be `"auto"` or `"expanded"` or `"collapsed"` (got `"{initial_sidebar_state}"`)',
            initial_sidebar_state=initial_sidebar_state,
        )


class StreamlitInvalidMenuItemKeyError(LocalizableStreamlitException):
    """Exception raised when an invalid key is specified."""

    def __init__(self, key: str):
        super().__init__(
            'We only accept the keys: `"Get help"`, `"Report a bug"`, and `"About"` (`"{key}"` is not a valid key.)',
            key=key,
        )


class StreamlitInvalidURLError(LocalizableStreamlitException):
    """Exception raised when an invalid URL is specified for any of the menu items except for "About"."""

    def __init__(self, url: str):
        super().__init__(
            '"{url}" is a not a valid URL. '
            'You must use a fully qualified domain beginning with "http://", "https://", or "mailto:".',
            url=url,
        )


# st.columns
class StreamlitInvalidColumnSpecError(LocalizableStreamlitException):
    """Exception raised when no weights are specified, or a negative weight is specified."""

    def __init__(self):
        super().__init__(
            "The `spec` argument to `st.columns` must be either a "
            "positive integer (number of columns) or a list of positive numbers (width ratios of the columns). "
            "See [documentation](https://docs.streamlit.io/develop/api-reference/layout/st.columns) "
            "for more information."
        )


class StreamlitInvalidVerticalAlignmentError(LocalizableStreamlitException):
    """Exception raised when an invalid value is specified for vertical_alignment."""

    def __init__(self, vertical_alignment: str):
        super().__init__(
            'The `vertical_alignment` argument to `st.columns` must be `"top"`, `"center"`, or `"bottom"`. \n'
            "The argument passed was {vertical_alignment}.",
            vertical_alignment=vertical_alignment,
        )


class StreamlitInvalidColumnGapError(LocalizableStreamlitException):
    """Exception raised when an invalid value is specified for gap."""

    def __init__(self, gap: str):
        super().__init__(
            'The `gap` argument to `st.columns` must be `"small"`, `"medium"`, or `"large"`. \n'
            "The argument passed was {gap}.",
            gap=gap,
        )


# st.multiselect
class StreamlitSelectionCountExceedsMaxError(LocalizableStreamlitException):
    """Exception raised when there are more default selections specified than the max allowable selections."""

    def __init__(self, current_selections_count: int, max_selections_count: int):
        super().__init__(
            "Multiselect has {current_selections_count} {current_selections_noun} "
            "selected but `max_selections` is set to {max_selections_count}. "
            "This happened because you either gave too many options to `default` "
            "or you manipulated the widget's state through `st.session_state`. "
            "Note that the latter can happen before the line indicated in the traceback. "
            "Please select at most {max_selections_count} {options_noun}.",
            current_selections_count=current_selections_count,
            current_selections_noun="option"
            if current_selections_count == 1
            else "options",
            max_selections_count=max_selections_count,
            options_noun="option" if max_selections_count == 1 else "options",
        )


# st.number_input
class StreamlitMixedNumericTypesError(LocalizableStreamlitException):
    """Exception raised mixing floats and ints in st.number_input."""

    def __init__(
        self,
        value: int | float | Literal["min"] | None,
        min_value: int | float | None,
        max_value: int | float | None,
        step: int | float | None,
    ):
        value_type = None
        min_value_type = None
        max_value_type = None
        step_type = None

        error_message = "All numerical arguments must be of the same type."

        if value:
            value_type = type(value).__name__
            error_message += "\n`value` has {value_type} type."

        if min_value:
            min_value_type = type(min_value).__name__
            error_message += "\n`min_value` has {min_value_type} type."

        if max_value:
            max_value_type = type(max_value).__name__
            error_message += "\n`max_value` has {max_value_type} type."

        if step:
            step_type = type(step).__name__
            error_message += "\n`step` has {step_type} type."

        super().__init__(
            error_message,
            value_type=value_type,
            min_value_type=min_value_type,
            max_value_type=max_value_type,
            step_type=step_type,
        )


class StreamlitValueBelowMinError(LocalizableStreamlitException):
    """Exception raised when the `min_value` is greater than the `value`."""

    def __init__(self, value: int | float, min_value: int | float):
        super().__init__(
            "The `value` {value} is less than the `min_value` {min_value}.",
            value=value,
            min_value=min_value,
        )


class StreamlitValueAboveMaxError(LocalizableStreamlitException):
    """Exception raised when the `max_value` is less than the `value`."""

    def __init__(self, value: int | float, max_value: int | float):
        super().__init__(
            "The `value` {value} is greater than the `max_value` {max_value}.",
            value=value,
            max_value=max_value,
        )


class StreamlitJSNumberBoundsError(LocalizableStreamlitException):
    """Exception raised when a number exceeds the Javascript limits."""

    def __init__(self, message: str):
        super().__init__(message)


class StreamlitInvalidNumberFormatError(LocalizableStreamlitException):
    """Exception raised when the format string for `st.number_input` contains
    invalid characters.
    """

    def __init__(self, format: str):
        super().__init__(
            "Format string for `st.number_input` contains invalid characters: {format}",
            format=format,
        )


# st.page_link
class StreamlitMissingPageLabelError(LocalizableStreamlitException):
    """Exception raised when a page_link is created without a label."""

    def __init__(self):
        super().__init__(
            "The `label` param is required for external links used with `st.page_link` - please provide a `label`."
        )


class StreamlitPageNotFoundError(LocalizableStreamlitException):
    """Exception raised the linked page can not be found."""

    def __init__(
        self, page: str, main_script_directory: str, uses_pages_directory: bool
    ):
        directory = os.path.basename(main_script_directory)

        message = (
            "Could not find page: `{page}`. You must provide a `StreamlitPage` "
            "object or file path relative to the entrypoint file. Only pages "
            "previously defined by `st.Page` and passed to `st.navigation` are "
            "allowed."
        )

        if uses_pages_directory:
            message = (
                "Could not find page: `{page}`. You must provide a file path "
                "relative to the entrypoint file (from the directory `{directory}`). "
                "Only the entrypoint file and files in the `pages/` directory are supported."
            )

        super().__init__(
            message,
            page=page,
            directory=directory,
        )


# policies
class StreamlitFragmentWidgetsNotAllowedOutsideError(LocalizableStreamlitException):
    """Exception raised when the fragment attempts to write to an element outside of its container."""

    def __init__(self):
        super().__init__("Fragments cannot write widgets to outside containers.")


class StreamlitInvalidFormCallbackError(LocalizableStreamlitException):
    """Exception raised a `on_change` callback is set on any element in a form except for the `st.form_submit_button`."""

    def __init__(self):
        super().__init__(
            "Within a form, callbacks can only be defined on `st.form_submit_button`. "
            "Defining callbacks on other widgets inside a form is not allowed."
        )


class StreamlitValueAssignmentNotAllowedError(LocalizableStreamlitException):
    """Exception raised when trying to set values where writes are not allowed."""

    def __init__(self, key: str):
        super().__init__(
            "Values for the widget with `key` '{key}' cannot be set using `st.session_state`.",
            key=key,
        )


class StreamlitInvalidColorError(LocalizableStreamlitException):
    def __init__(self, color):
        super().__init__(
            "This does not look like a valid color: {color}.\n\n"
            "Colors must be in one of the following formats:"
            "* Hex string with 3, 4, 6, or 8 digits. Example: `'#00ff00'`"
            "* List or tuple with 3 or 4 components. Example: `[1.0, 0.5, 0, 0.2]`",
            color=repr(color),
        )


class StreamlitBadTimeStringError(LocalizableStreamlitException):
    """Exception Raised when a time string argument is passed that cannot be parsed."""

    def __init__(self, time_string: str):
        super().__init__(
            "Time string doesn't look right. It should be formatted as"
            "`'1d2h34m'` or `2 days`, for example. Got: {time_string}",
            time_string=time_string,
        )


# New error classes for layouts
class StreamlitMissingLabelError(LocalizableStreamlitException):
    """Exception raised when a UI element that requires a label is created without one."""

    def __init__(self, element_type: str):
        super().__init__(
            "A label is required for a {element_type}",
            element_type=element_type,
        )


# New error class for media elements
class StreamlitInvalidTimeRangeError(LocalizableStreamlitException):
    """Exception raised when invalid start_time and end_time are provided for media elements."""

    def __init__(self, start_time: float, end_time: float | None):
        message = "Invalid start_time and end_time combination."
        if start_time < 0:
            message = "The `start_time` {start_time} must be non-negative."
        elif end_time is not None and end_time <= start_time:
            message = "The `end_time` {end_time} must be greater than the `start_time` {start_time}."

        super().__init__(
            message,
            start_time=start_time,
            end_time=end_time,
        )


# New error class for conflicting parameters
class StreamlitConflictingParametersError(LocalizableStreamlitException):
    """Exception raised when conflicting parameters are provided."""

    def __init__(self, param1: str, param2: str, recommendation: str | None = None):
        message = (
            "The parameters `{param1}` and `{param2}` cannot be set at the same time."
        )
        if recommendation:
            message += " {recommendation}"

        super().__init__(
            message,
            param1=param1,
            param2=param2,
            recommendation=recommendation,
        )


# New error class for numpy array shape validation
class StreamlitInvalidNumpyShapeError(LocalizableStreamlitException):
    """Exception raised when a numpy array has an invalid shape."""

    def __init__(self, expected_dims: str, actual_dims: int | None = None):
        message = "Numpy array {expected_dims}"
        if actual_dims is not None:
            message = "Numpy array must have {expected_dims}, but got {actual_dims} dimensions."

        super().__init__(
            message,
            expected_dims=expected_dims,
            actual_dims=actual_dims,
        )


# New error class for missing required parameters
class StreamlitMissingRequiredParameterError(LocalizableStreamlitException):
    """Exception raised when a required parameter is missing."""

    def __init__(self, param_name: str, context: str | None = None):
        message = "Missing required parameter: `{param_name}`"
        if context:
            message += " for {context}"

        super().__init__(
            message,
            param_name=param_name,
            context=context,
        )


# New error class for empty options
class StreamlitEmptyOptionsError(LocalizableStreamlitException):
    """Exception raised when an options list is empty."""

    def __init__(self, widget_type: str):
        super().__init__(
            "The `options` argument for `{widget_type}` needs to be non-empty",
            widget_type=widget_type,
        )


# New error class for user info modification
class StreamlitUserInfoModificationError(LocalizableStreamlitException):
    """Exception raised when attempting to modify user info."""

    def __init__(self):
        super().__init__("st.experimental_user cannot be modified")


# New error classes for progress bars
class StreamlitInvalidProgressValueError(LocalizableStreamlitException):
    """Exception raised when an invalid progress value is provided."""

    def __init__(self, value: int | float, expected_range: str):
        super().__init__(
            "Progress Value has invalid value {expected_range}: {value}",
            value=value,
            expected_range=expected_range,
        )


class StreamlitInvalidProgressTypeError(LocalizableStreamlitException):
    """Exception raised when a progress value has an invalid type."""

    def __init__(self, type_name: str):
        super().__init__(
            "Progress Value has invalid type: {type_name}",
            type_name=type_name,
        )


class StreamlitInvalidProgressTextTypeError(LocalizableStreamlitException):
    """Exception raised when a progress text has an invalid type."""

    def __init__(self, type_name: str):
        super().__init__(
            "Progress Text is of type {type_name}, which is not an accepted type. "
            "Text only accepts: str. Please convert the text to an accepted type.",
            type_name=type_name,
        )


# New error class for toast
class StreamlitEmptyToastError(LocalizableStreamlitException):
    """Exception raised when a toast is created with an empty message."""

    def __init__(self):
        super().__init__("Toast body cannot be blank - please provide a message.")


# New error class for date manipulation
class StreamlitInvalidDateError(LocalizableStreamlitException):
    """Exception raised when a date manipulation results in an invalid date."""

    def __init__(self, input_date: str, target_year: int):
        super().__init__(
            "Date {input_date} does not exist in the target year {target_year}. "
            "This should never happen. Please report this bug.",
            input_date=input_date,
            target_year=target_year,
        )


# New error classes for database connections
class StreamlitMissingConnectionConfigError(LocalizableStreamlitException):
    """Exception raised when a connection configuration is missing."""

    def __init__(self, connection_type: str, config_locations: str):
        super().__init__(
            "Missing {connection_type} connection configuration. "
            "Did you forget to set this in {config_locations}?",
            connection_type=connection_type,
            config_locations=config_locations,
        )


class StreamlitMissingConnectionParamError(LocalizableStreamlitException):
    """Exception raised when a required connection parameter is missing."""

    def __init__(self, connection_type: str, param_name: str):
        super().__init__(
            "Missing {connection_type} connection param: {param_name}",
            connection_type=connection_type,
            param_name=param_name,
        )


# New error class for file uploader
class StreamlitInvalidFileExtensionError(LocalizableStreamlitException):
    """Exception raised when a file with an invalid extension is uploaded."""

    def __init__(self, extension: str, allowed_types: list[str] | None):
        super().__init__(
            "Invalid file extension: `{extension}`. Allowed: {allowed_types}",
            extension=extension,
            allowed_types=allowed_types,
        )


# New error classes for buttons
class StreamlitInvalidButtonTypeError(LocalizableStreamlitException):
    """Exception raised when an invalid button type is provided."""

    def __init__(self, button_name: str, type_value: str):
        super().__init__(
            'The type argument to {button_name} must be "primary", "secondary", or "tertiary". '
            '\nThe argument passed was "{type_value}".',
            button_name=button_name,
            type_value=type_value,
        )


class StreamlitButtonInFormError(LocalizableStreamlitException):
    """Exception raised when a button is used incorrectly with forms."""

    def __init__(self, button_name: str, in_form: bool):
        message = "`{button_name}` can't be used in an `st.form()`."
        if not in_form:
            message = "`{button_name}` must be used inside an `st.form()`."

        super().__init__(
            message
            + " For more information, refer to https://docs.streamlit.io/library/api-reference/control-flow/st.form",
            button_name=button_name,
            in_form=in_form,
        )


# New error classes for chat widgets
class StreamlitInvalidAvatarError(LocalizableStreamlitException):
    """Exception raised when an invalid avatar is provided for a chat message."""

    def __init__(self):
        super().__init__("Failed to load the provided avatar value as an image.")


class StreamlitMissingChatAuthorError(LocalizableStreamlitException):
    """Exception raised when a chat message is created without an author name."""

    def __init__(self):
        super().__init__(
            "The author name is required for a chat message, please set it via the parameter `name`."
        )


class StreamlitInvalidChatFileOptionError(LocalizableStreamlitException):
    """Exception raised when an invalid accept_file option is provided for chat input."""

    def __init__(self):
        super().__init__("The `accept_file` parameter must be a boolean or 'multiple'.")


class StreamlitChatInputInFormError(LocalizableStreamlitException):
    """Exception raised when a chat input is used inside a form."""

    def __init__(self):
        super().__init__("`st.chat_input()` can't be used in a `st.form()`.")


# New error class for color picker
class StreamlitInvalidColorFormatError(LocalizableStreamlitException):
    """Exception raised when an invalid color format is provided."""

    def __init__(self, value: str | None, is_type_error: bool = False):
        if is_type_error:
            message = "Color Picker Value has invalid type: {value_type}. Expects a hex string like '#00FFAA' or '#000'."
            super().__init__(
                message,
                value_type=value,
            )
        else:
            message = "'{value}' is not a valid hex code for colors. Valid ones are like '#00FFAA' or '#000'."
            super().__init__(
                message,
                value=value,
            )


# New error classes for time widgets
class StreamlitInvalidTimeValueTypeError(LocalizableStreamlitException):
    """Exception raised when an invalid time value type is provided."""

    def __init__(self):
        super().__init__(
            "The type of value should be one of datetime, time, ISO string or None"
        )


class StreamlitInvalidDateValueTypeError(LocalizableStreamlitException):
    """Exception raised when an invalid date value type is provided."""

    def __init__(self):
        super().__init__(
            'Date value should either be an date/datetime or an ISO string or "today"'
        )


class StreamlitInvalidDateRangeError(LocalizableStreamlitException):
    """Exception raised when an invalid date range is provided."""

    def __init__(self):
        super().__init__(
            "DateInput value should either be an date/datetime or a list/tuple of "
            "0 - 2 date/datetime values"
        )


class StreamlitInvalidMinDateTypeError(LocalizableStreamlitException):
    """Exception raised when an invalid min date type is provided."""

    def __init__(self):
        super().__init__("DateInput min should either be a date/datetime or None")


class StreamlitInvalidMaxDateTypeError(LocalizableStreamlitException):
    """Exception raised when an invalid max date type is provided."""

    def __init__(self):
        super().__init__("DateInput max should either be a date/datetime or None")


class StreamlitMinDateGreaterThanMaxError(LocalizableStreamlitException):
    """Exception raised when min_value is greater than max_value for date input."""

    def __init__(self, min_value: str, max_value: str):
        super().__init__(
            "The `min_value`, set to {min_value}, shouldn't be larger "
            "than the `max_value`, set to {max_value}.",
            min_value=min_value,
            max_value=max_value,
        )


class StreamlitDateOutOfRangeError(LocalizableStreamlitException):
    """Exception raised when a date value is outside the min/max range."""

    def __init__(self, value: str, min_value: str, max_value: str):
        super().__init__(
            "The default `value` of {value} "
            "must lie between the `min_value` of {min_value} "
            "and the `max_value` of {max_value}, inclusively.",
            value=value,
            min_value=min_value,
            max_value=max_value,
        )


class StreamlitInvalidTimeStepTypeError(LocalizableStreamlitException):
    """Exception raised when an invalid time step type is provided."""

    def __init__(self, step_type: str):
        super().__init__(
            "`step` can only be `int` or `timedelta` but {step_type} is provided.",
            step_type=step_type,
        )


class StreamlitInvalidTimeStepRangeError(LocalizableStreamlitException):
    """Exception raised when a time step is outside the valid range."""

    def __init__(self, step_seconds: int):
        super().__init__(
            "`step` must be between 60 seconds and 23 hours but is currently set to {step_seconds} seconds.",
            step_seconds=step_seconds,
        )


class StreamlitInvalidDateFormatError(LocalizableStreamlitException):
    """Exception raised when an invalid date format is provided."""

    def __init__(self, format: str):
        super().__init__(
            "The provided format (`{format}`) is not valid. DateInput format "
            "should be one of `YYYY/MM/DD`, `DD/MM/YYYY`, or `MM/DD/YYYY` "
            "and can also use a period (.) or hyphen (-) as separators.",
            format=format,
        )


# New error classes for data editor
class StreamlitDuplicateColumnNamesError(LocalizableStreamlitException):
    """Exception raised when duplicate column names are found in a dataframe."""

    def __init__(self, duplicated_columns: list[str]):
        super().__init__(
            "All column names are required to be unique for usage with data editor. "
            "The following column names are duplicated: {duplicated_columns}. "
            "Please rename the duplicated columns in the provided data.",
            duplicated_columns=duplicated_columns,
        )


class StreamlitReservedColumnNameError(LocalizableStreamlitException):
    """Exception raised when a reserved column name is used in a dataframe."""

    def __init__(self, column_name: str):
        super().__init__(
            "The column name '{column_name}' is reserved for the index column "
            "and cannot be used as a column name in the provided data.",
            column_name=column_name,
        )


class StreamlitIncompatibleColumnTypeError(LocalizableStreamlitException):
    """Exception raised when an incompatible column type is configured."""

    def __init__(self, column_name: str, configured_type: str, data_type: str):
        super().__init__(
            "The configured column type `{configured_type}` for column "
            "`{column_name}` is not compatible for editing the underlying "
            "data type `{data_type}`.\n\nYou have following options to "
            "fix this: 1) choose a compatible type 2) disable the column "
            "3) convert the column into a compatible data type.",
            column_name=column_name,
            configured_type=configured_type,
            data_type=data_type,
        )


class StreamlitUnsupportedDataTypeError(LocalizableStreamlitException):
    """Exception raised when an unsupported data type is provided to the data editor."""

    def __init__(self, data_type: str):
        super().__init__(
            "The data type ({data_type}) or format is not supported by "
            "the data editor. Please convert your data into a Pandas Dataframe or "
            "another supported data format.",
            data_type=data_type,
        )


class StreamlitUnsupportedIndexTypeError(LocalizableStreamlitException):
    """Exception raised when an unsupported index type is provided to the data editor."""

    def __init__(self, index_type: str):
        super().__init__(
            "The type of the dataframe index - {index_type} - is not "
            "yet supported by the data editor.",
            index_type=index_type,
        )


# New error classes for radio buttons
class StreamlitInvalidRadioIndexTypeError(LocalizableStreamlitException):
    """Exception raised when an invalid radio index type is provided."""

    def __init__(self, index_type: str):
        super().__init__(
            "Radio Value has invalid type: {index_type}",
            index_type=index_type,
        )


class StreamlitRadioIndexOutOfRangeError(LocalizableStreamlitException):
    """Exception raised when a radio index is out of range."""

    def __init__(self):
        super().__init__("Radio index must be between 0 and length of options")


class StreamlitInvalidRadioCaptionTypeError(LocalizableStreamlitException):
    """Exception raised when an invalid radio caption type is provided."""

    def __init__(self, caption_type: str):
        super().__init__(
            "Radio captions must be strings. Passed type: {caption_type}",
            caption_type=caption_type,
        )


# New error classes for selectbox
class StreamlitInvalidSelectboxIndexTypeError(LocalizableStreamlitException):
    """Exception raised when an invalid selectbox index type is provided."""

    def __init__(self, index_type: str):
        super().__init__(
            "Selectbox Value has invalid type: {index_type}",
            index_type=index_type,
        )


class StreamlitSelectboxIndexOutOfRangeError(LocalizableStreamlitException):
    """Exception raised when a selectbox index is out of range."""

    def __init__(self):
        super().__init__(
            "Selectbox index must be greater than or equal to 0 and less than the length of options."
        )


# New error classes for slider
class StreamlitInvalidSliderValueTypeError(LocalizableStreamlitException):
    """Exception raised when an invalid slider value type is provided."""

    def __init__(self):
        super().__init__(
            "Slider value should either be an int/float/datetime or a list/tuple of "
            "0 to 2 ints/floats/datetimes"
        )


class StreamlitSliderMixedTypesError(LocalizableStreamlitException):
    """Exception raised when slider components have mixed types."""

    def __init__(self, types: list[type]):
        super().__init__(
            "Slider tuple/list components must be of the same type.\nBut were: {types}",
            types=types,
        )


class StreamlitSliderZeroStepError(LocalizableStreamlitException):
    """Exception raised when a slider step is zero."""

    def __init__(self):
        super().__init__("Slider components cannot be passed a `step` of 0.")


class StreamlitSliderArgumentTypeMismatchError(LocalizableStreamlitException):
    """Exception raised when slider arguments have mismatched types."""

    def __init__(self, min_type: str, max_type: str, step_type: str):
        super().__init__(
            "Slider value arguments must be of matching types."
            "\n`min_value` has {min_type} type."
            "\n`max_value` has {max_type} type."
            "\n`step` has {step_type} type.",
            min_type=min_type,
            max_type=max_type,
            step_type=step_type,
        )


class StreamlitSliderValueArgumentTypeMismatchError(LocalizableStreamlitException):
    """Exception raised when slider value and arguments have mismatched types."""

    def __init__(self, value_type: str, min_type: str, max_type: str):
        super().__init__(
            "Both value and arguments must be of the same type."
            "\n`value` has {value_type} type."
            "\n`min_value` has {min_type} type."
            "\n`max_value` has {max_type} type.",
            value_type=value_type,
            min_type=min_type,
            max_type=max_type,
        )


class StreamlitSliderEqualBoundsError(LocalizableStreamlitException):
    """Exception raised when slider min and max values are equal."""

    def __init__(self, min_value: Any, max_value: Any):
        super().__init__(
            "Slider `min_value` must be less than the `max_value`."
            "\nThe values were {min_value} and {max_value}.",
            min_value=min_value,
            max_value=max_value,
        )


# New error class for JS number bounds in sliders
class StreamlitSliderJSNumberBoundsError(LocalizableStreamlitException):
    """Exception raised when a slider value exceeds JavaScript number bounds."""

    def __init__(self, error_message: str):
        super().__init__(
            "{error_message}",
            error_message=error_message,
        )


# New error classes for deck_gl charts
class StreamlitInvalidSelectionModeSetError(LocalizableStreamlitException):
    """Exception raised when multiple selection modes are passed to a deck_gl chart."""

    def __init__(self, selection_mode: Any):
        super().__init__(
            "Invalid selection mode: {selection_mode}. "
            "Selection mode must be a single value, but got a set instead.",
            selection_mode=selection_mode,
        )


class StreamlitInvalidSelectionModeError(LocalizableStreamlitException):
    """Exception raised when an invalid selection mode is passed to a deck_gl chart."""

    def __init__(self, selection_mode: Any, valid_modes: Any):
        super().__init__(
            "Invalid selection mode: {selection_mode}. "
            "Valid options are: {valid_modes}",
            selection_mode=selection_mode,
            valid_modes=valid_modes,
        )


class StreamlitConflictingSelectionModesError(LocalizableStreamlitException):
    """Exception raised when conflicting selection modes are passed to a deck_gl chart."""

    def __init__(self):
        super().__init__(
            "Only one of `single-object` or `multi-object` can be selected as selection mode."
        )


class StreamlitInvalidOnSelectError(LocalizableStreamlitException):
    """Exception raised when an invalid on_select value is passed to a chart."""

    def __init__(self, on_select: Any):
        super().__init__(
            "You have passed {on_select} to `on_select`. But only 'ignore', "
            "'rerun', or a callable is supported.",
            on_select=on_select,
        )


# New error classes for plotly charts
class StreamlitInvalidPlotlySelectionModeError(LocalizableStreamlitException):
    """Exception raised when an invalid selection mode is passed to a plotly chart."""

    def __init__(self, selection_mode: Any, valid_modes: Any):
        super().__init__(
            "Invalid selection mode: {selection_mode}. "
            "Valid options are: {valid_modes}",
            selection_mode=selection_mode,
            valid_modes=valid_modes,
        )


class StreamlitInvalidPlotlyThemeError(LocalizableStreamlitException):
    """Exception raised when an invalid theme is passed to a plotly chart."""

    def __init__(self, theme: Any):
        super().__init__(
            'You set theme="{theme}" while Streamlit charts only support '
            'theme="streamlit" or theme=None to fallback to the default '
            "library theme.",
            theme=theme,
        )


# New error class for bokeh charts
class StreamlitIncompatibleBokehVersionError(LocalizableStreamlitException):
    """Exception raised when an incompatible bokeh version is used."""

    def __init__(self, current_version: str, required_version: str):
        super().__init__(
            "Streamlit only supports Bokeh version {required_version}, "
            "but you have version {current_version} installed. Please "
            "run `pip install --force-reinstall --no-deps bokeh=="
            "{required_version}` to install the correct version.\n\n\n"
            "To use the latest version of Bokeh, install our custom component, "
            "streamlit-bokeh-events, from https://github.com/ash2shukla/streamlit-bokeh-events",
            current_version=current_version,
            required_version=required_version,
        )


# New error class for query parameters
class StreamlitInvalidConnectionTypeError(LocalizableStreamlitException):
    """Raised when an invalid connection type is provided."""

    def __init__(self, connection_type: str, supported_connections: dict[str, Any]):
        super().__init__(
            "Invalid connection '{connection_type}'. Supported connection classes: {supported_connections}",
            connection_type=connection_type,
            supported_connections=supported_connections,
        )


class StreamlitInvalidQueryParamDictError(LocalizableStreamlitException):
    """Raised when a dictionary is provided as a query param value."""

    def __init__(self, key: str):
        super().__init__(
            "You cannot set a query params key `{key}` to a dictionary.",
            key=key,
        )


class StreamlitReservedQueryParamError(LocalizableStreamlitException):
    """Raised when a reserved query param is set programmatically."""

    def __init__(self):
        super().__init__(
            "Query param embed and embed_options (case-insensitive) cannot be set programmatically."
        )


# New error classes for logos
class StreamlitInvalidLogoImageError(LocalizableStreamlitException):
    """Exception raised when an invalid logo image is provided."""

    def __init__(self, field_name: str):
        super().__init__(
            "The {field_name} passed to st.logo is invalid - See [documentation]"
            "(https://docs.streamlit.io/develop/api-reference/media/st.logo) "
            "for more information on valid types",
            field_name=field_name,
        )


class StreamlitInvalidLogoLinkError(LocalizableStreamlitException):
    """Exception raised when an invalid logo link is provided."""

    def __init__(self, link: str):
        super().__init__(
            "Invalid link: {link} - the link param supports external links only "
            "and must start with either http:// or https://.",
            link=link,
        )


class StreamlitInvalidLogoSizeError(LocalizableStreamlitException):
    """Exception raised when an invalid logo size is provided."""

    def __init__(self, size: Any):
        super().__init__(
            'The size argument to st.logo must be "small", "medium", or "large". \n'
            "The argument passed was {size}.",
            size=size,
        )


# New error classes for execution control
class StreamlitInvalidFragmentScopeError(LocalizableStreamlitException):
    """Exception raised when fragment scope is used outside of a fragment rerun."""

    def __init__(self):
        super().__init__(
            'scope="fragment" can only be specified from `@st.fragment`-decorated '
            "functions during fragment reruns."
        )


class StreamlitInvalidRerunScopeError(LocalizableStreamlitException):
    """Exception raised when an invalid rerun scope is provided."""

    def __init__(self, scope: str):
        super().__init__(
            "'{scope}' is not a valid rerun scope. Valid scopes are 'app' and 'fragment'.",
            scope=scope,
        )


class StreamlitPageNotFoundInAppError(LocalizableStreamlitException):
    """Exception raised when a page is not found in the app."""

    def __init__(self, page: str, main_script_directory: str):
        super().__init__(
            "Could not find page: `{page}`. Must be the file path relative to the main script, "
            "from the directory: `{directory}`. Only the main app file and files in the "
            "`pages/` directory are supported.",
            page=page,
            directory=os.path.basename(main_script_directory),
        )


# New error classes for navigation
class StreamlitInvalidPageTypeError(LocalizableStreamlitException):
    """Exception raised when an invalid page type is provided."""

    def __init__(self, page_type: str):
        super().__init__(
            "Invalid page type: {page_type}. Must be either a string path, "
            "a pathlib.Path, a callable function, or a st.Page object.",
            page_type=page_type,
        )


class StreamlitEmptyNavigationError(LocalizableStreamlitException):
    """Exception raised when navigation is called with no pages."""

    def __init__(self):
        super().__init__("`st.navigation` must be called with at least one `st.Page`.")


class StreamlitMultipleDefaultPagesError(LocalizableStreamlitException):
    """Exception raised when multiple pages are set as default."""

    def __init__(self):
        super().__init__(
            "Multiple Pages specified with `default=True`. "
            "At most one Page can be set to default."
        )


class StreamlitDuplicatePagePathError(LocalizableStreamlitException):
    """Exception raised when multiple pages have the same URL pathname."""

    def __init__(self, url_path: str):
        super().__init__(
            "Multiple Pages specified with URL pathname {url_path}. "
            "URL pathnames must be unique. The url pathname may be "
            "inferred from the filename, callable name, or title.",
            url_path=url_path,
        )


# New error class for type validation
class StreamlitNonComparableOptionError(LocalizableStreamlitException):
    """Exception raised when a non-comparable option is provided."""

    def __init__(self, option_type: str):
        super().__init__(
            "Invalid option type provided. Options must be comparable, returning a "
            "boolean when used with *==*. \n\nGot **{option_type}**, "
            "which cannot be compared. Refactor your code to use elements of "
            "comparable types as options, e.g. use indices instead.",
            option_type=option_type,
        )


# New error class for custom components
class StreamlitMissingPyArrowError(LocalizableStreamlitException):
    """Exception raised when PyArrow is missing for custom components."""

    def __init__(self):
        super().__init__(
            """To use Custom Components in Streamlit, you need to install
PyArrow. To do so locally:

`pip install pyarrow`

And if you're using Streamlit Cloud, add "pyarrow" to your requirements.txt."""
        )


# New error class for local component registry
class StreamlitComponentDirectoryNotFoundError(LocalizableStreamlitException):
    """Exception raised when a component directory is not found."""

    def __init__(self, directory: str):
        super().__init__(
            "No such component directory: '{directory}'",
            directory=directory,
        )


# New error class for mutable status container
class StreamlitInvalidStatusStateError(LocalizableStreamlitException):
    """Exception raised when an invalid state is provided for a status container."""

    def __init__(self, state: str):
        super().__init__(
            "Unknown state ({state}). Must be one of 'running', 'complete', or 'error'.",
            state=state,
        )


# New error class for dialog
class StreamlitMultipleDialogsError(LocalizableStreamlitException):
    """Exception raised when multiple dialogs are opened at the same time."""

    def __init__(self):
        super().__init__(
            "Only one dialog is allowed to be opened at the same time. "
            "Please make sure to not call a dialog-decorated function more than once in a script run."
        )


# New error classes for media
class StreamlitMissingSampleRateError(LocalizableStreamlitException):
    """Exception raised when sample_rate is missing for numpy array audio data."""

    def __init__(self):
        super().__init__(
            "`sample_rate` must be specified when `data` is a numpy array."
        )


class StreamlitYouTubeSubtitlesError(LocalizableStreamlitException):
    """Exception raised when subtitles are provided for YouTube videos."""

    def __init__(self):
        super().__init__("Subtitles are not supported for YouTube videos.")


class StreamlitUnsupportedSubtitlesTypeError(LocalizableStreamlitException):
    """Exception raised when an unsupported subtitles type is provided."""

    def __init__(self, subtitles_type: str):
        super().__init__(
            "Unsupported data type for subtitles: {subtitles_type}. "
            "Only str (file paths) and dict are supported.",
            subtitles_type=subtitles_type,
        )


class StreamlitSubtitlesProcessingError(LocalizableStreamlitException):
    """Exception raised when there's an error processing subtitles."""

    def __init__(self, label: str):
        super().__init__(
            "Failed to process the provided subtitle: {label}",
            label=label,
        )


class StreamlitInvalidTimeFormatError(LocalizableStreamlitException):
    """Raised when an invalid time format is provided."""

    def __init__(self, param_name: str, expected_formats: str):
        super().__init__(
            "Invalid {param_name} format. Expected formats: {expected_formats}",
            param_name=param_name,
            expected_formats=expected_formats,
        )


class StreamlitInvalidTextInputTypeError(LocalizableStreamlitException):
    """Raised when an invalid text input type is provided."""

    def __init__(self, invalid_type: str):
        super().__init__(
            "'{invalid_type}' is not a valid text_input type. Valid types are 'default' and 'password'.",
            invalid_type=invalid_type,
        )


class StreamlitInvalidTextAreaHeightError(LocalizableStreamlitException):
    """Raised when an invalid height is provided for a text area."""

    def __init__(self, height: int):
        super().__init__(
            "Invalid height {height}px for `st.text_area` - must be at least 68 pixels.",
            height=height,
        )


class StreamlitInvalidButtonGroupSelectionModeError(LocalizableStreamlitException):
    """Raised when an invalid selection mode is provided for a button group."""

    def __init__(self, selection_mode: str):
        super().__init__(
            "The selection_mode argument must be one of ['single', 'multi']. The argument passed was '{selection_mode}'.",
            selection_mode=selection_mode,
        )


class StreamlitInvalidFeedbackOptionsError(LocalizableStreamlitException):
    """Raised when invalid options are provided for feedback widget."""

    def __init__(self, options: str):
        super().__init__(
            "The options argument to st.feedback must be one of ['thumbs', 'faces', 'stars']. The argument passed was '{options}'.",
            options=options,
        )


class StreamlitInvalidDefaultValueError(LocalizableStreamlitException):
    """Raised when an invalid default value is provided for a widget."""

    def __init__(self, widget_name: str, selection_mode: str):
        super().__init__(
            "The default argument to `st.{widget_name}` must be a single value when `selection_mode='{selection_mode}'`.",
            widget_name=widget_name,
            selection_mode=selection_mode,
        )


class StreamlitInvalidStyleError(LocalizableStreamlitException):
    """Raised when an invalid style is provided for a button group."""

    def __init__(self, style: str, valid_styles: list[str]):
        valid_styles_str = "', '".join(valid_styles)
        super().__init__(
            "The style argument must be one of ['{valid_styles_str}']. The argument passed was '{style}'.",
            valid_styles_str=valid_styles_str,
            style=style,
        )


class StreamlitInvalidDividerColorError(LocalizableStreamlitException):
    """Raised when an invalid divider color is provided for a heading."""

    def __init__(self, divider: str, valid_colors: list[str]):
        super().__init__(
            "Divider parameter has invalid value: `{divider}`. Please choose from: {valid_colors}.",
            divider=divider,
            valid_colors=", ".join(valid_colors),
        )


class StreamlitInvalidAnchorValueError(LocalizableStreamlitException):
    """Raised when an invalid anchor value is provided for a heading."""

    def __init__(self, anchor: Any):
        super().__init__(
            "Anchor parameter has invalid value: {anchor}. Supported values: None, any string or False",
            anchor=anchor,
        )


class StreamlitInvalidAnchorTypeError(LocalizableStreamlitException):
    """Raised when an invalid anchor type is provided for a heading."""

    def __init__(self, anchor_type: str):
        super().__init__(
            "Anchor parameter has invalid type: {anchor_type}. Supported values: None, any string or False",
            anchor_type=anchor_type,
        )


class StreamlitEmptyTabsError(LocalizableStreamlitException):
    """Raised when an empty list is provided to st.tabs."""

    def __init__(self):
        super().__init__(
            "The input argument to st.tabs must contain at least one tab label."
        )


class StreamlitInvalidTabTypeError(LocalizableStreamlitException):
    """Raised when non-string tab labels are provided to st.tabs."""

    def __init__(self):
        super().__init__(
            "The tabs input list to st.tabs is only allowed to contain strings."
        )


class StreamlitInvalidDeltaColorError(LocalizableStreamlitException):
    """Raised when an invalid delta_color is provided to st.metric."""

    def __init__(self, delta_color: str):
        super().__init__(
            "'{delta_color}' is not an accepted value. delta_color only accepts: 'normal', 'inverse', or 'off'",
            delta_color=delta_color,
        )


class StreamlitNestedFormError(LocalizableStreamlitException):
    """Raised when a form is nested inside another form."""

    def __init__(self):
        super().__init__("Forms cannot be nested in other forms.")


class StreamlitDuplicateFormError(LocalizableStreamlitException):
    """Raised when a form with the same key is created more than once."""

    def __init__(self, message: str):
        super().__init__(message)


class StreamlitInvalidFormButtonTypeError(LocalizableStreamlitException):
    """Raised when an invalid button type is provided to st.form_submit_button."""

    def __init__(self, button_type: str):
        super().__init__(
            'The type argument to st.form_submit_button must be "primary", "secondary", or "tertiary". \n'
            'The argument passed was "{button_type}".',
            button_type=button_type,
        )


class StreamlitNestedDialogError(LocalizableStreamlitException):
    """Raised when a dialog is nested inside another dialog."""

    def __init__(self):
        super().__init__("Dialogs may not be nested inside other dialogs.")


class StreamlitEmptyDialogTitleError(LocalizableStreamlitException):
    """Raised when an empty title is provided for a dialog."""

    def __init__(self):
        super().__init__(
            "A non-empty `title` argument has to be provided for dialogs, for example "
            '`@st.dialog("Example Title")`.'
        )


class StreamlitNestedPopoverError(LocalizableStreamlitException):
    """Raised when a popover is nested inside another popover."""

    def __init__(self):
        super().__init__("Popovers may not be nested inside other popovers.")


class StreamlitNestedExpanderError(LocalizableStreamlitException):
    """Raised when an expander is nested inside another expander."""

    def __init__(self):
        super().__init__("Expanders may not be nested inside other expanders.")


class StreamlitNestedChatMessageError(LocalizableStreamlitException):
    """Raised when a chat message is nested inside another chat message."""

    def __init__(self):
        super().__init__("Chat messages cannot nested inside other chat messages.")


class StreamlitNestedColumnsError(LocalizableStreamlitException):
    """Raised when columns are nested too deeply."""

    def __init__(self):
        super().__init__(
            "Columns can only be placed inside other columns up to one level of nesting."
        )


class StreamlitSidebarNestedColumnsError(LocalizableStreamlitException):
    """Raised when columns are nested inside other columns in the sidebar."""

    def __init__(self):
        super().__init__(
            "Columns cannot be placed inside other columns in the sidebar. This is only possible in the main area of the app."
        )


class StreamlitEmptyVegaLiteSpecError(LocalizableStreamlitException):
    """Raised when an empty spec is provided to a Vega-Lite chart."""

    def __init__(self):
        super().__init__("Vega-Lite charts require a non-empty spec dict.")


class StreamlitMissingMapboxTokenError(LocalizableStreamlitException):
    """Raised when a map style is specified but no Mapbox token is provided."""

    def __init__(self):
        super().__init__(
            "You need a Mapbox token in order to select a map type. "
            "Refer to the docs for st.map for more information."
        )


class StreamlitMissingMapColumnError(LocalizableStreamlitException):
    """Raised when required latitude or longitude columns are missing from map data."""

    def __init__(
        self,
        human_readable_name: str,
        allowed_col_names: list[str],
        existing_columns: list[str],
    ):
        super().__init__(
            "Map data must contain a {human_readable_name} column named: "
            "{allowed_col_names}. Existing columns: {existing_columns}",
            human_readable_name=human_readable_name,
            allowed_col_names=", ".join(map(repr, sorted(allowed_col_names))),
            existing_columns=", ".join(map(repr, existing_columns)),
        )


class StreamlitMapColumnNullError(LocalizableStreamlitException):
    """Raised when a map column contains null values."""

    def __init__(self, col_name: str):
        super().__init__(
            "Column {col_name} is not allowed to contain null values, such "
            "as NaN, NaT, or None.",
            col_name=col_name,
        )


class StreamlitInvalidMapColorError(LocalizableStreamlitException):
    """Raised when a map color column contains invalid colors."""

    def __init__(self, col_name: str):
        super().__init__(
            'Column "{col_name}" does not appear to contain valid colors.',
            col_name=col_name,
        )


class StreamlitInvalidGraphvizChartError(LocalizableStreamlitException):
    """Raised when an invalid figure or dot is provided to a graphviz chart."""

    def __init__(self, figure_type: str):
        super().__init__(
            "Unhandled type for graphviz chart: {figure_type}",
            figure_type=figure_type,
        )


class StreamlitInvalidDataframeSelectionModeError(LocalizableStreamlitException):
    """Raised when an invalid selection mode is provided to a dataframe."""

    def __init__(self, selection_mode: Any, valid_modes: Any):
        super().__init__(
            "Invalid selection mode: {selection_mode}. Valid options are: {valid_modes}",
            selection_mode=selection_mode,
            valid_modes=valid_modes,
        )


class StreamlitConflictingRowSelectionModesError(LocalizableStreamlitException):
    """Raised when conflicting row selection modes are provided to a dataframe."""

    def __init__(self):
        super().__init__(
            "Only one of `single-row` or `multi-row` can be selected as selection mode."
        )


class StreamlitConflictingColumnSelectionModesError(LocalizableStreamlitException):
    """Raised when conflicting column selection modes are provided to a dataframe."""

    def __init__(self):
        super().__init__(
            "Only one of `single-column` or `multi-column` can be selected as selection mode."
        )


class StreamlitAddRowsToNonExistingElementError(LocalizableStreamlitException):
    """Raised when add_rows is called on a non-existing element."""

    def __init__(self):
        super().__init__("Only existing elements can `add_rows`.")


class StreamlitWrongAddRowsArgsError(LocalizableStreamlitException):
    """Raised when add_rows is called with wrong number of arguments."""

    def __init__(self):
        super().__init__("Wrong number of arguments to add_rows().")


class StreamlitInvalidStreamTypeError(LocalizableStreamlitException):
    """Raised when an invalid stream type is provided to write_stream."""

    def __init__(self, stream_type: type):
        super().__init__(
            "`st.write_stream` expects a generator or stream-like object as input "
            "not {stream_type}. Please use `st.write` instead for "
            "this data type.",
            stream_type=stream_type,
        )


class StreamlitNonIterableStreamError(LocalizableStreamlitException):
    """Raised when a non-iterable stream is provided to write_stream."""

    def __init__(self, stream_type: type):
        super().__init__(
            "The provided input (type: {stream_type}) cannot be iterated. "
            "Please make sure that it is a generator, generator function or iterable.",
            stream_type=stream_type,
        )


class StreamlitOpenAIChunkParseError(LocalizableStreamlitException):
    """Raised when an OpenAI chat completion chunk cannot be parsed."""

    def __init__(self):
        super().__init__(
            "Failed to parse the OpenAI ChatCompletionChunk. "
            "The most likely cause is a change of the chunk object structure "
            "due to a recent OpenAI update. You might be able to fix this "
            "by downgrading the OpenAI library or upgrading Streamlit. Also, "
            "please report this issue to: https://github.com/streamlit/streamlit/issues."
        )


class StreamlitLangChainChunkParseError(LocalizableStreamlitException):
    """Raised when a LangChain message chunk cannot be parsed."""

    def __init__(self):
        super().__init__(
            "Failed to parse the LangChain AIMessageChunk. "
            "The most likely cause is a change of the chunk object structure "
            "due to a recent LangChain update. You might be able to fix this "
            "by downgrading the OpenAI library or upgrading Streamlit. Also, "
            "please report this issue to: https://github.com/streamlit/streamlit/issues."
        )


class StreamlitMultipleElementsReplaceError(LocalizableStreamlitException):
    """Raised when trying to replace a single element with multiple elements."""

    def __init__(self):
        super().__init__(
            "Cannot replace a single element with multiple elements.\n\n"
            "The `write()` method only supports multiple elements when "
            "inserting elements rather than replacing. That is, only "
            "when called as `st.write()` or `st.sidebar.write()`."
        )


class StreamlitInvalidEmojiError(LocalizableStreamlitException):
    """Raised when an invalid emoji is provided."""

    def __init__(self, emoji: str):
        super().__init__(
            'The value "{emoji}" is not a valid emoji. Shortcodes are not allowed, please use a single character instead.',
            emoji=emoji,
        )


class StreamlitInvalidMaterialIconError(LocalizableStreamlitException):
    """Raised when an invalid Material icon is provided."""

    def __init__(self, icon: str):
        # Since our markdown processing needs to change the `/` to `_` in order to
        # correctly render the icon, we need to add a zero-width space before the
        # `/` to avoid this transformation here.
        invisible_white_space = "\u200b"
        super().__init__(
            'The value `"{icon}"` is not a valid Material icon. '
            "Please use a Material icon shortcode like **`:material{invisible_white_space}/thumb_up:`**",
            icon=icon.replace("/", invisible_white_space + "/"),
            invisible_white_space=invisible_white_space,
        )


class StreamlitInvalidMaterialIconPackError(LocalizableStreamlitException):
    """Raised when an invalid Material icon pack or icon name is provided."""

    def __init__(self, icon: str):
        # Since our markdown processing needs to change the `/` to `_` in order to
        # correctly render the icon, we need to add a zero-width space before the
        # `/` to avoid this transformation here.
        invisible_white_space = "\u200b"
        super().__init__(
            'The value `"{icon}"` is not a valid Material icon.'
            " Please use a Material icon shortcode like **`:material{invisible_white_space}/thumb_up:`**. ",
            icon=icon.replace("/", invisible_white_space + "/"),
            invisible_white_space=invisible_white_space,
        )


class StreamlitInvalidConnectionClassError(LocalizableStreamlitException):
    """Raised when an invalid connection class is provided."""

    def __init__(self, connection_class: type):
        super().__init__(
            "{connection_class} is not a subclass of BaseConnection!",
            connection_class=connection_class,
        )


class StreamlitUnrecognizedConfigOptionError(LocalizableStreamlitException):
    """Raised when an unrecognized config option is provided."""

    def __init__(self, key: str):
        super().__init__(
            "Unrecognized config option: {key}",
            key=key,
        )


class StreamlitNonScriptableConfigOptionError(LocalizableStreamlitException):
    """Raised when a non-scriptable config option is set on the fly."""

    def __init__(self, key: str):
        super().__init__(
            "{key} cannot be set on the fly. Set as command line option, e.g. streamlit run script.py --{key}, or in config.toml instead.",
            key=key,
        )


class StreamlitQueryParamsAPIConflictError(LocalizableStreamlitException):
    """Raised when both experimental and production query params APIs are used together."""

    def __init__(self):
        super().__init__(
            "Using `st.query_params` together with either `st.experimental_get_query_params` "
            "or `st.experimental_set_query_params` is not supported. Please convert your app "
            "to only use `st.query_params`"
        )


class StreamlitUnsupportedPersistOptionError(LocalizableStreamlitException):
    def __init__(self, persist: str):
        super().__init__(
            "Unsupported persist option: {persist}. Valid options are 'disk' and 'memory'.",
            persist=persist,
        )


# New error classes to replace direct StreamlitAPIException usage


class StreamlitReservedKeyError(LocalizableStreamlitException):
    """Raised when a user tries to use a reserved key name for a widget or other element."""

    def __init__(self, key: str, prefix: str):
        super().__init__(
            "Keys beginning with {prefix} are reserved.",
            key=key,
            prefix=prefix,
        )


class StreamlitWidgetStateModificationError(LocalizableStreamlitException):
    """Raised when attempting to modify a widget's state after the widget has been instantiated."""

    def __init__(self, user_key: str):
        super().__init__(
            "`st.session_state.{user_key}` cannot be modified after the widget with key `{user_key}` is instantiated.",
            user_key=user_key,
        )


class StreamlitMultiViewChartSelectionsNotSupportedError(LocalizableStreamlitException):
    """Raised when attempting to use selections with multi-view charts, which is not yet supported."""

    def __init__(self):
        super().__init__(
            "Selections are not yet supported for multi-view charts (chart compositions). "
            "If you would like to use selections on multi-view charts, please upvote "
            "this [Github issue](https://github.com/streamlit/streamlit/issues/8643)."
        )


class StreamlitInvalidStackParameterError(LocalizableStreamlitException):
    """Raised when an invalid value is provided for the stack parameter in a chart."""

    def __init__(self, stack: Any, command: str, docs_link: str):
        super().__init__(
            'Invalid value for stack parameter: {stack}. Stack must be one of True, False, "normalize", "center", "layered" or None. '
            "See documentation for `{command}` [here]({docs_link}) for more information.",
            stack=stack,
            command=command,
            docs_link=docs_link,
        )


class StreamlitColumnNotFoundError(LocalizableStreamlitException):
    """Raised when a specified column name is not found in the input dataframe."""

    def __init__(self, column_name: str, available_columns: list[str]):
        super().__init__(
            "Column '{column_name}' not found in the input dataframe. Available columns: {available_columns}",
            column_name=column_name,
            available_columns=available_columns,
        )


class StreamlitChartInvalidColorError(LocalizableStreamlitException):
    """Raised when an invalid color value is provided to a chart or visual element."""

    def __init__(self, color_value: Any):
        super().__init__(
            "Invalid color value: {color_value}. Expected a string color name, CSS color code, or a list of colors.",
            color_value=color_value,
        )


class StreamlitColorLengthError(LocalizableStreamlitException):
    """Raised when the length of a color list doesn't match the number of columns to be colored."""

    def __init__(self, color_values: list[Any], y_column_count: int):
        super().__init__(
            "Length of color list ({color_length}) must match the number of y columns ({y_column_count}).",
            color_length=len(color_values),
            y_column_count=y_column_count,
        )


class StreamlitRangeIndexStepError(LocalizableStreamlitException):
    """Raised when attempting to access the step attribute of a RangeIndex that doesn't have one."""

    def __init__(self):
        super().__init__("'RangeIndex' object has no attribute 'step'")


class StreamlitRangeIndexStopError(LocalizableStreamlitException):
    """Raised when attempting to access the stop attribute of a RangeIndex that doesn't have one."""

    def __init__(self):
        super().__init__("'RangeIndex' object has no attribute 'stop'")


class StreamlitInvalidSizeValueError(LocalizableStreamlitException):
    """Raised when an invalid size value is provided to a chart element."""

    def __init__(self, size_value: Any):
        super().__init__(
            "Invalid size value: {size_value}. Expected a number or a column name.",
            size_value=size_value,
        )


class StreamlitMixedColumnTypesError(LocalizableStreamlitException):
    """Raised when chart columns contain too many values with mixed types."""

    def __init__(self):
        super().__init__(
            "The columns used for rendering the chart contain too many values with mixed types. "
            "Please select the columns manually via the y parameter."
        )


class StreamlitInvalidXParameterTypeError(LocalizableStreamlitException):
    """Raised when an invalid type is provided for the x parameter in a chart."""

    def __init__(self, x_from_user: Any):
        super().__init__(
            "x parameter should be a column name (str) or None to use the dataframe's index. "
            "Value given: {x_from_user} (type {x_type})",
            x_from_user=x_from_user,
            x_type=type(x_from_user),
        )


class StreamlitMissingChartSelectionsError(LocalizableStreamlitException):
    """Raised when selections are activated but the chart spec doesn't have any selections defined."""

    def __init__(self):
        super().__init__(
            "Selections are activated, but the provided chart spec does not "
            "have any selections defined. To add selections to `st.altair_chart`, check out the documentation "
            "[here](https://altair-viz.github.io/user_guide/interactions.html#selections-capturing-chart-interactions). "
            "For adding selections to `st.vega_lite_chart`, take a look "
            "[here](https://vega.github.io/vega-lite/docs/selection.html)."
        )


class StreamlitUndefinedSelectionParameterError(LocalizableStreamlitException):
    """Raised when a selection parameter is specified but not defined in the chart spec."""

    def __init__(self, selection_name: str, available_params: set[str]):
        super().__init__(
            "Selection parameter '{selection_name}' is not defined in the chart spec. "
            "Available selection parameters are: {available_params}.",
            selection_name=selection_name,
            available_params=available_params,
        )


class StreamlitAltairVersionError(LocalizableStreamlitException):
    """Raised when a feature requires a newer version of Altair."""

    def __init__(self, feature: str):
        super().__init__(
            "Streamlit does not support {feature} with Altair 4.x. Please upgrade "
            "to Version 5.",
            feature=feature,
        )


class StreamlitAltairSelectionsVersionError(LocalizableStreamlitException):
    """Raised when selections are used with an older version of Altair."""

    def __init__(self):
        super().__init__(
            "Streamlit does not support selections with Altair 4.x. Please upgrade "
            "to Version 5. "
            "If you would like to use Altair 4.x with selections, please upvote "
            "this [Github issue](https://github.com/streamlit/streamlit/issues/8516)."
        )


class StreamlitInvalidThemeError(LocalizableStreamlitException):
    """Raised when an invalid theme is specified for a chart."""

    def __init__(self, theme: str):
        super().__init__(
            'You set theme="{theme}" while Streamlit charts only support '
            'theme="streamlit" or theme=None to fallback to the default '
            "library theme.",
            theme=theme,
        )


class StreamlitDefaultValueNotInOptionsError(LocalizableStreamlitException):
    """Raised when a default value is not part of the provided options."""

    def __init__(self, value: Any):
        super().__init__(
            "The default value '{value}' is not part of the options. "
            "Please make sure that every default values also exists in the options.",
            value=value,
        )


class StreamlitInvalidEnumCoercionConfigError(LocalizableStreamlitException):
    """Raised when an invalid enum coercion config value is provided."""

    def __init__(self, coercion_type: str, allowed_settings: set[str]):
        super().__init__(
            "Invalid value for config option runner.enumCoercion. "
            "Expected one of {allowed_settings}, but got '{coercion_type}'.",
            coercion_type=coercion_type,
            allowed_settings=allowed_settings,
        )


class StreamlitPandasStylerMaxElementsError(LocalizableStreamlitException):
    """Raised when a pandas styler exceeds the maximum number of elements allowed."""

    def __init__(self, cells_count: int, max_elements: int):
        super().__init__(
            "The dataframe has `{cells_count}` cells, but the maximum number "
            "of cells allowed to be rendered by Pandas Styler is configured to "
            "`{max_elements}`. To allow more cells to be "
            'styled, you can change the `"styler.render.max_elements"` config. For example: '
            '`pd.set_option("styler.render.max_elements", {cells_count})`',
            cells_count=cells_count,
            max_elements=max_elements,
        )


class StreamlitBGRChannelsRequireThreeColorChannelsError(LocalizableStreamlitException):
    """Raised when BGR channels are specified but the image doesn't have exactly 3 color channels."""

    def __init__(self):
        super().__init__(
            'When using `channels="BGR"`, the input image should have exactly 3 color channels'
        )


class StreamlitInvalidColumnConfigTypeError(LocalizableStreamlitException):
    """Raised when an invalid column config type is provided."""

    def __init__(self, column: str, config_type: type):
        super().__init__(
            "Invalid column config for column `{column}`. "
            "Expected `None`, `str` or `dict`, but got `{config_type}`.",
            column=column,
            config_type=config_type,
        )


class StreamlitColumnConfigSerializationError(LocalizableStreamlitException):
    """Raised when a column config cannot be serialized to JSON."""

    def __init__(self, error_message: str):
        super().__init__(
            "The provided column config cannot be serialized into JSON: {error_message}",
            error_message=error_message,
        )


class StreamlitMissingSnowflakeConfigError(LocalizableStreamlitException):
    """Raised when Snowflake connection configuration is missing."""

    def __init__(self):
        super().__init__(
            "Missing Snowflake connection configuration. "
            "Did you forget to set this in `secrets.toml`, a Snowflake configuration file, "
            "or as kwargs to `st.connection`? "
            "See the [SnowflakeConnection configuration documentation](https://docs.streamlit.io/st.connections.snowflakeconnection-configuration) "
            "for more details and examples."
        )


class StreamlitInvalidComponentConfigError(LocalizableStreamlitException):
    """Raised when a custom component has invalid configuration."""

    def __init__(self):
        super().__init__("Either 'path' or 'url' must be set, but not both.")


class StreamlitPageFileNotFoundError(LocalizableStreamlitException):
    """Raised when a page file cannot be found."""

    def __init__(self, page_name: str):
        super().__init__(
            "Unable to create Page. The file `{page_name}` could not be found.",
            page_name=page_name,
        )


class StreamlitMissingPageTitleError(LocalizableStreamlitException):
    """Raised when a page title cannot be inferred for a callable page."""

    def __init__(self):
        super().__init__(
            "Cannot infer page title for Callable. Set the `title=` keyword argument."
        )


class StreamlitEmptyPageTitleError(LocalizableStreamlitException):
    """Raised when a page title is empty or consists only of underscores/spaces."""

    def __init__(self):
        super().__init__(
            "The title of the page cannot be empty or consist of underscores/spaces only"
        )


class StreamlitEmptyPageUrlPathError(LocalizableStreamlitException):
    """Raised when a page URL path is empty and the page is not the default page."""

    def __init__(self):
        super().__init__(
            "The URL path cannot be an empty string unless the page is the default page."
        )


class StreamlitNestedPageUrlPathError(LocalizableStreamlitException):
    """Raised when a page URL path contains a nested path."""

    def __init__(self):
        super().__init__("The URL path cannot contain a nested path (e.g. foo/bar).")


class StreamlitPageCannotBeCalledDirectlyError(LocalizableStreamlitException):
    """Raised when a page is called directly instead of through st.navigation."""

    def __init__(self):
        super().__init__(
            "This page cannot be called directly. Only the page returned from st.navigation can be called once."
        )


class StreamlitInvalidCommandError(LocalizableStreamlitException):
    """Raised when an invalid Streamlit command is used."""

    def __init__(self, command_name: str, suggestion: str | None = None):
        if suggestion:
            super().__init__(
                "Method `{command_name}()` does not exist for "
                "`DeltaGenerator` objects. Did you mean "
                "`st.{suggestion}()`?",
                command_name=command_name,
                suggestion=suggestion,
            )
        else:
            super().__init__(
                "`{command_name}()` is not a valid Streamlit command.",
                command_name=command_name,
            )


class StreamlitSidebarInFragmentError(LocalizableStreamlitException):
    """Raised when st.sidebar is called in a function wrapped with st.fragment."""

    def __init__(self):
        super().__init__(
            "Calling `st.sidebar` in a function wrapped with `st.fragment` is not "
            "supported. Please use `st.sidebar` outside of the fragment function."
        )


class StreamlitBuiltinNameError(LocalizableStreamlitException):
    """Raised when a builtin name is used with st prefix."""

    def __init__(self, name: str):
        super().__init__(
            "Did you mean `{name}` instead of `st.{name}`?",
            name=name,
        )


class StreamlitSidebarMethodError(LocalizableStreamlitException):
    """Raised when a method is incorrectly called on st.sidebar."""

    def __init__(self, name: str):
        super().__init__(
            "Method `{name}()` does not exist for `st.sidebar`. Did you mean `st.{name}()`?",
            name=name,
        )


class StreamlitUnsupportedLabelVisibilityError(LocalizableStreamlitException):
    """Raised when an unsupported label_visibility option is provided."""

    def __init__(self, label_visibility: str):
        super().__init__(
            "Unsupported label_visibility option '{label_visibility}'. "
            "Valid values are 'visible', 'hidden' or 'collapsed'.",
            label_visibility=label_visibility,
        )


class StreamlitDataFrameConversionError(LocalizableStreamlitException):
    """Raised when an object cannot be converted to a pandas DataFrame."""

    def __init__(self, data: Any):
        super().__init__(
            """
Unable to convert object of type `{data_type}` to `pandas.DataFrame`.
Offending object:
```py
{data}
```""",
            data_type=type(data),
            data=data,
        )
