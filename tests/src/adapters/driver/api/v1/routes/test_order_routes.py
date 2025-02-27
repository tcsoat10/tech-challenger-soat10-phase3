from fastapi import status

from src.constants.product_category import ProductCategoryEnum
from src.constants.order_status import OrderStatusEnum
from tests.factories.category_factory import CategoryFactory
from tests.factories.customer_factory import CustomerFactory
from tests.factories.employee_factory import EmployeeFactory
from tests.factories.order_factory import OrderFactory
from tests.factories.order_item_factory import OrderItemFactory
from tests.factories.order_status_factory import OrderStatusFactory
from tests.factories.person_factory import PersonFactory
from src.constants.permissions import OrderPermissions
from tests.factories.product_factory import ProductFactory


def test_create_order_success(client, populate_order_status):
    # person = PersonFactory(cpf="12345678901", name="JOÃO", email="joao@gmail.com")
    # customer = CustomerFactory(person=person)
    # order_status = OrderStatusFactory()
    # employee = EmployeeFactory()

    # payload = {
    #     "id_customer": customer.id
    # }

    person = PersonFactory()
    CustomerFactory(person=person)

    response = client.post(
        "/api/v1/orders",
        permissions=[OrderPermissions.CAN_CREATE_ORDER],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    
    assert "id" in data
    assert data["customer"]["person"]["cpf"] == person.cpf
    assert data["customer"]["person"]["name"] == person.name
    assert data["customer"]["person"]["email"] == person.email
    assert data["order_status"]["status"] == OrderStatusEnum.ORDER_PENDING.status
    assert data["order_status"]["description"] == OrderStatusEnum.ORDER_PENDING.description
    
def test_list_products_by_order_status_and_return_success(client):
    person = PersonFactory()
    customer = CustomerFactory(person=person)
    
    category1 = CategoryFactory(name=ProductCategoryEnum.BURGERS.name, description=ProductCategoryEnum.BURGERS.description)
    category2 = CategoryFactory(name=ProductCategoryEnum.DRINKS.name, description=ProductCategoryEnum.DRINKS.description)

    product1 = ProductFactory(category=category1)
    ProductFactory(category=category2)

    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)


    order = OrderFactory(customer=customer, order_status=order_status)

    response = client.get(
        f"/api/v1/orders/{order.id}/products",
        permissions=[OrderPermissions.CAN_LIST_PRODUCTS_BY_ORDER_STATUS],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        }
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 1
    assert data[0]["category"]["name"] == ProductCategoryEnum.BURGERS.name
    assert data[0]["category"]["description"] == ProductCategoryEnum.BURGERS.description
    assert data[0]["name"] == product1.name
    assert data[0]["description"] == product1.description

def test_get_order_by_id_and_return_success(client):
    person = PersonFactory()
    customer = CustomerFactory(person=person)
    order_status = OrderStatusFactory()
    order = OrderFactory(customer=customer, order_status=order_status)

    response = client.get(
        f"/api/v1/orders/{order.id}",
        permissions=[OrderPermissions.CAN_VIEW_ORDER],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        }
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "id" in data
    assert data["customer"]["person"]["cpf"] == person.cpf
    assert data["customer"]["person"]["name"] == person.name
    assert data["customer"]["person"]["email"] == person.email


def test_add_item_and_return_success(client):
    person = PersonFactory()
    customer = CustomerFactory(person=person)
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(customer=customer, order_status=order_status)

    category = CategoryFactory(name=ProductCategoryEnum.BURGERS.name, description=ProductCategoryEnum.BURGERS.description)
    product = ProductFactory(category=category)

    payload = {
        "order_id": order.id,
        "product_id": product.id,
        "quantity": 1,
        "observation": "No onions"
    }

    response = client.post(
        f"/api/v1/orders/{order.id}/items",
        json=payload,
        permissions=[OrderPermissions.CAN_ADD_ITEM],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        }
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["detail"] == "Item adicionado com sucesso."

def test_try_add_item_product_with_different_category_and_return_error(client):
    person = PersonFactory()
    customer = CustomerFactory(person=person)
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(customer=customer, order_status=order_status)

    category = CategoryFactory(name=ProductCategoryEnum.DRINKS.name, description=ProductCategoryEnum.DRINKS.description)
    product = ProductFactory(category=category)

    payload = {
        "order_id": order.id,
        "product_id": product.id,
        "quantity": 1,
        "observation": "No onions"
    }

    response = client.post(
        f"/api/v1/orders/{order.id}/items",
        json=payload,
        permissions=[OrderPermissions.CAN_ADD_ITEM],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        }
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()
    assert data["detail"]["message"] == "Não é possível adicionar itens da categoria 'drinks' no status atual 'order_waiting_burgers'."


def test_remove_item_and_return_success(client):
    person = PersonFactory()
    customer = CustomerFactory(person=person)
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(customer=customer, order_status=order_status)

    category = CategoryFactory(name=ProductCategoryEnum.BURGERS.name, description=ProductCategoryEnum.BURGERS.description)
    product = ProductFactory(category=category)

    order_item = OrderItemFactory(order=order, product=product)

    response = client.delete(
        f"/api/v1/orders/{order.id}/items/{order_item.id}",
        permissions=[OrderPermissions.CAN_REMOVE_ITEM],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        }
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["detail"] == "Item removido com sucesso."

def test_try_remove_item_from_order_when_item_not_exists_and_return_error(client):
    person = PersonFactory()
    customer = CustomerFactory(person=person)
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(customer=customer, order_status=order_status)

    response = client.delete(
        f"/api/v1/orders/{order.id}/items/1",
        permissions=[OrderPermissions.CAN_REMOVE_ITEM],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        }
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O item com ID '1' não foi encontrado no pedido."

def test_change_item_quantity_and_return_success(client):
    person = PersonFactory()
    customer = CustomerFactory(person=person)
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(customer=customer, order_status=order_status)

    category = CategoryFactory(name=ProductCategoryEnum.BURGERS.name, description=ProductCategoryEnum.BURGERS.description)
    product = ProductFactory(category=category)

    order_item = OrderItemFactory(order=order, product=product)

    payload = {
        "order_id": order.id,
        "new_quantity": 2
    }

    response = client.put(
        f"/api/v1/orders/{order.id}/items/{order_item.id}/quantity",
        params={"order_item_id": order_item.id, "new_quantity": 2},
        json=payload,
        permissions=[OrderPermissions.CAN_CHANGE_ITEM_QUANTITY],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        }
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["detail"] == "Quantidade atualizada com sucesso."

def test_try_change_item_quantity_when_item_not_exists_and_return_error(client):
    person = PersonFactory()
    customer = CustomerFactory(person=person)
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(customer=customer, order_status=order_status)

    response = client.put(
        f"/api/v1/orders/{order.id}/items/1/quantity",
        params={"order_item_id": 1, "new_quantity": 2},
        json={"order_id": order.id, "new_quantity": 2},
        permissions=[OrderPermissions.CAN_CHANGE_ITEM_QUANTITY],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        }
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O item com ID '1' não foi encontrado no pedido."

def test_change_item_observation_and_return_success(client):
    person = PersonFactory()
    customer = CustomerFactory(person=person)
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(customer=customer, order_status=order_status)

    category = CategoryFactory(name=ProductCategoryEnum.BURGERS.name, description=ProductCategoryEnum.BURGERS.description)
    product = ProductFactory(category=category)

    order_item = OrderItemFactory(order=order, product=product)

    payload = {
        "order_id": order.id,
        "new_observation": "No onions"
    }

    response = client.put(
        f"/api/v1/orders/{order.id}/items/{order_item.id}/observation",
        params={"item_id": order_item.id, "new_observation": payload["new_observation"]},
        json=payload,
        permissions=[OrderPermissions.CAN_CHANGE_ITEM_OBSERVATION],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        }
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["detail"] == "Observação atualizada com sucesso."

def test_try_change_item_observation_when_item_not_exists_and_return_error(client):
    person = PersonFactory()
    customer = CustomerFactory(person=person)
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(customer=customer, order_status=order_status)

    response = client.put(
        f"/api/v1/orders/{order.id}/items/1/observation",
        params={"item_id": 1, "new_observation": "No onions"},
        json={"order_id": order.id, "new_observation": "No onions"},
        permissions=[OrderPermissions.CAN_CHANGE_ITEM_OBSERVATION],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        }
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O item com ID '1' não foi encontrado no pedido."

def test_list_order_items_and_return_success(client):
    person = PersonFactory()
    customer = CustomerFactory(person=person)
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(customer=customer, order_status=order_status)

    category = CategoryFactory(name=ProductCategoryEnum.BURGERS.name, description=ProductCategoryEnum.BURGERS.description)
    product = ProductFactory(category=category)

    order_item = OrderItemFactory(order=order, product=product)

    response = client.get(
        f"/api/v1/orders/{order.id}/items",
        permissions=[OrderPermissions.CAN_LIST_ORDER_ITEMS],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        }
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 1
    assert data[0]["product"]["category"]["name"] == ProductCategoryEnum.BURGERS.name
    assert data[0]["product"]["category"]["description"] == ProductCategoryEnum.BURGERS.description
    assert data[0]["product"]["name"] == product.name
    assert data[0]["product"]["description"] == product.description
    assert data[0]["quantity"] == order_item.quantity
    assert data[0]["observation"] == order_item.observation
    assert data[0]["total"] == order_item.total

def test_try_list_order_items_when_order_not_exists_and_return_error(client):
    person = PersonFactory()
    CustomerFactory(person=person)

    response = client.get(
        "/api/v1/orders/999/items",
        permissions=[OrderPermissions.CAN_LIST_ORDER_ITEMS],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        }
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O pedido com ID '999' não foi encontrado."


def test_try_list_order_items_when_order_not_belongs_to_customer_and_return_error(client):
    person = PersonFactory()
    CustomerFactory(person=person)
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status)

    response = client.get(
        f"/api/v1/orders/{order.id}/items",
        permissions=[OrderPermissions.CAN_LIST_ORDER_ITEMS],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        }
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O pedido com ID '1' não foi encontrado."

def test_go_back_order_status_and_return_success(client):
    person = PersonFactory()
    customer = CustomerFactory(person=person)
    
    OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_SIDES.status, description=OrderStatusEnum.ORDER_WAITING_SIDES.description)
    
    order = OrderFactory(customer=customer, order_status=order_status)

    response = client.post(
        f"/api/v1/orders/{order.id}/go-back",
        permissions=[OrderPermissions.CAN_GO_BACK],
        profile_name="employee",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        },
        params={"order_id": order.id}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["detail"] == "Pedido retornado ao passo anterior com sucesso."

def test_try_go_back_order_status_when_order_not_exists_and_return_error(client):
    person = PersonFactory()
    EmployeeFactory(person=person)

    response = client.post(
        "/api/v1/orders/999/go-back",
        permissions=[OrderPermissions.CAN_GO_BACK],
        profile_name="employee",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        },
        params={"order_id": 999}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O pedido com ID '999' não foi encontrado."

def test_try_go_back_order_status_when_order_status_is_waiting_burgers_and_return_error(client):
    person = PersonFactory()
    EmployeeFactory(person=person)

    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status)

    response = client.post(
        f"/api/v1/orders/{order.id}/go-back",
        permissions=[OrderPermissions.CAN_GO_BACK],
        profile_name="employee",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        },
        params={"order_id": order.id}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()
    assert data["detail"]["message"] == "O status atual 'order_waiting_burgers' não permite voltar."

def test_try_go_back_order_status_when_order_status_is_order_placed_and_return_error(client):
    person = PersonFactory()
    EmployeeFactory(person=person)
    
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_PLACED.status, description=OrderStatusEnum.ORDER_PLACED.description)
    order = OrderFactory(order_status=order_status)

    response = client.post(
        f"/api/v1/orders/{order.id}/go-back",
        permissions=[OrderPermissions.CAN_GO_BACK],
        profile_name="employee",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        },
        params={"order_id": order.id}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()
    assert data["detail"]["message"] == "O status atual 'order_placed' não permite voltar."

def test_next_step_order_status_and_return_success(client):
    person = PersonFactory()
    EmployeeFactory(person=person)
    
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_SIDES.status, description=OrderStatusEnum.ORDER_WAITING_SIDES.description)
    
    order = OrderFactory(order_status=order_status)

    response = client.post(
        f"/api/v1/orders/{order.id}/next-step",
        permissions=[OrderPermissions.CAN_NEXT_STEP],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        },
        params={"order_id": order.id}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["detail"] == "Pedido avançado para o próximo passo: order_waiting_sides"

def test_try_next_step_order_status_when_order_not_exists_and_return_error(client):
    person = PersonFactory()
    EmployeeFactory(person=person)

    response = client.post(
        "/api/v1/orders/999/next-step",
        permissions=[OrderPermissions.CAN_NEXT_STEP],
        profile_name="employee",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        },
        params={"order_id": 999}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O pedido com ID '999' não foi encontrado."

def test_clear_order_and_return_success(client):
    person = PersonFactory()
    EmployeeFactory(person=person)
    
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status)

    response = client.delete(
        f"/api/v1/orders/{order.id}/clear",
        permissions=[OrderPermissions.CAN_CLEAR_ORDER],
        profile_name="employee",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        },
        params={"order_id": order.id}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["detail"] == "Pedido limpo com sucesso."
    
def test_try_clear_order_when_order_not_exists_and_return_error(client):
    person = PersonFactory()
    EmployeeFactory(person=person)

    response = client.delete(
        "/api/v1/orders/999/clear",
        permissions=[OrderPermissions.CAN_CLEAR_ORDER],
        profile_name="employee",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        },
        params={"order_id": 999}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O pedido com ID '999' não foi encontrado."

def test_cancel_order_and_return_success(client):
    person = PersonFactory()
    EmployeeFactory(person=person)
    
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status)

    OrderStatusFactory(status=OrderStatusEnum.ORDER_CANCELLED.status, description=OrderStatusEnum.ORDER_CANCELLED.description)

    response = client.post(
        f"/api/v1/orders/{order.id}/cancel",
        permissions=[OrderPermissions.CAN_CANCEL_ORDER],
        profile_name="employee",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        },
        params={"order_id": order.id}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["detail"] == "Pedido cancelado com sucesso."
    
def test_try_cancel_order_when_order_not_exists_and_return_error(client):
    person = PersonFactory()
    EmployeeFactory(person=person)

    response = client.post(
        "/api/v1/orders/999/cancel",
        permissions=[OrderPermissions.CAN_CANCEL_ORDER],
        profile_name="employee",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        },
        params={"order_id": 999}
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    data = response.json()
    assert data["detail"]["message"] == "O pedido com ID '999' não foi encontrado."
