from collections.abc import Iterable

from aiogram import types


from aiogram.utils.callback_data import CallbackData


class StartDialog(types.ReplyKeyboardMarkup):
    def __init__(self):

        buy_button = types.KeyboardButton("Купить")

        sell_button = types.KeyboardButton("Продать")

        super().__init__(
            [[buy_button], [sell_button]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )


class MainMenuDialog(types.ReplyKeyboardMarkup):
    def __init__(self):

        search_button = types.KeyboardButton("Найти объект")

        settings_button = types.KeyboardButton("Перезвоните мне")

        contact_button = types.KeyboardButton("Связь с оператором")

        terms_button = types.KeyboardButton("Условия сотрудничества")

        back_button = types.KeyboardButton("Вернуться в меню")

        super().__init__(
            keyboard=[
                [back_button, search_button],
                [settings_button, contact_button],
                [terms_button],
            ],
            resize_keyboard=True,
        )


class BuyingTermsDialog(types.InlineKeyboardMarkup):
    def __init__(self, callback_data):

        about_button = types.InlineKeyboardButton(
            "О компании", callback_data=callback_data.new(action="about")
        )

        payment_system_button = types.InlineKeyboardButton(
            "Пакетная система оплаты",
            callback_data=callback_data.new(action="payment_system"),
        )

        agreement_button = types.InlineKeyboardButton(
            "Договор сотрудничества (договор купли)",
            callback_data=callback_data.new(action="buyer_agreement"),
        )

        super().__init__(
            inline_keyboard=[
                [about_button],
                [payment_system_button],
                [agreement_button],
            ]
        )


class SellingTermsDialog(types.InlineKeyboardMarkup):
    def __init__(self, callback_data):

        about_button = types.InlineKeyboardButton(
            "О компании", callback_data=callback_data.new(action="about")
        )

        payment_system_button = types.InlineKeyboardButton(
            "Пакетная система оплаты",
            callback_data=callback_data.new(action="payment_system"),
        )

        agreement_button = types.InlineKeyboardButton(
            "Договор сотрудничества (договор продажи)",
            callback_data=callback_data.new(action="seller_agreement"),
        )

        super().__init__(
            inline_keyboard=[
                [about_button],
                [payment_system_button],
                [agreement_button],
            ]
        )


class PreSearchMenuDialog(types.ReplyKeyboardMarkup):
    def __init__(self):

        set_parameters_button = types.KeyboardButton("Задать параметры")

        favorites_button = types.KeyboardButton("По сохранённым параметрам")

        main_menu_button = types.KeyboardButton("Главное меню")

        super().__init__(
            keyboard=[
                [set_parameters_button, favorites_button],
                [main_menu_button],
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )


class InlineSearchMenuDialog(types.InlineKeyboardMarkup):
    def __init__(self, callback_data: CallbackData):

        keyboard = [
            [
                types.InlineKeyboardButton(
                    "Вернуться", callback_data=callback_data.new(action="back")
                ),
                types.InlineKeyboardButton(
                    "Подобрать", callback_data=callback_data.new(action="pick")
                ),
            ],
            [
                types.InlineKeyboardButton(
                    "Сохранить настройки",
                    callback_data=callback_data.new(action="save_settings"),
                )
            ],
        ]

        super().__init__(
            inline_keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
        )


class PostSearchMenuDialog(types.ReplyKeyboardMarkup):
    def __init__(self):

        back_button = types.KeyboardButton("Вернуться")

        more_button = types.KeyboardButton("Ещё объекты")

        # updates_button = types.KeyboardButton("Получать обновления")

        keyboard = [[more_button], [back_button]]

        super().__init__(
            keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True
        )


class DistrictSelectionDialog(types.InlineKeyboardMarkup):
    def __init__(self, districts: dict[str, str], cb_data: CallbackData):

        district_buttons: list[list[types.InlineKeyboardButton]] = []

        for district in districts:

            button = types.InlineKeyboardButton(
                district, callback_data=cb_data.new(action=districts[district])
            )

            district_buttons.append([button])

        super().__init__(inline_keyboard=district_buttons)


class EstateTypeSelectionDialog(types.InlineKeyboardMarkup):
    def __init__(self, district: str, cb_data: CallbackData):

        flat_button = types.InlineKeyboardButton(
            "Квартира", callback_data=cb_data.new(action="flat")
        )

        room_button = types.InlineKeyboardButton(
            "Комната", callback_data=cb_data.new(action="room")
        )

        house_button = types.InlineKeyboardButton(
            "Дом", callback_data=cb_data.new(action="house")
        )

        country_house_button = types.InlineKeyboardButton(
            "Дача", callback_data=cb_data.new(action="country_house")
        )

        claim_button = types.InlineKeyboardButton(
            "Участок", callback_data=cb_data.new(action="claim")
        )

        commerce_button = types.InlineKeyboardButton(
            "Коммерция", callback_data=cb_data.new(action="commerce")
        )

        super().__init__(
            inline_keyboard=[
                [flat_button, room_button],
                [house_button, country_house_button],
                [claim_button],
                [commerce_button],
            ]
        )


class SellMenuDialog(types.ReplyKeyboardMarkup):
    def __init__(self):

        back_button = types.KeyboardButton("Вернуться")

        next_button = types.KeyboardButton("Далее")

        terms_button = types.KeyboardButton("Условия сотрудничества")

        super().__init__(
            keyboard=[
                [back_button, next_button],
                [
                    terms_button,
                ],
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )


class PhoneRetreivalDialog(types.ReplyKeyboardMarkup):
    def __init__(self):

        phone_request_button = types.KeyboardButton(
            "Отправить", request_contact=True
        )

        back_button = types.KeyboardButton("Вернуться")

        super().__init__(
            keyboard=[[phone_request_button], [back_button]],
            resize_keyboard=True,
        )


class InlineFavoritesDialog(types.InlineKeyboardMarkup):
    def __init__(
        self,
        cb_data: CallbackData,
        names: Iterable[str],
        save_mode: bool = False,
    ):

        keyboard = []

        for i in range(0, 3):

            keyboard.append(
                [
                    types.InlineKeyboardButton(
                        names[i],  # type: ignore
                        callback_data=cb_data.new(
                            action="property_group", index=i
                        ),
                    )
                ]
            )

        if not save_mode:

            keyboard.append(
                [
                    types.InlineKeyboardButton(
                        "Редактировать",
                        callback_data=cb_data.new(action="edit", index=4),
                    )
                ]
            )

        super().__init__(inline_keyboard=keyboard)


class InlinePropertiesDialog(types.InlineKeyboardMarkup):
    def __init__(
        self, cb_data: CallbackData, estate_type: str, selling: bool = False
    ):

        self.estate_type = estate_type

        self.cb_data = cb_data

        room_count_buttons = self.configure_room_buttons() or []

        area_buttons = self.configure_area_buttons() or []

        price_buttons = self.configure_price_buttons() or []

        commerce_buttons = []

        if estate_type == "commerce":

            commerce_buttons = [
                [
                    types.InlineKeyboardButton(
                        "Офис",
                        callback_data=self.cb_data.new(
                            property="commerce",
                            filter="office",
                            row_index="0",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "Гараж",
                        callback_data=self.cb_data.new(
                            property="commerce",
                            filter="garage",
                            row_index="0",
                            column_index="0",
                        ),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        "Магазин",
                        callback_data=self.cb_data.new(
                            property="commerce",
                            filter="store",
                            row_index="0",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "Свобод",
                        callback_data=self.cb_data.new(
                            property="commerce",
                            filter="free",
                            row_index="0",
                            column_index="0",
                        ),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        "Производство",
                        callback_data=self.cb_data.new(
                            property="commerce",
                            filter="industry",
                            row_index="0",
                            column_index="0",
                        ),
                    ),
                ],
            ]

        keyboard = []

        for row in room_count_buttons:

            keyboard.append(row)

        for row in area_buttons:

            keyboard.append(row)

        for row in price_buttons:

            keyboard.append(row)

        for row in commerce_buttons:

            keyboard.append(row)

        if estate_type == "commerce":

            super().__init__(inline_keyboard=keyboard)
            return

        if selling:

            keyboard.append(
                [
                    types.InlineKeyboardButton(
                        "Продать быстро", callback_data="sell_fast"
                    )
                ]
            )

            keyboard.append(
                [
                    types.InlineKeyboardButton(
                        "Продать дорого", callback_data="sell_expensive"
                    )
                ]
            )

        else:

            keyboard.append(
                [types.InlineKeyboardButton("Принять", callback_data="accept")]
            )

        super().__init__(inline_keyboard=keyboard)

    def configure_room_buttons(self):

        room_buttons_condition = (
            (self.estate_type == "flat")
            or (self.estate_type == "house")
            or (self.estate_type == "country_house")
        )

        return [
            [
                types.InlineKeyboardButton(
                    "Кол-во комнат", callback_data="blank"
                )
            ],
            [
                types.InlineKeyboardButton(
                    "1",
                    callback_data=self.cb_data.new(
                        property="room_count",
                        filter="= 1",
                        row_index="1",
                        column_index="0",
                    ),
                ),
                types.InlineKeyboardButton(
                    "2",
                    callback_data=self.cb_data.new(
                        property="room_count",
                        filter="= 2",
                        row_index="1",
                        column_index="1",
                    ),
                ),
                types.InlineKeyboardButton(
                    "3",
                    callback_data=self.cb_data.new(
                        property="room_count",
                        filter="= 3",
                        row_index="1",
                        column_index="2",
                    ),
                ),
                types.InlineKeyboardButton(
                    "4+",
                    callback_data=self.cb_data.new(
                        property="room_count",
                        filter=">= 4",
                        row_index="1",
                        column_index="3",
                    ),
                ),
            ],
        ] * room_buttons_condition

    def configure_area_buttons(self):

        if (self.estate_type == "flat") or (self.estate_type == "house"):

            return [
                [types.InlineKeyboardButton("Площадь", callback_data="blank")],
                [
                    types.InlineKeyboardButton(
                        "до 30",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter="<= 30",
                            row_index="3",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "31-40",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter="BETWEEN 31 AND 40",
                            row_index="3",
                            column_index="1",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "41-50",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter="BETWEEN 41 AND 50",
                            row_index="3",
                            column_index="2",
                        ),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        "51-60",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter="BETWEEN 51 AND 60",
                            row_index="4",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "61-70",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter="BETWEEN 61 AND 70",
                            row_index="4",
                            column_index="1",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "71+",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter=">= 71",
                            row_index="4",
                            column_index="2",
                        ),
                    ),
                ],
            ]

        elif self.estate_type == "room":

            return [
                [types.InlineKeyboardButton("Площадь", callback_data="blank")],
                [
                    types.InlineKeyboardButton(
                        "до 5",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter="<= 5",
                            row_index="1",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "5-10",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter="BETWEEN 5 AND 10",
                            row_index="1",
                            column_index="1",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "10+",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter=">= 10",
                            row_index="1",
                            column_index="2",
                        ),
                    ),
                ],
            ]

        elif self.estate_type == "country_house":

            return [
                [types.InlineKeyboardButton("Площадь", callback_data="blank")],
                [
                    types.InlineKeyboardButton(
                        "до 30",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter="<= 30",
                            row_index="3",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "31-40",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter="BETWEEN 31 AND 40",
                            row_index="3",
                            column_index="1",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "41-50",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter="BETWEEN 41 AND 50",
                            row_index="3",
                            column_index="2",
                        ),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        "51-60",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter="BETWEEN 51 AND 60",
                            row_index="4",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "61-70",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter="BETWEEN 61 AND 70",
                            row_index="4",
                            column_index="1",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "71+",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter=">= 71",
                            row_index="4",
                            column_index="2",
                        ),
                    ),
                ],
            ]

        elif self.estate_type == "claim":

            return [
                [types.InlineKeyboardButton("Площадь", callback_data="blank")],
                [
                    types.InlineKeyboardButton(
                        "до 10",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter="<= 10",
                            row_index="1",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "11-20",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter="BETWEEN 11 AND 20",
                            row_index="1",
                            column_index="1",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "21+",
                        callback_data=self.cb_data.new(
                            property="area",
                            filter=">= 21",
                            row_index="1",
                            column_index="2",
                        ),
                    ),
                ],
            ]

    def configure_price_buttons(self):

        if self.estate_type == "flat":

            return [
                [types.InlineKeyboardButton("Цена", callback_data="blank")],
                [
                    types.InlineKeyboardButton(
                        "до 25",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="<= 25000",
                            row_index="6",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "26-40",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 26000 AND 40000",
                            row_index="6",
                            column_index="1",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "41-60",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 41000 AND 60000",
                            row_index="6",
                            column_index="2",
                        ),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        "61-80",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 61000 AND 80000",
                            row_index="7",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "81-100",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 81000 AND 100000",
                            row_index="7",
                            column_index="1",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "100+",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter=">= 100000",
                            row_index="7",
                            column_index="2",
                        ),
                    ),
                ],
            ]

        elif self.estate_type == "room":

            return [
                [types.InlineKeyboardButton("Цена", callback_data="blank")],
                [
                    types.InlineKeyboardButton(
                        "до 5",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="<= 5000",
                            row_index="3",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "5-10",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 5000 AND 10000",
                            row_index="3",
                            column_index="1",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "10+",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter=">= 10000",
                            row_index="3",
                            column_index="2",
                        ),
                    ),
                ],
            ]

        elif self.estate_type == "house":

            return [
                [types.InlineKeyboardButton("Цена", callback_data="blank")],
                [
                    types.InlineKeyboardButton(
                        "до 25",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="<= 25000",
                            row_index="6",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "26-40",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 26000 AND 40000",
                            row_index="6",
                            column_index="1",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "41-60",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 41000 AND 60000",
                            row_index="6",
                            column_index="2",
                        ),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        "61-80",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 61000 AND 80000",
                            row_index="7",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "81-100",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 81000 AND 100000",
                            row_index="7",
                            column_index="1",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "100+",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter=">= 100000",
                            row_index="7",
                            column_index="2",
                        ),
                    ),
                ],
            ]

        elif self.estate_type == "country_house":

            return [
                [types.InlineKeyboardButton("Цена", callback_data="blank")],
                [
                    types.InlineKeyboardButton(
                        "до 25",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="<= 25000",
                            row_index="6",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "26-40",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 26000 AND 40000",
                            row_index="6",
                            column_index="1",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "41-60",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 41000 AND 60000",
                            row_index="6",
                            column_index="2",
                        ),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        "61-80",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 61000 AND 80000",
                            row_index="7",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "81-100",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 81000 AND 100000",
                            row_index="7",
                            column_index="1",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "100+",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter=">= 100000",
                            row_index="7",
                            column_index="2",
                        ),
                    ),
                ],
            ]

        elif self.estate_type == "claim":

            return [
                [types.InlineKeyboardButton("Цена", callback_data="blank")],
                [
                    types.InlineKeyboardButton(
                        "до 5",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="<= 5000",
                            row_index="3",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "6-10",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 6000 AND 10000",
                            row_index="3",
                            column_index="1",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "11-20",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 11000 AND 20000",
                            row_index="3",
                            column_index="2",
                        ),
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        "21-30",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 21000 AND 30000",
                            row_index="4",
                            column_index="0",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "31-40",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter="BETWEEN 31000 AND 40000",
                            row_index="4",
                            column_index="1",
                        ),
                    ),
                    types.InlineKeyboardButton(
                        "41+",
                        callback_data=self.cb_data.new(
                            property="price",
                            filter=">= 41000",
                            row_index="4",
                            column_index="2",
                        ),
                    ),
                ],
            ]


class ShowOnWebDialog(types.InlineKeyboardMarkup):
    def __init__(self, url: str):

        url_button = types.InlineKeyboardButton("Показать на сайте", url=url)

        keyboard = [[url_button]]

        super().__init__(inline_keyboard=keyboard)
