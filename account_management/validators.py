import re

from django.core.exceptions import ValidationError

def validate_username(value):
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{1,}[a-zA-Z0-9]", value):
        raise ValidationError(
            "Username can only contain latin letters, numbers, and can't start or end with special symbols like '_' and '-'.",
            code="invalid_username",
        )


custom_username_validators = [validate_username]