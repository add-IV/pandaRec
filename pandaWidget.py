import ipywidgets as widgets
from traitlets import Unicode

class PandaWidget(widgets.DOMWidget):
    _view_name = Unicode('PandaView').tag(sync=True)
    _view_module = Unicode('pandaWidget').tag(sync=True)
    _view_module_version = Unicode('0.1.0').tag(sync=True)

    value = Unicode('Hello World!').tag(sync=True)