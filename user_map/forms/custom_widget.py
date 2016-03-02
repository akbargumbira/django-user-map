from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.forms.widgets import ClearableFileInput, Input, CheckboxInput


class CustomClearableFileInput(ClearableFileInput):
    """A custom ClearableFileInput widget.

    ..note:: Adapted from django.forms.widgets.ClearableFileInput and also
        utilising img-responsive bootstrap class.
    """
    def render(self, name, value, attrs=None):
        """Render the custom widget."""
        substitutions = {
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
            }
        template = '%(input)s'
        substitutions['input'] = Input.render(self, name, value, attrs)

        if value and hasattr(value, "url"):
            template = ('%(initial)s %(clear_template)s<br />%(input_text)s: '
                        '%(input)s')
            substitutions['initial'] = (
                '<img class="img-responsive" src="%s" alt="%s"/>' % (
                    escape(value.url), escape(force_unicode(value))))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(
                    checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(
                    checkbox_id)
                substitutions['clear'] = CheckboxInput().render(
                    checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = \
                    self.template_with_clear % substitutions
        return mark_safe(template % substitutions)
