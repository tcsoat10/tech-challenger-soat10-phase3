# from tests.factories.payment_method_factory import PaymentMethodFactory
# from tests.factories.payment_status_factory import PaymentStatusFactory
# from src.constants.permissions import PaymentPermissions
# from tests.factories.payment_factory import PaymentFactory

# from fastapi import status


# def test_create_payment_success(client):
#     payment_method = PaymentMethodFactory()
#     payment_status = PaymentStatusFactory()

#     payload = {'payment_method_id': payment_method.id, "payment_status_id": payment_status.id}

#     response = client.post('/api/v1/payments', json=payload, permissions=[PaymentPermissions.CAN_CREATE_PAYMENT])
#     assert response.status_code == status.HTTP_201_CREATED

#     data = response.json()
#     assert 'id' in data
#     assert data['payment_method']['id'] == payment_method.id
#     assert data['payment_status']['id'] == payment_status.id


# def test_get_payment_by_id_success(client):
#     payment = PaymentFactory()

#     response = client.get(f'/api/v1/payments/{payment.id}/id', permissions=[PaymentPermissions.CAN_VIEW_PAYMENTS])
#     assert response.status_code == status.HTTP_200_OK

#     data = response.json()

#     assert 'id' in data
#     assert data['id'] == payment.id
#     assert data['payment_method']['id'] == payment.payment_method_id
#     assert data['payment_status']['id'] == payment.payment_status_id


# def test_get_payments_by_method_id_success(client):
#     method = PaymentMethodFactory()
#     payment1 = PaymentFactory(payment_method=method)
#     payment2 = PaymentFactory(payment_method=method)
#     payment3 = PaymentFactory()

#     response = client.get(
#         f'/api/v1/payments/{method.id}/method_id', permissions=[PaymentPermissions.CAN_VIEW_PAYMENTS]
#     )
#     assert response.status_code == status.HTTP_200_OK

#     data = response.json()
#     assert len(data) == 2
#     assert data == [
#         {
#             'id': payment1.id,
#             'payment_method': {
#                 'id': method.id,
#                 'name': method.name,
#                 'description': method.description
#             },
#             'payment_status': {
#                 'id': payment1.payment_status.id,
#                 'name': payment1.payment_status.name,
#                 'description': payment1.payment_status.description
#             }
#         },
#         {
#             'id': payment2.id,
#             'payment_method': {
#                 'id': method.id,
#                 'name': method.name,
#                 'description': method.description
#             },
#             'payment_status': {
#                 'id': payment2.payment_status.id,
#                 'name': payment2.payment_status.name,
#                 'description': payment2.payment_status.description
#             }
#         }
#     ]


# def test_get_payments_by_status_id_success(client):
#     payment_status = PaymentStatusFactory()
#     payment1 = PaymentFactory(payment_status=payment_status)
#     payment2 = PaymentFactory(payment_status=payment_status)
#     payment3 = PaymentFactory()

#     response = client.get(
#         f'/api/v1/payments/{payment_status.id}/status_id', permissions=[PaymentPermissions.CAN_VIEW_PAYMENTS]
#     )
#     assert response.status_code == status.HTTP_200_OK

#     data = response.json()
#     assert len(data) == 2
#     assert data == [
#         {
#             'id': payment1.id,
#             'payment_method': {
#                 'id': payment1.payment_method.id,
#                 'name': payment1.payment_method.name,
#                 'description': payment1.payment_method.description
#             },
#             'payment_status': {
#                 'id': payment_status.id,
#                 'name': payment_status.name,
#                 'description': payment_status.description
#             }
#         },
#         {
#             'id': payment2.id,
#             'payment_method': {
#                 'id': payment2.payment_method.id,
#                 'name': payment2.payment_method.name,
#                 'description': payment2.payment_method.description
#             },
#             'payment_status': {
#                 'id': payment_status.id,
#                 'name': payment_status.name,
#                 'description': payment_status.description
#             }
#         }
#     ]


# def test_get_all_payments(client):
#     payment1 = PaymentFactory()
#     payment2 = PaymentFactory()

#     response = client.get('/api/v1/payments', permissions=[PaymentPermissions.CAN_VIEW_PAYMENTS])
#     assert response.status_code == status.HTTP_200_OK

#     data = response.json()
#     assert len(data) == 2
#     assert data == [
#         {
#             'id': payment1.id,
#             'payment_method': {
#                 'id': payment1.payment_method.id,
#                 'name': payment1.payment_method.name,
#                 'description': payment1.payment_method.description
#             },
#             'payment_status': {
#                 'id': payment1.payment_status.id,
#                 'name': payment1.payment_status.name,
#                 'description': payment1.payment_status.description
#             }
#         },
#         {
#             'id': payment2.id,
#             'payment_method': {
#                 'id': payment2.payment_method.id,
#                 'name': payment2.payment_method.name,
#                 'description': payment2.payment_method.description
#             },
#             'payment_status': {
#                 'id': payment2.payment_status.id,
#                 'name': payment2.payment_status.name,
#                 'description': payment2.payment_status.description
#             }
#         }
#     ]


# def test_update_payment_success(client):
#     payment = PaymentFactory()
#     method = PaymentMethodFactory()
#     payment_status = PaymentStatusFactory()
    
#     payload = {'id': payment.id, 'payment_method_id': method.id, 'payment_status_id': payment_status.id}

#     response = client.put(
#         f'/api/v1/payments/{payment.id}', json=payload, permissions=[PaymentPermissions.CAN_UPDATE_PAYMENT]
#     )
#     assert response.status_code == status.HTTP_200_OK


#     data = response.json()
#     assert data == {
#         'id': payment.id,
#             'payment_method': {
#                 'id': method.id,
#                 'name': method.name,
#                 'description': method.description
#             },
#             'payment_status': {
#                 'id': payment_status.id,
#                 'name': payment_status.name,
#                 'description': payment_status.description
#             }
#     }
        

# def test_delete_payment_success(client):
#     payment = PaymentFactory()
#     payment_delete = PaymentFactory()

#     response = client.delete(
#         f'/api/v1/payments/{payment_delete.id}',
#         permissions=[PaymentPermissions.CAN_DELETE_PAYMENT]
#     )
#     assert response.status_code == status.HTTP_204_NO_CONTENT

#     response = client.get('/api/v1/payments', permissions=[PaymentPermissions.CAN_VIEW_PAYMENTS])
#     assert response.status_code == status.HTTP_200_OK

#     data = response.json()
#     assert data == [{
#         'id': payment.id,
#             'payment_method': {
#                 'id': payment.payment_method.id,
#                 'name': payment.payment_method.name,
#                 'description': payment.payment_method.description
#             },
#             'payment_status': {
#                 'id': payment.payment_status.id,
#                 'name': payment.payment_status.name,
#                 'description': payment.payment_status.description
#             }
#     }]
    