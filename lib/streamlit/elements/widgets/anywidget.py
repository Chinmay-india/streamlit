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

# anywidget.py:

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Optional, cast

from streamlit.proto import AnyWidget_pb2

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator
from urllib.parse import quote

from streamlit.runtime.metrics_util import gather_metrics
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.runtime.state import get_session_state


class WidgetValue:
    """A wrapper class to provide access to widget value."""

    def __init__(self, key: str, default_value: Any = None):
        self._key = key
        self._default = default_value

    def __repr__(self):
        return f"{self.value}"

    @property
    def value(self) -> Any:
        """Get the current value of the widget."""
        ctx = get_script_run_ctx()
        if ctx is None:
            return self._default

        try:
            session_state = get_session_state()
            print("session_state: ", session_state)
            print("self._key: ", self._key)

            return session_state.get(self._key, self._default)
        except Exception:
            return self._default


class AnyWidgetMixin:
    @gather_metrics("anywidget")
    def anywidget(
        self,
        widget_obj: Any,
        key: Optional[str] = None,
        help: Optional[str] = None,
        disabled: bool = False,
        label_visibility: str = "visible",
    ) -> WidgetValue:
        """Insert an anywidget element.

        Parameters
        ----------
        widget_obj : Any
            An anywidget-compatible widget object
        key : str, optional
            An optional key that uniquely identifies this widget
        help : str, optional
            An optional tooltip
        disabled : bool, default False
            Whether this widget is disabled
        label_visibility : str, default "visible"
            One of "visible", "hidden", or "collapsed"

        Returns
        -------
        WidgetValue
            An object with a .value property that provides access to the widget's value
        """
        # Generate a unique ID if none provided
        widget_id = key or f"anywidget_{id(widget_obj)}"

        # Get session state to check for existing values
        session_state = get_session_state()

        # Create the protobuf message
        anywidget_proto = AnyWidget_pb2.AnyWidget()

        # Handle different ESM source types
        esm_source = widget_obj._esm
        if not esm_source.startswith(("http://", "https://", "/", "data:")):
            # Encode inline JavaScript as proper data URL
            esm_source = f"data:text/javascript;charset=utf-8,{quote(esm_source)}"

        # Create widget spec
        spec_dict = {"esm": esm_source, "css": getattr(widget_obj, "_css", "")}

        # Set the widget specification
        anywidget_proto.spec = json.dumps(spec_dict)

        # Extract widget state
        widget_state = self._extract_serializable_data(widget_obj)

        # Check if we have a value in session state and use it to update the widget object
        if widget_id in session_state:
            stored_value = session_state[widget_id]
            try:
                stored_data = (
                    json.loads(stored_value)
                    if isinstance(stored_value, str)
                    else stored_value
                )
                # Update traitlets attributes if possible
                if hasattr(widget_obj, "_trait_values"):
                    for key, value in stored_data.items():
                        if hasattr(widget_obj, key) and key in widget_obj._trait_values:
                            setattr(widget_obj, key, value)
                # Update our extracted state
                widget_state.update(stored_data)
            except (json.JSONDecodeError, AttributeError):
                pass

        # Serialize the initial value
        anywidget_proto.initial_value = json.dumps(widget_state).encode()

        # Set other widget properties
        anywidget_proto.disabled = disabled
        if help:
            anywidget_proto.help = help
        anywidget_proto.id = widget_id

        # Queue the widget in the Streamlit app
        self.dg._enqueue("anyWidget", anywidget_proto)

        # Return a WidgetValue for accessing the current value
        return WidgetValue(widget_id, widget_state)

    def _extract_serializable_data(self, widget_obj):
        """Extract serializable data from a widget object, handling special cases."""
        print("widget_obj: ", widget_obj)
        # For anywidget, we need to extract the state
        if hasattr(widget_obj, "_model_state"):
            # Most anywidget implementations have this attribute
            return self._make_serializable(widget_obj._model_state)

        # For direct trait/value access
        if hasattr(widget_obj, "_trait_values"):
            try:
                traits = {}
                for key, value in widget_obj._trait_values.items():
                    if not key.startswith("_") and key != "comm":
                        traits[key] = value
                return self._make_serializable(traits)
            except:
                pass

        # For direct data attribute (common pattern)
        if hasattr(widget_obj, "data"):
            return {"data": self._make_serializable(widget_obj.data)}

        # For Pydantic models
        if hasattr(widget_obj, "model_dump"):
            try:
                return self._make_serializable(widget_obj.model_dump())
            except:
                pass

        if hasattr(widget_obj, "dict"):
            try:
                return self._make_serializable(widget_obj.dict())
            except:
                pass

        # Fallback: try to get all public attributes
        return self._make_serializable(
            {
                attr: getattr(widget_obj, attr)
                for attr in dir(widget_obj)
                if not attr.startswith("_") and not callable(getattr(widget_obj, attr))
            }
        )

    def _make_serializable(self, data):
        """Convert data to a JSON-serializable format."""
        if data is None:
            return None

        if isinstance(data, (str, int, float, bool, type(None))):
            return data

        if isinstance(data, (list, tuple)):
            return [self._make_serializable(item) for item in data]

        if isinstance(data, dict):
            return {
                str(k): self._make_serializable(v)
                for k, v in data.items()
                if not isinstance(k, str)
                or not k.startswith("_")  # Skip private attributes
            }

        # Handle common types from numpy and pandas if available
        module_name = type(data).__module__
        if module_name == "numpy":
            try:
                return data.tolist()
            except:
                return str(data)

        if module_name.startswith("pandas"):
            try:
                return json.loads(data.to_json())
            except:
                return str(data)

        # Skip non-serializable objects like DummyComm
        if module_name == "ipykernel.comm" or type(data).__name__ == "DummyComm":
            return None

        # Try to convert to dict if the object has a __dict__
        if hasattr(data, "__dict__"):
            try:
                return self._make_serializable(vars(data))
            except:
                pass

        # Last resort: convert to string
        try:
            return str(data)
        except:
            return None

    @property
    def dg(self) -> DeltaGenerator:
        """Get the DeltaGenerator for this mixin"""
        return cast(DeltaGenerator, self)
