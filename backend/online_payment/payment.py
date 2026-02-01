import os
import sys
import uuid
from pathlib import Path
from dotenv import load_dotenv
from yookassa import Configuration
from yookassa.domain.common.user_agent import Version
from yookassa import Payment

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from orders.models import Order

load_dotenv()
check_env = os.getenv("ENV_CHECK")
if not check_env:
    raise FileNotFoundError(".env file not found")

shop_id = os.getenv("SHOP_ID")
shop_api_key = os.getenv("SHOP_API_KEY")

Configuration.account_id = shop_id
Configuration.secret_key = shop_api_key
Configuration.configure_user_agent(framework=Version("Django", "5.03"))


class YooKassaPayment:
    def __init__(self):
        pass

    def online_payment(self, order: Order):
        return Payment.create(
            {
                "amount": {"value": order.total_cost, "currency": "RUB"},
                "confirmation": {
                    "type": "redirect",
                    "return_url": "https://delivery.itomilov.tech/orders/list/",
                },
                "capture": True,
                "description": f"Заказ №{order.id}",
                "metadata": {"order_uuid": str(order.uuid)},
                "test": True,
            },
            idempotency_key=str(uuid.uuid4()),
        )


yookassa_payment = YooKassaPayment()
