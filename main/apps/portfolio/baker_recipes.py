from model_bakery.recipe import Recipe
from .models import Portfolio
from ..categories.models import Category

portfolio = Recipe(
    Portfolio,
    units=1,
)

bank_account = portfolio.extend(
    category=Category.get_bank_account(),
)

bond = portfolio.extend(
    category=Category.get_bond(),
)

saving_account = portfolio.extend(
    category=Category.get_saving_account(),
)

term_account = portfolio.extend(
    category=Category.get_term_account(),
)

building_saving = portfolio.extend(
    category=Category.get_building_saving(),
)

pension_saving = portfolio.extend(
    category=Category.get_pension_saving(),
)

stock = portfolio.extend(
    category=Category.get_stock(),
)

crypto = portfolio.extend(
    category=Category.get_crypto(),
)

commodity = portfolio.extend(
    category=Category.get_commodity(),
)

share_etf = portfolio.extend(
    category=Category.get_share_etf(),
)
