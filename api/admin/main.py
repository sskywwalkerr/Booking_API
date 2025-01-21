from sqladmin import ModelView
from sqlalchemy import Select

from api.models import User, Booking, Hotel, Room


class UserAdmin(ModelView, model=User):
    column_list = [User.uid, User.email] + [User.bookings]
    can_delete = False
    save_as = True
    name = 'Пользователь'
    name_plural = 'Пользователь'
    icon = 'fa-solid fa-user'
    column_searchable_list = [User.uid, User.email]
    column_filters = {User.bookings: 'Бронь пользователя'}

    def search_query(self, stmt: Select, term: str) -> Select:
        """Поиск по email пользователя"""

        return stmt.filter(User.email.icontains(term))


class HotelAdmin(ModelView, model=Hotel):
    column_list = [col.name for col in Hotel.__table__.columns] + [Hotel.room]
    save_as = True
    name = 'Отель'
    name_plural = 'Отели'
    icon = 'fa-solid fa-hotel'
    column_searchable_list = [Hotel.uid, Hotel.room]
    # column_sortable_list = [Hotel.stars]
    column_labels = {
        Hotel.name: 'Название',
        Hotel.room: 'номер',
        Hotel.description: 'Описание',
        Hotel.location: 'Адрес',
    }

    def search_query(self, stmt: Select, term: str) -> Select:
        """Поиск по названию отеля"""

        return stmt.filter(User.email.icontains(term))


class BookingAdmin(ModelView, model=Booking):
    column_list = [col.name for col in Booking.__table__.columns] + [Booking.room, Booking.user]
    save_as = True
    name = 'Бронь'
    name_plural = 'Брони'
    icon = 'fa-solid fa-tag'
    column_searchable_list = [Booking.uid, Booking.date_from, Booking.date_to]
    column_sortable_list = [Booking.date_from, Booking.date_to, Booking.user_uid, Booking.room_uid]
    column_labels = {
        Booking.user: 'Забронировал',
        Booking.room: 'Номер',
        Booking.price: 'Цена',
        Booking.date_to: 'Дата выселения',
        Booking.date_from: 'Дата заселения',
        Booking.total_cost: 'Общая стоимость',
        Booking.total_days: 'Общее кол-во дней',
        Booking.uid: 'ID брони',
        Booking.room_uid: 'ID комнаты',
        Booking.user_uid: 'ID пользователя'
    }

    def search_query(self, stmt: Select, term: str) -> Select:
        """Поиск по названию номера в броне"""

        return stmt.filter(Booking.room.icontains(term))


class RoomAdmin(ModelView, model=Room):
    column_list = [Room.uid, Room.name, Room.description, Room.price, Room.hotel_uid]
    save_as = True
    name = 'Номер'
    name_plural = 'Номера'
    icon = 'fa-solid fa-bed'
    column_searchable_list = [Room.uid, Room.hotel]
    column_sortable_list = [Room.hotel_uid, Room.price]
    column_labels = {
        Room.name: 'Название',
        Room.price: 'Цена',
        Room.booking: 'Брони',
        Room.description: 'Описание',
        Room.hotel: 'Отель',
        Room.quantity: 'Количество',
        Room.hotel_uid: 'ID отеля'
    }

    def search_query(self, stmt: Select, term: str) -> Select:
        """Поиск по названию номера"""

        return stmt.filter(Room.name.icontains(term))
