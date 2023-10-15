
def path_to_upload_img(instance, filename):
    """Creates path for uploaded image."""
    return f"{instance.user.id}/images/{instance.id}/{filename}"
