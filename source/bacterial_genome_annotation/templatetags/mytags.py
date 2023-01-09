from django import template

register = template.Library()

@register.filter(name='replaceWithSpace')
def replaceWithSpace(value, arg):
    return value.replace(arg, ' ')

@register.filter(name='capsAfterSpace')
def capsAfterSpace(value):
    for i in range(len(value)-1):
        if value[i]==' ':
            value=value[:i+1]+value[i+1].upper()+value[i+2:]
    return value
