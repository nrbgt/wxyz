""" Jupyter Widgets for `@phosphor/datagrid`
[0.1.6]: https://github.com/phosphorjs/phosphor/blob/cdb412e9dfb/packages/datagrid/src

Notes:
- a future implementation would split the grid from the data source
"""
# pylint: disable=R0903,C0103,W0703,R0901
import json

import pandas as pd
import traittypes as TT

from wxyz.core.base import Base, T, W

TABLE = {"orient": "table"}

dataframe_serialization = dict(
    to_json=lambda df, obj: None if df is None else df.to_dict(orient="table"),
    from_json=lambda value, obj: None if value is None else pd.DataFrame(value),
)


@W.register
class DataGrid(Base, W.Box):
    """ An (overly) opinionated DataFrame-backed datagrid
        [0.1.6]/datagrid.ts#L64

        Used JSONModel, which expect JSON Table Schema
        [0.1.6]/jsonmodel.ts#L21
    """

    _model_name = T.Unicode("DataGridModel").tag(sync=True)
    _view_name = T.Unicode("DataGridView").tag(sync=True)

    value = TT.DataFrame(None, allow_none=True).tag(
        sync=True,
        to_json=lambda df, obj: None if df is None else json.loads(df.to_json(**TABLE)),
        from_json=lambda value, obj: None
        if value is None
        else pd.read_json(json.dumps(value), **TABLE),
    )

    def _repr_keys(self):
        """ this shouldn't be needed, but we're doing _something wrong_
        """
        try:
            super_keys = super(DataGrid, self)._repr_keys()
            for key in super_keys:
                if key != "value":
                    yield key
        except Exception:
            return