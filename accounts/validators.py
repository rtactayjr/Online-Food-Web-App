from django.core.exceptions import ValidationError
import os


def allow_only_images_validator(value):
    # Get the file extension from the file name (e.g., '.jpg' from 'cover-image.jpg')
    ext = os.path.splitext(value.name)[1]

    # List of valid image file extensions
    valid_extensions = ['.png', '.jpg', '.jpeg']

    # Check if the file extension is in the list of valid extensions
    if not ext.lower() in valid_extensions:
        # Raise a ValidationError if the extension is not valid
        raise ValidationError('Unsupported file extension. Allowed extensions: ' + str(valid_extensions))
