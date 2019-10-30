import time

from django import template
from django.template.loader import render_to_string
from html5lib import parseFragment
from html5lib.serializer import serialize

register = template.Library()


@register.filter
def transform_collapsibles(text):
    """Find simple collapsible elements and transform them to full html."""
    tree = parseFragment(text, container='div', treebuilder='etree',
                         namespaceHTMLElements=False)

    base_id = ''.join(filter(str.isdigit, str(time.time())))
    collapsibles = tree.findall('./div[@class="collapsible-item"]')
    for i, collapsible in enumerate(collapsibles):
        title = collapsible.find('./div[@class="collapsible-item-title"]')
        body = collapsible.find('./div[@class="collapsible-item-body"]')

        if title is not None and body is not None:
            title.tag = 'span'
            del title.attrib['class']

            body.tag = 'div'
            del body.attrib['class']

            final_html = render_to_string(
                'a4ckeditor/collapsible_fragment.html',
                dict(
                    id='a4ckeditor-collapsible-{}_{}'.format(base_id, i),
                    title=serialize(title),
                    body=serialize(body))
            )

            collapsible.clear()
            collapsible.append(parseFragment(final_html, treebuilder='etree',
                                             namespaceHTMLElements=False))

    return serialize(tree)
