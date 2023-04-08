from aiogram.contrib.middlewares.logging import LoggingMiddleware


from aiogram.contrib.fsm_storage.memory import MemoryStorage


from aiogram.utils.exceptions import MessageNotModified


from aiogram.utils.callback_data import CallbackData


from aiogram.dispatcher.filters import Text


from aiogram.dispatcher import Dispatcher, FSMContext


from aiogram import Bot, types, executor

import bs4
import requests

from states import MainStates

from typing import Union, Any
import logging
import random

from database import Database
from config import OPERATOR_PHONE_NUMBERS, TOKEN, OPERATOR_TELEGRAM_ID
import dialogs
import conversion


logging.basicConfig()

database = Database()

district_record: Union[tuple[dict[str, Any], ...], None]

districts = {"Полтава": "poltava", "Полт. район": "poltava_district"}


bot = Bot(token=TOKEN)


dp = Dispatcher(bot, storage=MemoryStorage())


dp.middleware.setup(LoggingMiddleware())

district_selection_dialog_cb_data = CallbackData("district", "action")


estate_selection_dialog_cb_data = CallbackData("estate", "action")


inline_sell_dialog_cb_data = CallbackData("sell_choice", "action")


inline_properties_dialog_cb_data = CallbackData(
    "property", "property", "filter", "row_index", "column_index"
)

inline_terms_dialog_cb_data = CallbackData("menu_item", "action")

inline_favorites_dialog_cb_data = CallbackData("menu_item", "action", "index")

inline_search_menu_dialog_cb_data = CallbackData("menu_item", "action")

# @dp.message_handler()
# async def get_message(message: types.Message):


@dp.message_handler(commands=["start"], state="*")
async def start_command(message: types.Message, state: FSMContext):
    state_data = await state.get_data()

    if "property_group_0" not in state_data.keys():
        await state.update_data(
            property_group_0={
                "name": "Вариант 1 (Пусто)",
                "district": str(),
                "estate_type": str(),
                "commerce_type": str(),
                "room_count": [],
                "area": [],
                "price": [],
            },
            property_group_1={
                "name": "Вариант 2 (Пусто)",
                "district": str(),
                "estate_type": str(),
                "commerce_type": str(),
                "room_count": [],
                "area": [],
                "price": [],
            },
            property_group_2={
                "name": "Вариант 3 (Пусто)",
                "district": str(),
                "estate_type": str(),
                "commerce_type": str(),
                "room_count": [],
                "area": [],
                "price": [],
            },
        )

    await message.reply(
        "Приветствуем вас в официальном боте Дом24.",
        reply_markup=dialogs.StartDialog(),
    )


# region StartDialog handlers


@dp.message_handler(lambda message: message.text == "Купить", state="*")
async def buy_button(message: types.Message, state: FSMContext):
    await bot.send_message(
        message.from_user.id,
        "Я помогу вам найти актуальные квартиры, дома, помещения и участки.",
        reply_markup=dialogs.MainMenuDialog(),
    )

    state_data = await state.get_data()

    await MainStates.buying.set()

    await state.update_data(state_data)


@dp.message_handler(lambda message: message.text == "Продать", state="*")
async def sell_button(message: types.Message, state: FSMContext):
    current_property_group = {
        "district": str(),
        "estate_type": str(),
        "commerce_type": str(),
        "room_count": [],
        "area": [],
        "price": [],
        "sale_type": "",
    }

    await state.update_data(current_property_group=current_property_group)

    await bot.send_message(
        message.from_user.id,
        "Выбор района:",
        reply_markup=dialogs.DistrictSelectionDialog(
            districts, district_selection_dialog_cb_data
        ),
    )

    state_data = await state.get_data()

    await MainStates.selling.set()

    await state.update_data(state_data)


# endregion


# region MainMenuDialog handlers


@dp.message_handler(
    lambda message: message.text == "Найти объект", state=MainStates.buying
)
async def search_button(message: types.Message, state: FSMContext):
    await bot.send_message(
        message.from_user.id,
        "Задайте параметры или воспользуйтесь сохранёнными 🔎",
        reply_markup=dialogs.PreSearchMenuDialog(),
    )

    current_property_group = {
        "district": str(),
        "estate_type": str(),
        "commerce_type": str(),
        "room_count": [],
        "area": [],
        "price": [],
    }

    await state.update_data(current_property_group=current_property_group)


@dp.message_handler(
    lambda message: message.text == "Перезвоните мне", state=MainStates.buying
)
async def settings_button(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        "Вы хотите отправить свой номер телефона?",
        reply_markup=dialogs.PhoneRetreivalDialog(),
    )


@dp.message_handler(
    lambda message: message.text == "Связь с оператором",
    state=MainStates.buying,
)
async def contact_operator_button(message: types.Message):
    index = random.randint(0, len(OPERATOR_PHONE_NUMBERS) - 1)

    contact = OPERATOR_PHONE_NUMBERS[index]

    await bot.send_contact(
        message.from_user.id, contact["phone"], "Оператор", contact["name"]
    )


@dp.message_handler(
    lambda message: message.text == "Условия сотрудничества",
    state=MainStates.buying,
)
async def terms_buying_button(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        (
            "Здесь найдете все необходимые документы о компании, договора"
            " и условия сотрудничества с нами"
        ),
        reply_markup=dialogs.BuyingTermsDialog(inline_terms_dialog_cb_data),
    )


@dp.message_handler(
    lambda message: message.text == "Условия сотрудничества",
    state=MainStates.selling,
)
async def terms_selling_button(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        (
            "Здесь найдете все необходимые документы о компании, договора"
            " и условия сотрудничества с нами"
        ),
        reply_markup=dialogs.SellingTermsDialog(inline_terms_dialog_cb_data),
    )


@dp.message_handler(
    lambda message: message.text == "Вернуться в меню",
    state=MainStates.buying,
)
async def back_to_start_button(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        "Воспользуйтесь клавиатурой 👇",
        reply_markup=dialogs.StartDialog(),
    )


# endregion


# region InlineTermsDialog handlers


@dp.callback_query_handler(
    inline_terms_dialog_cb_data.filter(action="about"), state="*"
)
async def about_button(query: types.CallbackQuery):
    await query.answer()

    await bot.send_message(
        query.from_user.id,
        (
            "О компании:\n"
            "Dom24.com.ua – недвижимость в Полтаве – "
            "интернет-проект о недвижимости. "
            "Это уникальный информационный портал, ресурсами которого может "
            "воспользоваться любой участник рынка недвижимости: "
            "строительные фирмы, продавцы и покупатели, арендаторы.\n"
            "Задача проекта: способствовать развитию рынка недвижимости в "
            "Полтаве и Полтавском районе.\n"
            "Наш сайт предоставляет покупателям свободный доступ к базе "
            "предложений о продаже и аренде недвижимости, "
            "продавцам – оптимизированный способ донесения информации всем "
            "потенциальным клиентам.\n"
            "С помощью нашего ресурса Вы сможете снять недвижимость, сдать "
            "недвижимость, купить недвижимость, "
            "продать недвижимость в Полтаве и Полтавском районе."
        ),
    )


@dp.callback_query_handler(
    inline_terms_dialog_cb_data.filter(action="payment_system"),
    state="*",
)
async def payment_system_button(query: types.CallbackQuery):
    await query.answer()

    doc_file = types.InputFile(
        "./docs/payment_system.pdf", filename="Пакетная система оплаты.pdf"
    )

    await bot.send_document(query.from_user.id, doc_file)


@dp.callback_query_handler(
    inline_terms_dialog_cb_data.filter(action="buyer_agreement"),
    state="*",
)
async def buyer_agreement_button(query: types.CallbackQuery):
    await query.answer()

    doc_file = types.InputFile(
        "./docs/buyer_agreement.pdf",
        filename="Договор сотрудничества (купля).pdf",
    )

    await bot.send_document(query.from_user.id, doc_file)


@dp.callback_query_handler(
    inline_terms_dialog_cb_data.filter(action="seller_agreement"),
    state="*",
)
async def seller_agreement_button(query: types.CallbackQuery):
    await query.answer()

    doc_file = types.InputFile(
        "./docs/seller_agreement.pdf",
        filename="Договор сотрудничества (продажа).pdf",
    )

    await bot.send_document(query.from_user.id, doc_file)


@dp.callback_query_handler(
    inline_terms_dialog_cb_data.filter(action="back"), state=MainStates.buying
)
async def terms_back_button(query: types.CallbackQuery):
    await query.answer()

    await bot.send_message(
        query.from_user.id,
        "Воспользуйтесь клавиатурой 👇",
        reply_markup=dialogs.MainMenuDialog(),
    )


# endregion


# region PreSearchMenuDialog handlers


@dp.message_handler(
    lambda message: message.text == "Задать параметры", state=MainStates.buying
)
async def set_parameters_button(message: types.Message, state: FSMContext):
    await bot.send_message(
        message.from_user.id,
        "Выбор района:",
        reply_markup=dialogs.DistrictSelectionDialog(
            districts,
            district_selection_dialog_cb_data,
        ),
    )


@dp.message_handler(
    lambda message: message.text == "По сохранённым параметрам",
    state=MainStates.buying,
)
async def favorites_menu_button(message: types.Message, state: FSMContext):
    state_data = await state.get_data()

    names = []

    for i in range(0, 3):
        names.append(state_data[f"property_group_{str(i)}"]["name"])

    await bot.send_message(
        message.from_user.id,
        "Избранное:",
        reply_markup=dialogs.InlineFavoritesDialog(
            inline_favorites_dialog_cb_data, names
        ),
    )


@dp.message_handler(
    lambda message: message.text == "Главное меню",
    state=[MainStates.buying, MainStates.editing],
)
async def main_menu_button(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        "Главное меню 👇",
        reply_markup=dialogs.MainMenuDialog(),
    )


# endregion


# region InlineFavoritesDialog handlers


@dp.callback_query_handler(
    inline_favorites_dialog_cb_data.filter(action="property_group"),
    state=MainStates.buying,
)
async def property_group_button(
    query: types.CallbackQuery, callback_data: CallbackData, state: FSMContext
):
    await query.answer()

    state_data = await state.get_data()

    index = callback_data["index"]

    property_group = state_data[f"property_group_{index}"]

    if property_group != {"name": property_group["name"]}:
        await state.update_data(current_property_group=property_group)
        await bot.send_message(
            query.from_user.id,
            "Воспользуйтесь клавиатурой 👇",
            reply_markup=dialogs.InlineSearchMenuDialog(
                inline_search_menu_dialog_cb_data
            ),
        )
        return

    await bot.send_message(
        query.from_user.id,
        (
            "Данный вариант параметров пуст. Пожалуйста, установите параметры"
            'с помощью кнопки "Редактировать"'
        ),
    )


@dp.callback_query_handler(
    inline_favorites_dialog_cb_data.filter(action="property_group"),
    state=MainStates.property_group_saving,
)
async def saving_property_group_button(
    query: types.CallbackQuery, callback_data: CallbackData, state: FSMContext
):
    await query.answer()

    await state.update_data(index=callback_data["index"])

    await bot.send_message(
        query.from_user.id, "Введите название варианта параметров:"
    )

    state_data = await state.get_data()

    await MainStates.property_group_naming.set()

    await state.update_data(state_data)


@dp.callback_query_handler(
    inline_favorites_dialog_cb_data.filter(action="property_group"),
    state=MainStates.editing,
)
async def edit_property_group_button(
    query: types.CallbackQuery, callback_data: CallbackData, state: FSMContext
):
    await query.answer()

    state_data = await state.get_data()

    index = callback_data["index"]

    await state.update_data(
        current_property_group=state_data[f"property_group_{index}"],
        index=index,
    )

    await bot.send_message(
        query.from_user.id,
        "Выбор района:",
        reply_markup=dialogs.DistrictSelectionDialog(
            districts, district_selection_dialog_cb_data
        ),
    )


@dp.callback_query_handler(
    inline_favorites_dialog_cb_data.filter(action="edit"),
    state=MainStates.buying,
)
async def edit_button(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    keyboard = query.message.reply_markup.inline_keyboard

    for i in range(0, 3):
        button_text = keyboard[i][0].text
        keyboard[i][0].text = f"🛠 {button_text}"

    await query.message.edit_reply_markup(
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    )

    await bot.send_message(
        query.from_user.id, "Пожалуйста, выберите вариант для редактирования."
    )

    state_data = await state.get_data()

    await MainStates.editing.set()

    await state.update_data(state_data)


# endregion


# region InlineSearchMenuDialog handlers


@dp.message_handler(
    lambda message: message.text == "Вернуться", state=MainStates.buying
)
async def back_button(message: types.Message):
    await database.dispose_post_cursor(message.from_user.id)
    await bot.send_message(
        message.from_user.id,
        "Воспользуйтесь клавиатурой 👇",
        reply_markup=dialogs.PreSearchMenuDialog(),
    )


@dp.callback_query_handler(
    inline_search_menu_dialog_cb_data.filter(action="pick"),
    state=MainStates.buying,
)
async def get_results_button(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    data = await state.get_data()

    current_property_group = data["current_property_group"]

    city_id = conversion.city_id[current_property_group["district"]]

    estate_type = current_property_group["estate_type"]

    if estate_type == "flat":
        type_object_id = "BETWEEN 1 AND 4"
    else:
        type_object_id = conversion.type_object_id[estate_type]

    type_pomesh_id = None

    if current_property_group["commerce_type"] != "":
        commerce_type = current_property_group["commerce_type"]
        type_pomesh_id = conversion.type_pomesh_id[commerce_type]

    await bot.send_message(query.from_user.id, "Пожалуйста, подождите...")

    await database.select_posts(
        city_id,
        type_object_id,
        current_property_group["room_count"],
        current_property_group["area"],
        current_property_group["price"],
        type_pomesh_id,
        query.from_user.id,
    )

    await send_posts(query.from_user.id, first_time=True)

    await bot.send_message(
        query.from_user.id,
        "Воспользуйтесь клавиатурой 👇",
        reply_markup=dialogs.PostSearchMenuDialog(),
    )


@dp.callback_query_handler(
    inline_search_menu_dialog_cb_data.filter(action="save_settings"),
    state=MainStates.buying,
)
async def save_to_property_group_button(
    message: types.Message, state: FSMContext
):
    state_data = await state.get_data()

    names = []

    for i in range(0, 3):
        names.append(state_data[f"property_group_{i}"]["name"])

    state_data = await state.get_data()

    await MainStates.property_group_saving.set()

    await state.update_data(state_data)

    await bot.send_message(
        message.from_user.id,
        "Выберите вариант параметров для сохранения:",
        reply_markup=dialogs.InlineFavoritesDialog(
            inline_favorites_dialog_cb_data, names, save_mode=True
        ),
    )


# endregion


async def send_posts(user_id: int, first_time: bool = False):
    posts = await database.fetch_posts(user_id)

    if district_record is None:
        logging.error("Error. No district record found in database.")
        return

    districts = dict()

    for district in district_record:
        districts[district["id"]] = district["name"]

    posts_sent = 0

    for post in posts:
        type_object_id = post["type_object_id"]
        post_id = post["id"]
        room_count = post["room_count"]
        ploshad = post["ploshad"]
        ploshad_gil = post["ploshad_gil"]
        rajon = districts[post["rajon_id"]]
        street = post["street"]
        if post["price"] != 0:
            price = post["price"]
        else:
            price = ""

        formatted_text = (
            f"✅ Площадь: {ploshad}\n\n"
            f"✅ Ориентир/улица: {rajon}, {street}\n\n"
            f"💵 Стоимость: {price} $"
        )

        if (ploshad_gil != "") and (type_object_id != 6):
            formatted_text = (
                f"✅ Площадь: {ploshad}\n\n"
                f"✅ Жил. Площадь: {ploshad_gil}\n\n"
                f"✅ Ориентир/улица: {rajon}, {street}\n\n"
                f"💵 Стоимость: {price} $"
            )

        if (
            (room_count is not None)
            and (type_object_id != 9)
            and (type_object_id != 6)
        ):
            formatted_text = (
                f"✅ Кол-во комнат: {room_count}\n\n" + formatted_text
            )

        post_url = f"https://dom24.com.ua/kartochka-obekta?item={post_id}"

        response = requests.get(post_url)

        try:
            post_html = response.content.decode("utf-8")
            post_soup = bs4.BeautifulSoup(post_html, features="html.parser")

            image_tag = post_soup.find(name="img", class_="image visible")

            image_src = image_tag["src"]  # type: ignore

            image_url = f"https://dom24.com.ua{image_src}"
        except UnicodeDecodeError:
            image_url = (
                "https://dom24.com.ua/images"
                "/placeholders/real-property-placeholder.jpg"
            )
        except TypeError:
            continue

        await bot.send_photo(
            user_id,
            photo=image_url,
            caption=formatted_text,
            reply_markup=dialogs.ShowOnWebDialog(post_url),
        )
        posts_sent += 1

    if (posts_sent == 0) and not first_time:
        await bot.send_message(
            user_id, "Вы просмотрели все объявления по указанным параметрам."
        )
    elif (posts_sent == 0) and first_time:
        await bot.send_message(
            user_id, "К сожалению, по указанным параметрам ничего не найдено."
        )


# region PostSearhMenuDialog handlers
@dp.message_handler(
    lambda message: message.text == "Ещё объекты", state=MainStates.buying
)
async def more_objects_button(message: types.Message):
    await send_posts(message.from_user.id)
    await bot.send_message(
        message.from_user.id,
        "Воспользуйтесь клавиатурой 👇",
        reply_markup=dialogs.PostSearchMenuDialog(),
    )


@dp.message_handler(
    lambda message: message.text == "Получать обновления",
    state=MainStates.buying,
)
async def get_updates_button(message: types.Message):
    pass


# endregion


# region DistrictSelectionDialog handler


@dp.callback_query_handler(
    district_selection_dialog_cb_data.filter(
        action=[districts[item] for item in districts]
    ),
    state="*",
)
async def district_selection_button(
    query: types.CallbackQuery,
    callback_data: dict[str, str],
    state: FSMContext,
):
    await query.answer()

    state_data = await state.get_data()

    current_property_group = state_data["current_property_group"]

    current_property_group["district"] = callback_data["action"]

    await state.update_data(current_property_group=current_property_group)

    await bot.send_message(
        query.from_user.id,
        "Выбор типа собственности:",
        reply_markup=dialogs.EstateTypeSelectionDialog(
            callback_data["action"], estate_selection_dialog_cb_data
        ),
    )


# endregion


# region EstateTypeSelectionDialog handlers


@dp.callback_query_handler(
    estate_selection_dialog_cb_data.filter(
        action=["flat", "room", "house", "country_house", "claim", "commerce"]
    ),
    state=[MainStates.buying, MainStates.editing],
)
async def estate_buy_button(
    query: types.CallbackQuery,
    callback_data: dict[str, str],
    state: FSMContext,
):

    await query.answer()

    state_data = await state.get_data()

    current_property_group = state_data["current_property_group"]

    current_property_group["estate_type"] = callback_data["action"]

    await state.update_data(current_property_group=current_property_group)

    await send_properties_dialog(query.from_user.id, current_property_group["estate_type"])


@dp.callback_query_handler(
    estate_selection_dialog_cb_data.filter(
        action=["flat", "room", "house", "country_house", "claim", "commerce"]
    ),
    state=MainStates.selling,
)
async def estate_sell_button(
    query: types.CallbackQuery,
    callback_data: dict[str, str],
    state: FSMContext,
):

    await query.answer()

    state_data = await state.get_data()

    current_property_group = state_data["current_property_group"]

    current_property_group["estate_type"] = callback_data["action"]

    await state.update_data(current_property_group=current_property_group)

    await send_sell_menu_message(query.from_user.id)


async def send_sell_menu_message(user_id: int):
    await bot.send_message(
        user_id,
        "Воспользуйтесь клавиатурой 👇",
        reply_markup=dialogs.SellMenuDialog(),
    )


async def send_properties_dialog(
    user_id: int, estate_type: str, selling: bool = False
):
    await bot.send_message(
        user_id,
        "Пожалуйста, уточните параметры собственности.",
        reply_markup=dialogs.InlinePropertiesDialog(
            inline_properties_dialog_cb_data, estate_type, selling=selling
        ),
    )


# endregion


# region InlinePropertiesDialog handlers


@dp.callback_query_handler(
    inline_properties_dialog_cb_data.filter(
        property=["room_count", "area", "price"]
    ),
    state=[MainStates.buying, MainStates.editing],
)
async def data_change_handler(
    query: types.CallbackQuery,
    callback_data: dict[str, str],
    state: FSMContext,
):
    state_data = await state.get_data()
    current_property_group = state_data["current_property_group"]

    keyboard = query.message.reply_markup.inline_keyboard

    row_index = int(callback_data["row_index"])
    column_index = int(callback_data["column_index"])

    if "✅" not in keyboard[row_index][column_index].text:
        keyboard[row_index][column_index].text = (
            "✅ " + keyboard[row_index][column_index].text
        )

        current_property_group[callback_data["property"]].append(
            callback_data["filter"]
        )
    else:
        keyboard[row_index][column_index].text = keyboard[row_index][
            column_index
        ].text[1:]

        current_property_group[callback_data["property"]].remove(
            callback_data["filter"]
        )

    await state.update_data(current_property_group=current_property_group)

    await query.message.edit_reply_markup(
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    )

    await query.answer()


@dp.callback_query_handler(
    inline_properties_dialog_cb_data.filter(
        property=["room_count", "area", "price"]
    ),
    state=MainStates.selling,
)
async def selling_data_change_handler(
    query: types.CallbackQuery,
    callback_data: dict[str, str],
    state: FSMContext,
):
    state_data = await state.get_data()
    current_property_group = state_data["current_property_group"]

    keyboard = query.message.reply_markup.inline_keyboard

    row_index = int(callback_data["row_index"])
    column_index = int(callback_data["column_index"])

    if "✅" not in keyboard[row_index][column_index].text:
        current_property_group[callback_data["property"]].append(
            keyboard[row_index][column_index].text
        )

        keyboard[row_index][column_index].text = (
            "✅ " + keyboard[row_index][column_index].text
        )
    else:
        keyboard[row_index][column_index].text = keyboard[row_index][
            column_index
        ].text[1:]

        current_property_group[callback_data["property"]].remove(
            keyboard[row_index][column_index].text
        )

    await state.update_data(current_property_group=current_property_group)

    await query.message.edit_reply_markup(
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
    )

    await query.answer()


@dp.callback_query_handler(
    inline_properties_dialog_cb_data.filter(property="commerce"),
    state=MainStates.buying,
)
async def commerce_buttons_handler(
    query: types.CallbackQuery,
    callback_data: dict[str, str],
    state: FSMContext,
):
    await query.answer()

    state_data = await state.get_data()

    current_property_group = state_data["current_property_group"]

    current_property_group["commerce_type"] = callback_data["filter"]

    await state.update_data(current_property_group=current_property_group)

    await bot.send_message(
        query.from_user.id,
        "Воспользуйтесь клавиатурой 👇",
        reply_markup=dialogs.InlineSearchMenuDialog(
            inline_search_menu_dialog_cb_data
        ),
    )


@dp.callback_query_handler(
    inline_properties_dialog_cb_data.filter(property="commerce"),
    state=MainStates.selling,
)
async def selling_commerce_buttons_handler(
    query: types.CallbackQuery,
    callback_data: dict[str, str],
    state: FSMContext,
):
    await query.answer()

    state_data = await state.get_data()

    current_property_group = state_data["current_property_group"]

    current_property_group["commerce_type"] = callback_data["filter"]

    await state.update_data(current_property_group=current_property_group)

    sale_type = "Коммерция"

    state_data = await state.get_data()

    current_property_group = state_data["current_property_group"]

    first_name = query.from_user.first_name

    last_name = query.from_user.last_name

    formatted_text = await generate_sale_formatted_text(
        first_name, last_name, current_property_group, sale_type
    )

    await state.update_data(formatted_text=formatted_text)

    await bot.send_message(
        query.from_user.id,
        "Пожалуйста, отправьте нам контакт, чтобы мы смогли с вами связаться.",
        reply_markup=dialogs.PhoneRetreivalDialog(),
    )


@dp.callback_query_handler(Text("accept"), state=MainStates.buying)
async def accept_button(query: types.CallbackQuery):
    await query.answer()

    await bot.send_message(
        query.from_user.id,
        "Воспользуйтесь клавиатурой 👇",
        reply_markup=dialogs.InlineSearchMenuDialog(
            inline_search_menu_dialog_cb_data
        ),
    )


@dp.callback_query_handler(Text("sell_fast"), state=MainStates.selling)
async def sell_fast_button(
    query: types.CallbackQuery,
    state: FSMContext,
):
    await query.answer()

    sale_type = "Быстрая продажа"

    state_data = await state.get_data()

    current_property_group = state_data["current_property_group"]

    first_name = query.from_user.first_name

    last_name = query.from_user.last_name

    formatted_text = await generate_sale_formatted_text(
        first_name, last_name, current_property_group, sale_type
    )

    await state.update_data(formatted_text=formatted_text)

    await bot.send_message(
        query.from_user.id,
        "Пожалуйста, отправьте нам контакт, чтобы мы смогли с вами связаться.",
        reply_markup=dialogs.PhoneRetreivalDialog(),
    )


@dp.callback_query_handler(Text("sell_expensive"), state=MainStates.selling)
async def sell_expensive_button(
    query: types.CallbackQuery,
    state: FSMContext,
):
    await query.answer()

    sale_type = "Продажа дорого"

    state_data = await state.get_data()

    current_property_group = state_data["current_property_group"]

    first_name = query.from_user.first_name

    last_name = query.from_user.last_name

    formatted_text = await generate_sale_formatted_text(
        first_name, last_name, current_property_group, sale_type
    )

    await state.update_data(formatted_text=formatted_text)

    await bot.send_message(
        query.from_user.id,
        "Пожалуйста, отправьте нам контакт, чтобы мы смогли с вами связаться.",
        reply_markup=dialogs.PhoneRetreivalDialog(),
    )


async def generate_sale_formatted_text(
    first_name: str,
    last_name: str,
    current_property_group: dict,
    sale_type: str,
):
    district = current_property_group["district"]
    district_localized = conversion.operator_district[district]

    estate_type = current_property_group["estate_type"]
    estate_type_localized = conversion.operator_estate_type[estate_type]

    commerce_type = "N/A"

    if current_property_group["commerce_type"] != "":
        commerce_type = conversion.operator_commerce_type[
            current_property_group["commerce_type"]
        ]

    room_count_formatted = ""

    for item in current_property_group["room_count"]:
        room_count_formatted += f"{item}, "

    area_formatted = ""

    for item in current_property_group["area"]:
        area_formatted += f"{item}, "

    price_formatted = ""

    for item in current_property_group["price"]:
        price_formatted += f"{item}, "

    if estate_type == "room":
        return (
            "Сообщение о продаже"
            f" от пользователя: {first_name} {last_name}\n\n"
            f"Город/область: {district_localized}\n"
            f"Типа помещения: {estate_type_localized}\n"
            f"Количество комнат: {room_count_formatted}\n"
            f"Площадь: {area_formatted}\n"
            f"Цена: {price_formatted}\n"
            f"Тип продажи: {sale_type}\n"
        )
    else:
        return (
            "Сообщение о продаже"
            f" от пользователя: {first_name} {last_name}\n\n"
            f"Город/область: {district_localized}\n"
            f"Тип собственности: {estate_type_localized}\n"
            f"Типа помещения: {commerce_type}\n"
            f"Количество комнат: {room_count_formatted}\n"
            f"Площадь: {area_formatted}\n"
            f"Цена: {price_formatted}\n"
            f"Тип продажи: {sale_type}\n"
        )


@dp.callback_query_handler(Text("accept"), state=MainStates.editing)
async def editing_accept_button(query: types.CallbackQuery, state: FSMContext):
    await query.answer()

    await bot.send_message(
        query.from_user.id, "Введите название варианта параметров:"
    )

    state_data = await state.get_data()

    await MainStates.property_group_naming.set()

    await state.update_data(state_data)


@dp.callback_query_handler(
    inline_properties_dialog_cb_data.filter(property="commerce"),
    state=MainStates.editing,
)
async def editing_commerce_buttons_handler(
    query: types.CallbackQuery,
    callback_data: dict[str, str],
    state: FSMContext,
):
    await query.answer()

    state_data = await state.get_data()

    current_property_group = state_data["current_property_group"]

    current_property_group["commerce_type"] = callback_data["filter"]

    await state.update_data(current_property_group=current_property_group)

    await bot.send_message(
        query.from_user.id, "Введите название варианта параметров:"
    )

    state_data = await state.get_data()

    await MainStates.property_group_naming.set()

    await state.update_data(state_data)


@dp.message_handler(state=MainStates.property_group_naming)
async def property_group_naming_prompt(
    message: types.Message, state: FSMContext
):
    name = message.text

    state_data = await state.get_data()

    index = int(state_data["index"])

    names = []

    for i in range(0, 3):
        names.append(state_data[f"property_group_{str(i)}"]["name"])

    names[index] = name

    await bot.send_message(
        message.from_user.id,
        f"Вариант параметров '{name}' успешно сохранён.",
        reply_markup=dialogs.InlineFavoritesDialog(
            inline_favorites_dialog_cb_data, names
        ),
    )

    state_data = await state.get_data()

    await MainStates.buying.set()

    await state.update_data(state_data)

    state_data = await state.get_data()

    state_data[f"property_group_{index}"] = state_data[
        "current_property_group"
    ]

    state_data[f"property_group_{index}"]["name"] = name

    await state.update_data(**state_data)


# Utility handler. Needed to answer queries for decorative buttons


@dp.callback_query_handler(Text("blank"))
async def black_handler(query: types.CallbackQuery):

    await query.answer()


async def send_search_menu(user_id: int):
    await bot.send_message(
        user_id,
        "Меню поиска 👇",
        reply_markup=dialogs.InlineSearchMenuDialog(
            inline_search_menu_dialog_cb_data
        ),
    )


# endregion


# region SellMenuDialog handlers


@dp.message_handler(
    lambda message: message.text == "Далее",
    state=MainStates.selling
)
async def next_sell_menu_button(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    current_property_group = state_data["current_property_group"]
    await send_properties_dialog(
        message.from_user.id, current_property_group["estate_type"], selling=True
    )


# endregion


# region PhoneRetreivalDialog handler


@dp.message_handler(
    state=MainStates.buying,
    content_types=types.ContentType.CONTACT,
)
async def phone_retrieval_buying_button(message: types.Message):
    await bot.send_message(OPERATOR_TELEGRAM_ID, "Клиент просит перезвонить:")
    await bot.send_contact(
        OPERATOR_TELEGRAM_ID,
        message.contact.phone_number,
        message.from_user.first_name,
    )

    await bot.send_message(
        message.from_user.id,
        "Наш менеджер перезвонит вам как можно быстрее.",
        reply_markup=dialogs.StartDialog(),
    )


@dp.message_handler(
    state=MainStates.selling,
    content_types=types.ContentType.CONTACT,
)
async def phone_retrieval_selling_button(
    message: types.Message, state: FSMContext
):
    await bot.send_message(OPERATOR_TELEGRAM_ID, "Объявление о продаже от:")
    await bot.send_contact(
        OPERATOR_TELEGRAM_ID,
        message.contact.phone_number,
        message.from_user.first_name,
    )

    await bot.send_message(
        message.from_user.id,
        "Наш менеджер перезвонит вам как можно быстрее.",
        reply_markup=dialogs.StartDialog(),
    )

    state_data = await state.get_data()

    formatted_text = state_data["formatted_text"]

    await bot.send_message(OPERATOR_TELEGRAM_ID, formatted_text)


@dp.message_handler(
    lambda message: message.text == "Вернуться",
    state=MainStates.selling,
)
async def sell_menu_back_button(message: types.Message):
    await back_to_start_button(message)


# endregion


@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(update, error):

    return True


if __name__ == "__main__":
    district_record = database.select_districts()
    executor.start_polling(dp, skip_updates=True)
