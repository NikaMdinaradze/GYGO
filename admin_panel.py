from sqladmin.authentication import AuthenticationBackend
from fastapi.requests import Request
from sqladmin import ModelView
from models import Places
from JWT import USERNAME, PASSWORD


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
        form = await request.form()
        username, password = form["username"], form["password"]

        if username == USERNAME and password == PASSWORD:
            request.session.update({"token": "superduperadmin"})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if token and token == "superduperadmin":
            return True

        return False


authentication_backend = AdminAuth(secret_key="...")

