from pandaRec.copy_button import copy_button_html

def test_copy_button_html():
    copy_button = copy_button_html("test")
    assert "<button class=\"copy_button\"" in copy_button
    assert "onclick=navigator.clipboard.writeText('{}')".format("test") in copy_button
