import stripe
from forex_python.converter import CurrencyRates

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_usd(amount):
    """Конвертор валюты"""

    c = CurrencyRates()
    rate = c.get_rate("RUB", "USD")
    return int(amount * rate)


def create_stipe_price(amount, course_name):
    """Создание стоимости для оплаты через страйп"""

    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": course_name},
    )


def create_stripe_session(price):
    """Создает сессию на оплату в страйпе"""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )

    return session.get("id"), session.get("url")
