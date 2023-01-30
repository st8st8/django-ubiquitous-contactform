from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_empty(value):
    if len(value.strip()) > 0:
        raise ValidationError(
            _('%(value)s is not empty'),
            params={'value': value},
        )