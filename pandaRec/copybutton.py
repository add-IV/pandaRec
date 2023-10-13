import ipywidgets as widgets
import pyperclip
from threading import Timer


def copybutton(text, html=False):
    if html:
        return HTMLCopyButton(text)
    else:
        return CopyButton(text)


class CopyButton(widgets.Button):
    def __init__(self, copytext):
        super().__init__()
        self.description = "Copy"
        self.icon = "copy"
        self.copytext = copytext
        self.timer = None
        self.on_click(self.copy)

    def set_copytext(self, copytext):
        self.copytext = copytext

    def copy(self, _self2):
        if self.timer:
            self.timer.cancel()
        pyperclip.copy(self.copytext)
        self._set_style_success()
        self.timer = Timer(0.5, self._set_style_normal).start()

    def _set_style_normal(self):
        self.button_style = ""
        self.icon = "copy"

    def _set_style_success(self):
        self.button_style = "success"
        self.icon = "check"


class HTMLCopyButton(widgets.HTML):
    def __init__(self, copytext):
        self.copytext = copytext
        self.set_copytext(copytext)
        self.timer = None

    def set_copytext(self, copytext):
        self.copytext = copytext
        self.value = """
        <button onclick=navigator.clipboard.writeText('{}') icon="copy">
            Copy
        </button>
        """.format(
            copytext
        )
