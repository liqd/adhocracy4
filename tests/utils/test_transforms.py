from adhocracy4 import transforms


def test_clean_html_all():
    input_html = (
        "<h2>A free platform from a non-profit " "association</h2><p><br/></p> "
    )
    expected = "A free platform from a non-profit association\n "
    sanitized = transforms.clean_html_all(input_html)
    assert sanitized == expected


def test_clean_html():
    input_html = """<p><b>Non-profit &amp; Open Source</b></p><p>The platform is developed and operated by Liquid Democracy, a non-profit association from Berlin. The code is in the public domain.</p><p><br/></p>
<div class="block-col_cta-content">
<a href="https://adhocracy.plus/info/features" class="btn btn--full btn--transparent">More about features and functions</a>
</div>"""  # noqa: E501
    expected = """<p>Non-profit &amp; Open Source</p><p>The platform is developed and operated by Liquid Democracy, a non-profit association from Berlin. The code is in the public domain.</p><p></p>
\n\n<a href="https://adhocracy.plus/info/features">More about features and functions</a>\n"""  # noqa: E501
    sanitized = transforms.clean_html_field(input_html)
    assert sanitized == expected


def test_clean_style():
    input_html = '<p style="color:red; margin: 5px">A red paragraph.</p>'
    expected = "<p>A red paragraph.</p>"
    sanitized = transforms.clean_html_field(input_html)
    assert sanitized == expected


def test_clean_style_keep_margin():
    input_html = (
        '<img src="smiley.gif" alt="Smiley face" width="42" '
        'height="42" style="vertical-align:middle;margin:0px 50px"> '
    )
    expected = '<img src="smiley.gif" alt="Smiley face" style="margin:0px ' '50px;"> '
    sanitized = transforms.clean_html_field(input_html, setting="image-editor")
    assert sanitized == expected
