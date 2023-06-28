from django import template

register = template.Library()

@register.filter
def addattrs(field, css):
    attrs = {}
    definition = css.split(';')

    for d in definition:
        parts = d.split('=')
        if len(parts) == 2:
            attr, val = parts
            attrs[attr] = val

    return field.as_widget(attrs=attrs)

