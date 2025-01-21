from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from api.auth.dependencies import get_current_users
from api.auth.service import authenticate_user
from api.auth.utils import create_access_token
from api.config import Config


class AdminAuth(AuthenticationBackend):
    """Аутентификация в админке"""

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await authenticate_user(email, password)
        if user:
            access_token = create_access_token({"sub": str(user.uid)})
            request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        """Выход из системы"""

        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | bool:
        """Проверка токена  и предостваление доступа к админке"""

        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        user = await get_current_users(token)
        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        return True


authentication_backend = AdminAuth(secret_key=Config.JWT_SECRET)
