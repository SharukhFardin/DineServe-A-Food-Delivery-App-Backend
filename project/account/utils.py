"""All the helper methods for the account app will be stored here"""


def get_slug_full_name(instance):
    """Takes the User instance and returns a string consiting full name, for slug"""
    return f"{instance.first_name} {instance.last_name}".strip()
