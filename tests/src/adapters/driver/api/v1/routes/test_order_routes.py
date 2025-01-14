from fastapi import status

from tests.factories.customer_factory import CustomerFactory
from tests.factories.employee_factory import EmployeeFactory
from tests.factories.order_factory import OrderFactory
from tests.factories.order_status_factory import OrderStatusFactory
from tests.factories.person_factory import PersonFactory


def test_create_order_success(client):
    person = PersonFactory(cpf="12345678901", name="JOÃO", email="joao@gmail.com")
    customer = CustomerFactory(person=person)
    order_status = OrderStatusFactory()
    employee = EmployeeFactory()

    payload = {
        "id_customer": customer.id,
        "id_order_status": order_status.id,
        "id_employee": employee.id
    }

    response = client.post("/api/v1/order", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "id" in data
    assert data["order_status"]["status"] == order_status.status
    assert data["order_status"]["status_description"] == order_status.status_description
    assert data["customer"]["person"]["cpf"] == person.cpf
    assert data["customer"]["person"]["name"] == person.name
    assert data["customer"]["person"]["email"] == person.email
    

# # def test_create_customer_duplicate_cpf_and_return_error(client, db_session):
# #     person = PersonFactory(cpf="12345678901", name="JOÃO", email="joao@gmail.com", birth_date="1999-01-01")
# #     CustomerFactory(id_person=person.id)
# #     payload = {
# #         "id_person": "2"
# #     }

# #     response = client.post("/api/v1/customer", json=payload)
# #     assert response.status_code == status.HTTP_409_CONFLICT

# #     data = response.json()

# #     assert data["detail"]["message"] == "Customer already exists."

def test_get_order_by_customer_id_and_return_success(client):
    person1 = PersonFactory(
        cpf="12345678901",
        name="JOÃO",
        email="joao@gmail.com",
        birth_date="1999-01-01"
    )
    customer = CustomerFactory(person=person1)
    person2 = PersonFactory(
        cpf="12345678902",
        name="PAULO",
        email="paulo@outlook.com",
        birth_date="1999-01-01"
    )
    employee = EmployeeFactory(person=person2)
    order_status = OrderStatusFactory()
    OrderFactory(customer=customer, employee=employee, order_status=order_status)
    response = client.get(f"/api/v1/orders/{customer.id}/id_customer")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "id" in data[0]
    assert data[0]["customer"]["person"]["cpf"] == "12345678901"
    assert data[0]["customer"]["person"]["name"] == "JOÃO"
    assert data[0]["customer"]["person"]["email"] == "joao@gmail.com"
    assert data[0]["customer"]["person"]["birth_date"] == "1999-01-01"

def test_get_order_by_employee_id_and_return_success(client):
    person1 = PersonFactory(
        cpf="12345678901",
        name="JOÃO",
        email="joao@gmail.com",
        birth_date="1999-01-01"
    )
    customer = CustomerFactory(person=person1)
    person2 = PersonFactory(
        cpf="12345678902",
        name="PAULO",
        email="paulo@outlook.com",
        birth_date="1999-01-01"
    )
    employee = EmployeeFactory(person=person2)
    order_status = OrderStatusFactory()
    OrderFactory(customer=customer, employee=employee, order_status=order_status)
    
    response = client.get(f"/api/v1/orders/{employee.id}/id_employee")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "id" in data[0]
    assert data[0]["employee"]["person"]["cpf"] == "12345678902"
    assert data[0]["employee"]["person"]["name"] == "PAULO"
    assert data[0]["employee"]["person"]["email"] == "paulo@outlook.com"
    assert data[0]["employee"]["person"]["birth_date"] == "1999-01-01"

def test_get_order_by_id_and_return_success(client):
    person1 = PersonFactory(
        cpf="12345678901",
        name="JOÃO",
        email="joao@gmail.com",
        birth_date="1999-01-01"
    )
    customer = CustomerFactory(person=person1)
    person2 = PersonFactory(
        cpf="12345678902",
        name="PAULO",
        email="paulo@outlook.com",
        birth_date="1999-01-01"
    )
    employee = EmployeeFactory(person=person2)
    order_status = OrderStatusFactory()
    order = OrderFactory(customer=customer, employee=employee, order_status=order_status)
    
    response = client.get(f"/api/v1/order/{order.id}/id")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "id" in data
    assert data["customer"]["person"]["cpf"] == "12345678901"
    assert data["customer"]["person"]["name"] == "JOÃO"

def test_get_all_order_return_success(client):
    person1 = PersonFactory(
        cpf="12345678901",
        name="JOÃO",
        email="joao@gmail.com",
        birth_date="1999-01-01"
    )
    customer1 = CustomerFactory(person=person1)
    person2 = PersonFactory(
        cpf="12345678902",
        name="PAULO",
        email="paulo@outlook.com",
        birth_date="1999-01-01"
    )
    employee = EmployeeFactory(person=person2)
    order_status = OrderStatusFactory()
    order1 = OrderFactory(customer=customer1, employee=employee, order_status=order_status)

    person3 = PersonFactory(
        cpf="12345678903",
        name="MATHEUS",
        email="matheus@gmail.com",
        birth_date="1999-03-03"
    )
    customer2 = CustomerFactory(person=person3)
    order_status = OrderStatusFactory()
    order2 = OrderFactory(customer=customer2, employee=employee, order_status=order_status)
    
    response = client.get("/api/v1/orders")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 2
    assert data[0]["id"] == order1.id
    assert data[1]["id"] == order2.id

def test_update_order_and_return_success(client):
    person1 = PersonFactory(
        cpf="12345678901",
        name="JOÃO",
        email="joao@gmail.com",
        birth_date="1999-01-01"
    )
    customer1 = CustomerFactory(person=person1)
    person2 = PersonFactory(
        cpf="12345678902",
        name="PAULO",
        email="paulo@outlook.com",
        birth_date="1999-01-01"
    )
    employee = EmployeeFactory(person=person2)
    order_status = OrderStatusFactory()
    order = OrderFactory(customer=customer1, employee=employee, order_status=order_status)

    person3 = PersonFactory(
        cpf="12345678903",
        name="MATHEUS",
        email="matheus@gmail.com",
        birth_date="1999-03-03"
    )
    customer2 = CustomerFactory(person=person3)
    
    payload = {
        "id": order.id,
        "id_customer": customer2.id,
        "id_order_status": order_status.id,
        "id_employee": employee.id
    }

    response = client.put(f"/api/v1/order/{order.id}", json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["customer"]["person"]["name"] == "MATHEUS"

def test_delete_customer_and_return_success(client):
    order1 = OrderFactory()
    order2 = OrderFactory()

    response = client.delete(f"/api/v1/order/{order1.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/api/v1/orders")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data[0]["id"] == order2.id