from django.core.exceptions import ValidationError


def validate_response(value):
    response_text = value
    if response_text == "":
        raise ValidationError("Rehsponse can not be empty")
    return response_text
