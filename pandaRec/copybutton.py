import ipywidgets as widgets
from IPython.display import display, HTML
import pyperclip
from threading import Timer


def copybutton(text, html=False):
    if html:
        return HTMLCopyButton(text).get_widget()
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


class HTMLCopyButton(object):
    def __init__(self, copytext):
        self.description = "Copy"
        self.icon = "copy"
        self.copytext = copytext
        self.timer = None

    def get_widget(self):
        buttontext = """
        <button onclick="copyToClipboard(this)" icon="copy" data-copytext="{}">
            Copy
        </button>
        """
        return widgets.HTML(buttontext.format(self.copytext))

    def _setup_copy_script(self):
        display(
            HTML(
                """
        <script>
        function copyToClipboard(button) {
            var dummy = document.createElement("textarea");
            document.body.appendChild(dummy);
            dummy.value = button.getAttribute('data-copytext');
            dummy.select();
            document.execCommand("copy");
            document.body.removeChild(dummy);
        }
        </script>
        """
            )
        )
