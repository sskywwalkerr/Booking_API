from sqladmin import Admin

from api.db.data import async_engine, async_session_maker

from .auth import authentication_backend

#from .views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from .main import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin


def create_admin(app) -> Admin:  # noqa: ANN001
    admin = Admin(
        app,
        engine=async_engine,
        session_maker=async_session_maker,
        authentication_backend=authentication_backend,
    )
    _add_admin_views(admin)
    return admin


def _add_admin_views(admin: Admin) -> None:
    admin.add_view(UserAdmin)
    admin.add_view(HotelAdmin)
    admin.add_view(RoomAdmin)
    admin.add_view(BookingAdmin)
