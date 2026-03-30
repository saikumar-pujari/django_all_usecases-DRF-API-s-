from django import template
register = template.Library()


@register.filter
def sai(value: str) -> str:
    return value.upper()


@register.simple_tag
def add(a: int, b: int) -> int:
    return a + b


@register.inclusion_tag('inclusion_tag.html')
def show_colors(colors):
    return {"colors": colors}
