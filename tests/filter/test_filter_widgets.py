from adhocracy4.filters import widgets


def test_render_dropdown_link_widget_without_choices():
    widget = widgets.DropdownLinkWidget()
    html = widget.render('test_filter', 'test_val1', attrs={'id': 'test_id'})

    assert len(widget.choices) == 0
    assert '' == html


def test_render_dropdown_link_widget():

    choices = (
        ('test-val1', 'test-label1'),
        ('test-val2', 'test-label2'),
    )
    widget = widgets.DropdownLinkWidget(choices=choices)
    html = widget.render('test_filter', 'test_val1', attrs={'id': 'test_id'})

    assert len(widget.choices) == 2
    assert ('<li><a href="?test_filter=test-val1">test-label1</a></li>\n'
            '<li><a href="?test_filter=test-val2">test-label2</a></li>'
            in html)


def test_free_text_filter_widget():
    name = 'test_filter'
    data = {
        'test_filter': 'value',
        'other': 'other_value',
    }

    widget = widgets.FreeTextFilterWidget()
    value = widget.value_from_datadict(data, [], name)
    html = widget.render(name, value, attrs={'id': 'test_id'})

    assert 'value' == value
    assert '<input type="hidden" name="other" value="other_value">' in html
    assert ('<input class="search-filter-input" id="test_id" type="search" '
            'name="test_filter" value="value">'
            in html)
