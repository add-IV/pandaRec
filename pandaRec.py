from ipydatagrid import DataGrid


class MyGrid(DataGrid):
    def __init__(self, dataframe, **kwargs):
        super().__init__(dataframe, **kwargs)
