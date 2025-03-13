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

import json
from collections.abc import Iterable
from typing import Any, Dict, Literal, Optional, Union, cast

from streamlit.delta_generator import DeltaGenerator
from streamlit.elements.arrow import marshall
from streamlit.elements.lib.form_utils import current_form_id
from streamlit.elements.lib.policies import check_widget_policies
from streamlit.elements.lib.utils import Key, compute_and_register_element_id, to_key
from streamlit.elements.lib.vega_lite_chart_utils import (
    VegaLiteChartSelectionSerde,
    VegaLiteChartState,
    parse_selection_mode,
)
from streamlit.errors import StreamlitAPIException
from streamlit.proto.ArrowVegaLiteChart_pb2 import (
    ArrowVegaLiteChart as ArrowVegaLiteChartProto,
)
from streamlit.runtime.scriptrunner_utils.script_run_context import (
    get_script_run_ctx,
    register_widget,
)
from streamlit.runtime.state import WidgetCallback
from streamlit.type_util import Data


def arrow_vega_lite_chart(
    self,
    data: Data = None,
    spec: Union[None, Dict[str, Any], str] = None,
    use_container_width: bool = False,
    theme: Union[None, Literal["streamlit"]] = "streamlit",
    key: Optional[Key] = None,
    on_select: Union[Literal["ignore", "rerun"], WidgetCallback] = "ignore",
    selection_mode: Union[str, Iterable[str]] = "multi",
    alt_text: Optional[str] = None,
) -> DeltaGenerator:
    """Display a chart using the Vega-Lite library.

    Parameters
    ----------
    data : pandas.DataFrame, pandas.Styler, pyarrow.Table, numpy.ndarray, pyspark.sql.DataFrame, snowflake.snowpark.DataFrame, Iterable, dict, or None
        The data to be plotted.

    spec : dict or string
        The Vega-Lite spec for the chart. If a string is supplied, it will be
        parsed as JSON. See https://vega.github.io/vega-lite/docs/ for more info.

    use_container_width : bool
        If True, set the chart width to the column width. This takes
        precedence over Vega-Lite's native `width` value.

    theme : "streamlit" or None
        The theme of the chart. Currently, we only support "streamlit" for the
        streamlit theme or None for the default Vega-Lite theme.
        More themes will be added in the future.

    key : str or int
        An optional string or integer to use as the unique key for the widget.
        If this is omitted, a key will be generated based on the widget's
        content. Multiple widgets of the same type may not share the same key.

    on_select : "ignore" or "rerun" or callable
        How the chart should respond to user selection events. This
        controls whether or not the chart behaves like an input widget.
        ``on_select`` can be one of the following:

        - ``"ignore"`` (default): Streamlit will not react to any selection
          events in the chart. The chart will not behave like an input widget.

        - ``"rerun"``: Streamlit will rerun the app when the user selects
          points in the chart. In this case, ``st.vega_lite_chart`` will
          return the selection data as a dictionary.

        - A ``callable``: Streamlit will rerun the app and execute the
          ``callable`` as a callback function before the rest of the app.
          In this case, ``st.vega_lite_chart`` will return the selection
          data as a dictionary.

    selection_mode : str or Iterable of str
        The types of selections Streamlit should allow when selections are
        enabled with ``on_select``. This can be one of the following:

        - "multi" (default): Multiple points can be selected at a time.
        - "single": Only one point can be selected at a time.
        - An ``Iterable`` of the above options: The chart will allow
          selection based on the modes specified.

    alt_text : str or None
        Alternative text for screen readers. If this is None (default), no alt
        text is displayed.

    Returns
    -------
    DeltaGenerator
        The DeltaGenerator object for the chart.

    Example
    -------
    >>> import streamlit as st
    >>> import pandas as pd
    >>> import numpy as np
    >>>
    >>> chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    >>>
    >>> st.vega_lite_chart(
    ...     chart_data,
    ...     {
    ...         "mark": {"type": "circle", "tooltip": True},
    ...         "encoding": {
    ...             "x": {"field": "a", "type": "quantitative"},
    ...             "y": {"field": "b", "type": "quantitative"},
    ...             "size": {"field": "c", "type": "quantitative"},
    ...             "color": {"field": "c", "type": "quantitative"},
    ...         },
    ...     },
    ... )

    .. output::
       https://doc-vega-lite-chart.streamlit.app/
       height: 400px

    """
    key = to_key(key)
    is_selection_activated = on_select != "ignore"

    if is_selection_activated:
        # Run some checks that are only relevant when selections are activated
        is_callback = callable(on_select)
        check_widget_policies(
            self.dg,
            key,
            on_change=cast(WidgetCallback, on_select) if is_callback else None,
            default_value=None,
            writes_allowed=False,
            enable_check_callback_rules=is_callback,
        )

    if theme not in (None, "streamlit"):
        raise StreamlitAPIException(
            f'You set theme="{theme}", but the only supported themes are None '
            'and "streamlit".'
        )

    if data is None and spec is None:
        return self.dg

    if data is not None and not isinstance(data, dict):
        # Check if the data is from Vega datasets
        if not isinstance(data, (list, tuple)):
            data = [("data", data)]

    proto = ArrowVegaLiteChartProto()

    if data is None:
        pass
    elif isinstance(data, (list, tuple)):
        # Add datasets to the proto
        for name, dataset in data:
            wrapped_dataset = proto.datasets.add()
            wrapped_dataset.name = name
            marshall(wrapped_dataset.data, dataset)
    elif isinstance(data, dict):
        # Add the dict as the main data source
        marshall(proto.data, data)
    else:
        # Add the data as the main data source
        marshall(proto.data, data)

    if isinstance(spec, str):
        proto.spec = spec
    elif isinstance(spec, dict):
        proto.spec = json.dumps(spec)
    elif spec is None:
        proto.spec = "{}"
    else:
        raise StreamlitAPIException(f"Unsupported type {type(spec)} for argument spec.")

    proto.use_container_width = use_container_width
    proto.theme = theme or ""

    if is_selection_activated:
        # If selection events are activated, we need to register the chart
        # element as a widget.
        proto.selection_mode.extend(parse_selection_mode(selection_mode))
        proto.form_id = current_form_id(self.dg)

        ctx = get_script_run_ctx()
        proto.id = compute_and_register_element_id(
            "vega_lite_chart",
            user_key=key,
            form_id=proto.form_id,
            data=proto.data,
            spec=proto.spec,
            use_container_width=use_container_width,
            theme=theme,
            selection_mode=selection_mode,
            is_selection_activated=is_selection_activated,
        )

        serde = VegaLiteChartSelectionSerde()
        widget_state = register_widget(
            proto.id,
            on_change_handler=on_select if callable(on_select) else None,
            deserializer=serde.deserialize,
            serializer=serde.serialize,
            ctx=ctx,
            value_type="string_value",
        )
        self.dg._enqueue("arrow_vega_lite_chart", proto)
        return cast(VegaLiteChartState, widget_state.value)
    else:
        return self.dg._enqueue("arrow_vega_lite_chart", proto)
