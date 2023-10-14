import ipywidgets as widgets

widgets.Button

def copy_button_html(copytext=""):
    return """
<style>
    .copybutton:active {{
        background-color: var(--jp-success-color1);
    }}
</style>
<button class="copybutton" onclick=navigator.clipboard.writeText('{}') icon="copy">
    Copy
</button>
""".format(
        copytext
    )
