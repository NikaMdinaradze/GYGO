from sqladmin.authentication import AuthenticationBackend
from fastapi.requests import Request
from sqladmin import ModelView, BaseView
from models import Places


class UserAdmin(ModelView, model=Places):
    column_list = [Places.id, Places.name,Places.logo, Places.category,
                   Places.district, Places.main_price, Places.main_visit]
    name = "Place"
    name_plural = "Places"
    icon = "fa-solid fa-home"
    column_searchable_list = [Places.name]

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        request.session.update({"token": "..."})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key="...")

