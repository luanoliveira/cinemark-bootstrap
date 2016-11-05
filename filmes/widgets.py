# encoding: utf-8
from django.forms.widgets import Widget, TextInput, Select
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, format_html, html_safe
from django.forms.utils import flatatt, to_current_timezone
from django.utils.encoding import (
    force_str, force_text, python_2_unicode_compatible,
)


class TagInput(TextInput):
    def __init__(self, attrs=None):
        attrs = {
            'class': 'form-control tagsinput',
        }
        super(TagInput, self).__init__(attrs)

    def format_value(self, value):
        
        if ( isinstance(value, basestring) ):
            return value
            
        tags = []
        
        for tag in value:
            tags.append(tag.titulo)

        return ','.join(tags)

 
class ChannelWidget(Widget):
   input_type = None

   def __init__(self, attrs=None, required=True):
      self.attrs = attrs or {}
      self.required = required

   def format_value(self, value):
      if self.is_localized:
         return formats.localize_input(value)
      return value

   def render(self, name, value, attrs=None):
      if value is None:
         value = ''
      final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
      if value != '':
         # Only add the 'value' attribute if a value is non-empty.
         final_attrs['value'] = force_text(self.format_value(value))
      return format_html('<input{} />', flatatt(final_attrs))

   '''
   def create_input(self, name, field, val):
      local_attrs = self.build_attrs()
      input_text = TextInput()
      input_text.attrs = {"style": "width:69% !important;"}
      return input_text.render(field, val, local_attrs)

   def create_select(self, name, field, val):
      local_attrs = self.build_attrs()
      select = Select()
      select.attrs = {"style": "width:auto;"}
      select.choices = tuple([(c, c) for c in self.choices])
      return select.render(field, val, local_attrs)
   '''