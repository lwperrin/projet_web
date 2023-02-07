from django import template

register = template.Library()


@register.filter(name='replaceWithSpace')
def replaceWithSpace(value, arg):
    return value.replace(arg, ' ')


@register.filter(name='capsAfterSpace')
def capsAfterSpace(value):
    for i in range(len(value) - 1):
        if value[i] == ' ':
            value = value[:i + 1] + value[i + 1].upper() + value[i + 2:]
    return value


@register.filter(name='replaceHyphens')
def replaceHyphens(value):
    return value.replace('-', '.')


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()
