import stripe
from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY

def create_stipe_price(amount):
    """Создание стоимости для оплаты через страйп"""

    stripe.Price.create(
        currency="usd",
        unit_amount=amount,
        product_data={"name": "Gold Plan"},
    )
