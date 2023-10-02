from django import template

register = template.Library()

@register.filter
def format_cnpj(value):
    return f"{value[:2]}.{value[2:5]}.{value[5:8]}/{value[8:12]}-{value[12:14]}"

@register.filter(name='replace_pipe')
def replace_pipe(value):
    return value.replace('|', '<br>')