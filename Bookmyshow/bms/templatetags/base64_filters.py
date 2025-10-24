import base64
from django import template

register = template.Library()

@register.filter
def b64encode(image):
    return base64.b64encode(image.getvalue()).decode()
