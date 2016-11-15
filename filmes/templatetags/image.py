from django import template

register = template.Library()

@register.filter
def image_path(value, path):
  return "/".join(value.split("/")[:-1])+path+"".join(value.split("/")[-1:])