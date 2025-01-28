from sqladmin import ModelView

from api.models import Booking, Hotel, User, Room


class UsersAdmin(ModelView, model=User):
    column_list = "__all__"
    # column_list = [User.uid, User.email, User.bookings]
    column_details_exclude_list = [User.password_hash]
    can_delete = False
    can_edit = False
    name_plural = "Users"
    name = "User"
    icon = "fa-solid fa-user"


class HotelsAdmin(ModelView, model=Hotel):
    column_list = [c.name for c in Hotel.__table__.c] + [Hotel.room]
    name_plural = "Hotels"
    name = "Hotel"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Room):
    column_list = [c.name for c in Room.__table__.c] + [Room.hotel, Room.booking]
    name_plural = "Rooms"
    name = "Room"
    icon = "fa-solid fa-bed"


class BookingsAdmin(ModelView, model=Booking):
    column_list = [c.name for c in Booking.__table__.c] + [
        Booking.user,
        Booking.room,
    ]
    name_plural = "Bookings"
    name = "Booking"
    icon = "fa-solid fa-book"
