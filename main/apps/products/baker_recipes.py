from model_bakery.recipe import Recipe
from .models import Product

product = Recipe(
    Product,
    value=1,
    evaluation=3,
)
