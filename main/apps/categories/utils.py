from main.apps.categories.models import Category


def get_category_name(category_slug: str) -> str:
    obj = Category.get_category_dict().get(category_slug)
    if obj is None:
        raise Category.DoesNotExist()
    return obj.name
