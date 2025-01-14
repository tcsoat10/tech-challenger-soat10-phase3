from enum import Enum
from typing import List, Optional

class BasePermissionEnum(str, Enum):

    def __new__(cls, value, description):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def keys(cls):
        return list(cls.__members__.keys())

    @classmethod
    def values(cls):
        return [member.value for member in cls]

    @classmethod
    def descriptions(cls):
        return [member.description for member in cls]
    
    @classmethod
    def values_and_descriptions(cls):
        return [{"name": member.value, "description": member.description} for member in cls]
    
    @classmethod
    def list_only_values(cls, only: Optional[List[str]] = None):
        if only:
            return [
                member.value
                for name, member in cls.__members__.items()
                if any(filter_value.upper() in name for filter_value in only)
            ]
        return cls.values()

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)


class CategoryPermissions(BasePermissionEnum):
    CAN_CREATE_CATEGORY = ("can_create_category", "Permission to create a category")
    CAN_VIEW_CATEGORIES = ("can_view_categories", "Permission to view all categories")
    CAN_UPDATE_CATEGORY = ("can_update_category", "Permission to update a category")
    CAN_DELETE_CATEGORY = ("can_delete_category", "Permission to delete a category")


class ProductPermissions(BasePermissionEnum):
    CAN_CREATE_PRODUCT = ("can_create_product", "Permission to create a product")
    CAN_VIEW_PRODUCTS = ("can_view_products", "Permission to view all products")
    CAN_UPDATE_PRODUCT = ("can_update_product", "Permission to update a product")
    CAN_DELETE_PRODUCT = ("can_delete_product", "Permission to delete a product")


class OrderItemPermissions(BasePermissionEnum):
    CAN_CREATE_ORDER_ITEM = ("can_create_order_item", "Permission to create an order item")
    CAN_VIEW_ORDER_ITEMS = ("can_view_order_items", "Permission to view all order items")
    CAN_UPDATE_ORDER_ITEM = ("can_update_order_item", "Permission to update an order item")
    CAN_DELETE_ORDER_ITEM = ("can_delete_order_item", "Permission to delete an order item")


class OrderPermissions(BasePermissionEnum):
    CAN_CREATE_ORDER = ("can_create_order", "Permission to create an order")
    CAN_VIEW_ORDERS = ("can_view_orders", "Permission to view all orders")
    CAN_UPDATE_ORDER = ("can_update_order", "Permission to update an order")
    CAN_DELETE_ORDER = ("can_delete_order", "Permission to delete an order")


class OrderStatusPermissions(BasePermissionEnum):
    CAN_CREATE_ORDER_STATUS = ("can_create_order_status", "Permission to create an order status")
    CAN_VIEW_ORDER_STATUSES = ("can_view_order_statuses", "Permission to view all order statuses")
    CAN_UPDATE_ORDER_STATUS = ("can_update_order_status", "Permission to update an order status")
    CAN_DELETE_ORDER_STATUS = ("can_delete_order_status", "Permission to delete an order status")


class PermissionPermissions(BasePermissionEnum):
    CAN_CREATE_PERMISSION = ("can_create_permission", "Permission to create a permission")
    CAN_VIEW_PERMISSIONS = ("can_view_permissions", "Permission to view all permissions")
    CAN_UPDATE_PERMISSION = ("can_update_permission", "Permission to update a permission")
    CAN_DELETE_PERMISSION = ("can_delete_permission", "Permission to delete a permission")


class ProfilePermissions(BasePermissionEnum):
    CAN_CREATE_PROFILE = ("can_create_profile", "Permission to create a profile")
    CAN_VIEW_PROFILES = ("can_view_profiles", "Permission to view all profiles")
    CAN_UPDATE_PROFILE = ("can_update_profile", "Permission to update a profile")
    CAN_DELETE_PROFILE = ("can_delete_profile", "Permission to delete a profile")


class ProfilePermissionPermissions(BasePermissionEnum):
    CAN_CREATE_PROFILE_PERMISSION = ("can_create_profile_permission", "Permission to create a profile permission")
    CAN_VIEW_PROFILE_PERMISSIONS = ("can_view_profile_permissions", "Permission to view all profile permissions")
    CAN_UPDATE_PROFILE_PERMISSION = ("can_update_profile_permission", "Permission to update a profile permission")
    CAN_DELETE_PROFILE_PERMISSION = ("can_delete_profile_permission", "Permission to delete a profile permission")


class PaymentMethodPermissions(BasePermissionEnum):
    CAN_CREATE_PAYMENT_METHOD = ("can_create_payment_method", "Permission to create a payment method")
    CAN_VIEW_PAYMENT_METHODS = ("can_view_payment_methods", "Permission to view all payment methods")
    CAN_UPDATE_PAYMENT_METHOD = ("can_update_payment_method", "Permission to update a payment method")
    CAN_DELETE_PAYMENT_METHOD = ("can_delete_payment_method", "Permission to delete a payment method")


class PaymentPermissions(BasePermissionEnum):
    CAN_CREATE_PAYMENT = ("can_create_payment", "Permission to create a payment")
    CAN_VIEW_PAYMENTS = ("can_view_payments", "Permission to view all payments")
    CAN_UPDATE_PAYMENT = ("can_update_payment", "Permission to update a payment")
    CAN_DELETE_PAYMENT = ("can_delete_payment", "Permission to delete a payment")


class PaymentStatusPermissions(BasePermissionEnum):
    CAN_CREATE_PAYMENT_STATUS = ("can_create_payment_status", "Permission to create a payment status")
    CAN_VIEW_PAYMENT_STATUSES = ("can_view_payment_statuses", "Permission to view all payment statuses")
    CAN_UPDATE_PAYMENT_STATUS = ("can_update_payment_status", "Permission to update a payment status")
    CAN_DELETE_PAYMENT_STATUS = ("can_delete_payment_status", "Permission to delete a payment status")


class RolePermissions(BasePermissionEnum):
    CAN_CREATE_ROLE = ("can_create_role", "Permission to create a role")
    CAN_VIEW_ROLES = ("can_view_roles", "Permission to view all roles")
    CAN_UPDATE_ROLE = ("can_update_role", "Permission to update a role")
    CAN_DELETE_ROLE = ("can_delete_role", "Permission to delete a role")


class UserPermissions(BasePermissionEnum):
    CAN_CREATE_USER = ("can_create_user", "Permission to create a user")
    CAN_VIEW_USERS = ("can_view_users", "Permission to view all users")
    CAN_UPDATE_USER = ("can_update_user", "Permission to update a user")
    CAN_DELETE_USER = ("can_delete_user", "Permission to delete a user")


class UserProfilePermissions(BasePermissionEnum):
    CAN_CREATE_USER_PROFILE = ("can_create_user_profile", "Permission to create a user profile")
    CAN_VIEW_USER_PROFILES = ("can_view_user_profiles", "Permission to view all user profiles")
    CAN_UPDATE_USER_PROFILE = ("can_update_user_profile", "Permission to update a user profile")
    CAN_DELETE_USER_PROFILE = ("can_delete_user_profile", "Permission to delete a user profile")


class EmployeePermissions(BasePermissionEnum):
    CAN_CREATE_EMPLOYEE = ("can_create_employee", "Permission to create an employee")
    CAN_VIEW_EMPLOYEES = ("can_view_employees", "Permission to view all employees")
    CAN_UPDATE_EMPLOYEE = ("can_update_employee", "Permission to update an employee")
    CAN_DELETE_EMPLOYEE = ("can_delete_employee", "Permission to delete an employee")
