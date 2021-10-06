from model_bakery.recipe import Recipe, foreign_key
from .models import PortfolioValue
from ..portfolio.baker_recipes import portfolio

portfolio_value = Recipe(
    PortfolioValue,
    portfolio=foreign_key(portfolio),
)
