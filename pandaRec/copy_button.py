def copy_button_html(copy_text=""):
    return """
<style>
    .copy_button:active {{
        background-color: var(--jp-success-color1);
    }}
</style>
<button class="copy_button" onclick=navigator.clipboard.writeText('{}') icon="copy">
    Copy
</button>
""".format(
        copy_text
    )
