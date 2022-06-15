from django import template

register = template.Library()


@register.filter
def new_debt(total_debt, proceeds):
    return total_debt - proceeds