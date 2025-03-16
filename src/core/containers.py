from dependency_injector import containers, providers
from sqlalchemy.orm import Session
from src.adapters.driver.api.v1.controllers.category_controller import CategoryController
from src.adapters.driven.repositories.category_repository import CategoryRepository
from src.adapters.driver.api.v1.controllers.product_controller import ProductController
from src.adapters.driven.repositories.product_repository import ProductRepository
from src.adapters.driven.repositories.permission_repository import PermissionRepository
from src.adapters.driver.api.v1.controllers.permission_controller import PermissionController
from src.adapters.driven.repositories.profile_repository import ProfileRepository
from src.adapters.driver.api.v1.controllers.profile_controller import ProfileController
from src.adapters.driven.repositories.profile_permission_repository import ProfilePermissionRepository
from src.adapters.driver.api.v1.controllers.profile_permission_controller import ProfilePermissionController
from src.adapters.driven.repositories.user_repository import UserRepository
from src.adapters.driver.api.v1.controllers.user_controller import UserController


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[
        "src.adapters.driver.api.v1.controllers.category_controller",
        "src.adapters.driver.api.v1.routes.category_routes",
        "src.adapters.driver.api.v1.controllers.product_controller",
        "src.adapters.driver.api.v1.routes.product_routes",
        "src.adapters.driver.api.v1.controllers.permission_controller",
        "src.adapters.driver.api.v1.routes.permission_routes",
        "src.adapters.driver.api.v1.controllers.profile_controller",
        "src.adapters.driver.api.v1.routes.profile_routes",
        "src.adapters.driver.api.v1.controllers.profile_permission_controller",
        "src.adapters.driver.api.v1.routes.profile_permission_routes",
        "src.adapters.driver.api.v1.controllers.user_controller",
        "src.adapters.driver.api.v1.routes.user_routes",
    ])

    db_session = providers.Dependency(instance_of=Session)

    category_gateway = providers.Factory(
        CategoryRepository,
        db_session=db_session
    )

    category_controller = providers.Factory(
        CategoryController,
        category_gateway=category_gateway
    )

    product_gateway = providers.Factory(ProductRepository, db_session=db_session)
    product_controller = providers.Factory(
        ProductController, product_gateway=product_gateway, category_gateway=category_gateway
    )

    permission_gateway = providers.Factory(PermissionRepository, db_session=db_session)
    permission_controller = providers.Factory(PermissionController, permission_gateway=permission_gateway)

    profile_gateway = providers.Factory(ProfileRepository, db_session=db_session)
    profile_controller = providers.Factory(ProfileController, profile_gateway=profile_gateway)

    profile_permission_gateway = providers.Factory(ProfilePermissionRepository, db_session=db_session)
    profile_permission_controller = providers.Factory(
        ProfilePermissionController,
        profile_permission_gateway=profile_permission_gateway,
        permission_gateway=permission_gateway,
        profile_gateway=profile_gateway
    )

    user_gateway = providers.Factory(UserRepository, db_session=db_session)
    user_controller = providers.Factory(UserController, user_gateway=user_gateway)
