from tests.factories.order_factory import OrderFactory
from tests.factories.payment_factory import PaymentFactory
from src.constants.permissions import OrderPaymentPermissions

from fastapi import status


def test_create_order_payment_success(client):
    order = OrderFactory()
    payment = PaymentFactory()
    payload = {'order_id': order.id, 'payment_id': payment.id}

    response = client.post('/api/v1/order_payments', json=payload, permissions=[OrderPaymentPermissions.CAN_CREATE_ORDER_PAYMENT])
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert 'id' in data
    assert data['payment']['id'] == payment.id
    assert data['order']['id'] == order.id