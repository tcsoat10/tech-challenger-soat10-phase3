from tests.factories.order_factory import OrderFactory
from tests.factories.payment_factory import PaymentFactory
from src.constants.permissions import OrderPaymentPermissions
from tests.factories.order_payment_factory import OrderPaymentFactory

from fastapi import status


def test_create_order_payment_success(client):
    order = OrderFactory()
    payment = PaymentFactory()
    payload = {'order_id': order.id, 'payment_id': payment.id}

    response = client.post('/api/v1/order_payments', json=payload, permissions=[OrderPaymentPermissions.CAN_CREATE_ORDER_PAYMENT])
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert 'id' in data
    assert data['order']['id'] == order.id
    assert data['payment']['id'] == payment.id    


def test_get_order_payment_by_id_success(client):
    order_payment = OrderPaymentFactory()

    response = client.get(
        f'/api/v1/order_payments/{order_payment.id}/id', permissions=[OrderPaymentPermissions.CAN_VIEW_ORDER_PAYMENTS]
    )
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['id'] == order_payment.id
    assert data['order']['id'] == order_payment.order_id
    assert data['payment']['id'] == order_payment.payment_id
    