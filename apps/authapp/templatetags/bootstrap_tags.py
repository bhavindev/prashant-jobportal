from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})

@register.filter
def add_name(field, atrname):
    return field.as_widget(attrs={'name': atrname})

@register.filter
def mul(value, arg):
    return value * arg

@register.filter(name='attr')
def attr(field, attribute):
    attr_name, attr_value = attribute.split('=') 
    attrs = {attr_name: attr_value}
    return field.as_widget(attrs=attrs)


@register.filter
def stars_range(value):
    return range(value)


@register.filter(name='filter_time')
def filter_time(value):
    if not value:
        return ''
    
    try:
        late_time_parts = value.split(':')
        late_hours = int(late_time_parts[0])
        late_minutes = int(late_time_parts[1])
        
        formatted_time = f'{late_hours} hours {late_minutes} minutes'
        return formatted_time
    except (ValueError, IndexError):
        return value
    
    
@register.filter
def subtract(value, arg):
    """Subtracts arg from value."""
    value = float(value)
    arg = float(arg)
    return value - arg