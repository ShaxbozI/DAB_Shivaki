import random
from aiogram import Router, F, Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    ContentType,
    ChatMemberUpdated,
    ReplyKeyboardMarkup,
    KeyboardButton,
    chat_member_updated, 
    CallbackQuery, 
    FSInputFile,
    InputMediaPhoto,
    ReplyKeyboardRemove,
)
from aiogram.types.chat_member import ChatMember
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject, Command, Filter, ChatMemberUpdatedFilter, StateFilter

from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from states import FAQ, MAI, BroadcastStates, PhotoAddorUpdate, BookAddorUpdate
from loader import bot, ADMIN_ID

from buttons import cancel_kb, generate_inline_keyboard, paginator, product_types_kb, error_types_kb, get_main_kb, add_or_update_info
from api import (
    admin_users,
    all_errors,
    all_product_types,
    all_products, 
    manual_info, 
    product_errors, 
    product_info, 
    products, 
    error_info, 
    save_manual,
    save_or_update_error,
    save_or_update_product,
    save_or_update_product_type, 
    save_or_update_user, 
    search_error_info, 
    users,
    all_info_users,
)



router: Router = Router()

staf_admin_id = ADMIN_ID

class MyFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text

    async def __call__(self, message: Message) -> bool:
        return message.text == self.my_text




"""_______________"/start" buyrug'iga javob beruvchi handler_________________"""


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    name = message.from_user.full_name
    username = message.from_user.username if message.from_user.username else "Noma'lum"  # Agar username mavjud bo'lmasa, "Noma'lum"
    
    # Holatni tozalash
    if await state.get_state() is not None:
        await state.clear()

    user_id = message.from_user.id
    admin_users_id = admin_users()  # Admin foydalanuvchilar ro'yxatini olish

    # Asosiy menyuni dinamik ravishda yaratish
    main_kb = get_main_kb(user_id, admin_users_id)
    
    # Foydalanuvchi ro'yxatini olish
    users_list = users()

    if user_id in users_list:
        # Foydalanuvchi mavjud bo'lsa, yangilash
        result = save_or_update_user(user_id, name, username, is_active=True)
        await message.answer(f"Qaytganingizdan xursandmiz, {hbold(name)}!", reply_markup=main_kb)

        all_users = len(all_info_users())
        active_users = len([user for user in all_info_users() if user['is_active']])
        deactive_users = all_users - active_users  # Passiv foydalanuvchilar soni
        # Adminga xabar yuborish
        await bot.send_message(
            chat_id=staf_admin_id,
            text=(
                f"Id raqami {user_id} bo'lgan {username} (Ismi: {name}) foydalanuvchi botni qayta ishga tushirdi. \n\n"
                f"👥 Umumiy foydalanuvchilar soni: {all_users}. \n"
                f"✅ Aktiv foydalanuvchilar soni: {active_users}. \n"
                f"⚠️ Aktiv bo'lmagan foydalanuvchilar soni: {deactive_users}."
            )
        )
    else:
        # Yangi foydalanuvchini qo'shish
        result = save_or_update_user(user_id, name, username, is_active=True)
        await message.answer(f"Salom, {hbold(name)} xush kelibsiz!", reply_markup=main_kb)

        all_users = len(all_info_users())
        active_users = len([user for user in all_info_users() if user['is_active']])
        deactive_users = all_users - active_users  # Passiv foydalanuvchilar soni
        # Adminga xabar yuborish
        await bot.send_message(
            chat_id=staf_admin_id,
            text=(
                f"Id raqami {user_id} bo'lgan {username} (Ismi: {name}) foydalanuvchi qo'shildi. \n\n"
                f"👥 Umumiy foydalanuvchilar soni: {all_users}. \n"
                f"✅ Aktiv foydalanuvchilar soni: {active_users}. \n"
                f"⚠️ Aktiv bo'lmagan foydalanuvchilar soni: {deactive_users}."
            )
        )





# Bekor qilish handler
@router.message(Command("cancel"))  # /cancel komanda uchun
@router.message(lambda message: message.text == "❌ Bekor qilish")  # "Bekor qilish" tugmasi uchun
async def cancel_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    admin_users_id = admin_users()  # Admin foydalanuvchilar ro'yxatini olish

    # Asosiy menyuni dinamik ravishda yaratish
    main_kb = get_main_kb(user_id, admin_users_id)
    
    # Holatni tozalash
    if await state.get_state() is not None:  # Agar holat mavjud bo'lsa
        await state.clear()  # Holatni tozalash
        await message.answer(
            text="Jarayon to'xtatildi. Kerkali bo'limdan foydalanishingiz mumkin.",
            reply_markup=main_kb  # Tugmalarni tozalash
        )
    else:
        await message.answer(
            text="Sizda aktiv Jarayon yo'q. Kerkali bo'limdan foydalanishingiz mumkin.",
            reply_markup=main_kb
        )




@router.my_chat_member()
async def handle_user_left_in_private(event: ChatMemberUpdated):

    if event.old_chat_member.status != "kicked" and event.new_chat_member.status == "kicked":
        user_id = event.from_user.id
        user_name = event.from_user.full_name
        username = event.from_user.username

        # Foydalanuvchini o'chirilgan deb belgilash
        save_or_update_user(user_id, user_name, username, is_active=False)
        # Foydalanuvchi ro'yxatini olish
        all_users = len(all_info_users())
        active_users = len([user for user in all_info_users() if user['is_active']])
        deactive_users = all_users - active_users  # Passiv foydalanuvchilar soni
        # Adminga xabar yuborish
        await bot.send_message(
            chat_id=staf_admin_id,
            text=f"Id raqami {user_id} bo'lgan {username} (Ismi: {user_name}) botni shaxsiy chatda blok qildi. \n\n"
                f"👥 Umumiy foydalanuvchilar soni: {all_users}. \n"
                f"✅ Aktiv foydalanuvchilar soni: {active_users}. \n"
                f"⚠️ Aktiv bo'lmagan foydalanuvchilar soni: {deactive_users}."
        )





"""_______________"/rn" buyrug'iga javob beruvchi handler_________________""" 
"""       Bu random son qaytaruvchi handler         """  
     
@router.message(Command(commands=["rn"]))
async def random_number(message: Message, command: CommandObject):
    a, b = [int(n) for n in command.args.split('-')]
    rnum = random.randint(a, b)
    
    await message.reply(f"Random number: {rnum}")




"""_______________"Asosiyga qaytish" tugmasiga javob beruvchi handler_________________"""

@router.callback_query(F.data == "asosiy_sahifa")
async def paginate_callback(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id  # Foydalanuvchi ID sini olish
    admin_users_id = admin_users()  # Admin foydalanuvchilar ro'yxatini olish

    # Asosiy menyuni dinamik ravishda yaratish
    main_kb = get_main_kb(user_id, admin_users_id)
    
    await callback_query.message.answer("Kerakili tugmani tanlang!", reply_markup=main_kb)


@router.message(lambda message: message.text == "🏠 Asosiyga qaytish")
async def ask_question_or_suggestion(message: Message, state: FSMContext):
    user_id = message.from_user.id  # Foydalanuvchi ID sini olish
    admin_users_id = admin_users()  # Admin foydalanuvchilar ro'yxatini olish

    # Asosiy menyuni dinamik ravishda yaratish
    main_kb = get_main_kb(user_id, admin_users_id)
    
    await message.answer("Kerakili tugmani tanlang!", reply_markup=main_kb)




@router.message(MyFilter("Mahsulotlar"))
async def show_types(message: Message):
    await message.answer("Mahsulot turlari", reply_markup=product_types_kb)




@router.message(MyFilter("Xatolik kodlari"))
async def show_types(message: Message):
    await message.answer("Tur bo'yicha yuzaga kelishi mumkin bo'lgan xatoliklarni ko'rishingiz mumkin bunig uchun turni tanlang", reply_markup=error_types_kb)




# @router.callback_query(lambda c: c.data.startswith('paginator_'))
# async def paginate_callback(callback_query: CallbackQuery):
#     # Sahifa raqamini va parametrni ajratib olish
#     data_parts = callback_query.data.split('_')
#     page = int(data_parts[1])
#     page_name = data_parts[2]

#     # Sahifalar bo'yicha tartib va kontentni boshqarish
#     if page == 1:
#         data = paginator(page=page)
#         title = data["title"]
#         keyboard = data["keyboard"]
#         await callback_query.message.edit_text(title, reply_markup=keyboard)
        
#     elif page == 2 and page_name:
#         data = paginator(page=page, item=page_name)
#         title = data["title"]
#         keyboard = data["keyboard"]
        
#         await callback_query.message.answer(title, reply_markup=keyboard)
        
#     elif page == 3:
#         data = paginator(page=page, item=page_name)
#         product_data = product_info(page_name)
#         title = data["title"]
#         keyboard = data["keyboard"]
#         print(data)
#         # Surat 'file_id'sini belgilash
#         photo = product_data['photo_id'] if product_data['photo_id'] else None
#         book = product_data['book_id'] if product_data['book_id'] else None
#         if photo is not None: 
#             await callback_query.message.answer_photo(photo)
            
#         if book is not None: 
#             await callback_query.message.answer_document(
#                 book, 
#                 caption=f"Turi: <b>{product_data['product_type']}</b>\n"
#                     f"Model: <b>{product_data['name']}</b>\n"
#                     "Mahsulot haqida ko'proq bilib oling\n",
#                     reply_markup=keyboard,
#                     parse_mode="HTML"  # HTML formatini qo'llash
#                 )
#         else:
#         # Xabarlar yuborish
#             await callback_query.message.answer(
#                 f"Turi: <b>{product_data['product_type']}</b>\n"
#                 f"Model: <b>{product_data['name']}</b>\n"
#                 "Mahsulot haqida ko'proq bilib oling\n",
#                 reply_markup=keyboard,
#                 parse_mode="HTML"  # HTML formatini qo'llash
#             )
    
#     elif page == 4:
#         data = paginator(page=page, item=page_name)
#         title = data["title"]
#         keyboard = data["keyboard"]
        
#         await callback_query.message.edit_text(title, reply_markup=keyboard)
    
#     elif page == 20:
#         data = paginator(page=page)
#         title = data["title"]
#         keyboard = data["keyboard"]
        
#         await callback_query.message.edit_text(title, reply_markup=keyboard)
        
#     elif page == 21 and page_name:
#         data = paginator(page=page, item=page_name)
#         title = data["title"]
#         keyboard = data["keyboard"]
        
#         await callback_query.message.edit_text(title, reply_markup=keyboard)
    
#     elif page == 30:
#         data = paginator(page=page)
#         title = data["title"]
#         keyboard = data["keyboard"]
        
#         await callback_query.message.edit_text(title, reply_markup=keyboard)
    
#     elif page == 31 and page_name:
#         data = paginator(page=page, item=page_name)
#         title = data["title"]
#         keyboard = data["keyboard"]
        
#         await callback_query.message.edit_text(title, reply_markup=keyboard)
    
#     elif page == 32:
#         data = paginator(page=page, item=page_name)
#         title = data["title"]
#         keyboard = data["keyboard"]
        
#         await callback_query.message.edit_text(title, reply_markup=keyboard)
        
#     else:
#         title = "Noto'g'ri sahifa tanlandi."
#         keyboard = None
#         await callback_query.message.edit_text(title, reply_markup=keyboard)



@router.callback_query(lambda c: c.data.startswith('paginator_'))
async def paginate_callback(callback_query: CallbackQuery):
    data_parts = callback_query.data.split('_')
    page = int(data_parts[1])
    page_name = data_parts[2] if len(data_parts) > 2 else None  # Ba'zi sahifalar uchun page_name kerak emas

    # Sahifalar bo'yicha ma'lumot olish
    data = paginator(page=page, item=page_name)
    title = data["title"]
    keyboard = data["keyboard"]

    # 2-sahifa: Mahsulot turlari yoki ichki turlari
    if page == 2 and page_name:
        await callback_query.message.answer(title, reply_markup=keyboard)

    # 3-sahifa: Mahsulot haqida ma'lumot
    elif page == 3 and page_name:
        product_data = product_info(page_name)

        # Rasm va hujjatni jo‘natish
        if product_data.get('photo_id'):
            await callback_query.message.answer_photo(product_data['photo_id'])

        if product_data.get('book_id'):
            await callback_query.message.answer_document(
                product_data['book_id'],
                caption=f"Turi: <b>{product_data['product_type']}</b>\n"
                        f"Model: <b>{product_data['name']}</b>\n"
                        "Mahsulot haqida ko'proq bilib oling\n",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        else:
            await callback_query.message.answer(
                f"Turi: <b>{product_data['product_type']}</b>\n"
                f"Model: <b>{product_data['name']}</b>\n"
                "Mahsulot haqida ko'proq bilib oling\n",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
    
    # 31-sahifa: Mahsulot turlari yoki ichki turlari
    elif page == 31 and page_name:
        await callback_query.message.answer(title, reply_markup=keyboard)
        
    # 3-sahifa: Mahsulot haqida ma'lumot
    elif page == 32 and page_name:
        product_data = product_info(page_name)

        # Rasm va hujjatni jo‘natish
        if product_data.get('photo_id'):
            await callback_query.message.answer_photo(product_data['photo_id'])

        if product_data.get('book_id'):
            await callback_query.message.answer_document(
                product_data['book_id'],
                caption=f"Turi: <b>{product_data['product_type']}</b>\n"
                        f"Model: <b>{product_data['name']}</b>\n"
                        "Mahsulot haqida ko'proq bilib oling\n",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        else:
            await callback_query.message.answer(
                f"Turi: <b>{product_data['product_type']}</b>\n"
                f"Model: <b>{product_data['name']}</b>\n"
                "Mahsulot haqida ko'proq bilib oling\n",
                reply_markup=keyboard,
                parse_mode="HTML"
            )

    # Qolgan barcha sahifalar uchun
    else:
        await callback_query.message.edit_text(title, reply_markup=keyboard)








@router.callback_query(lambda c: c.data.startswith('errors_')) 
async def callback_error_codes(callback_query: CallbackQuery):
    product_name = callback_query.data.split("_", 1)[1]  # callback data'dan mahsulot nomini olish
    # print(product_name)
    product_errors_data = product_errors(product_name)  # Mahsulot ma'lumotlarini olish
    
    # print(f"mahsulot xaxtolik kodlari: {product_errors_data}")
    
    if isinstance(product_errors_data, list) and product_errors_data:
    # Xatolik kodlari tugmalarini yaratish
        error_buttons = [
            InlineKeyboardButton(text=f"{item['name']}", callback_data=f'error_{item["id"]}')
            for item in product_errors_data if "name" in item  # Tugma yaratishdan oldin tekshirish
        ]

        if error_buttons:
            # Xatolik kodlarini 5 tadan bo'lib chiqarish
            error_rows = [error_buttons[i:i+5] for i in range(0, len(error_buttons), 5)]

            # Xatolik kodlari tugmalarini yuborish
            await callback_query.message.answer(
                text=f"<b>{product_name}</b> modelda yuzaga keluvchi xatoliklar ro'yhati.\n"
                    "O'zingizga kerak bo'lgan Xatolik kodi ustiga bosing va muammo nimada ekanligini bilib oling.",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=error_rows)
            )
        else:
            await callback_query.message.answer("Xatolik kodlari topilmadi.")
    else:
        # Agar product_errors_data list emas yoki xabar bo'lsa
        if isinstance(product_errors_data, dict) and "message" in product_errors_data:
            await callback_query.message.answer(product_errors_data["message"])
        else:
            await callback_query.message.answer("Xatolik kodlari haqida ma’lumot olishda muammo yuzaga keldi.")





"""_______________"Xatolik kodlari" Tugmalari ustida amallar_________________"""

# Xatolik kodi tanlanganda uning malumotlarini ko'rsatish
@router.callback_query(lambda c: c.data.startswith('error_'))
async def callback_product_info(callback_query: CallbackQuery):
    error_id = callback_query.data.split("_", 1)[1]  # callback data'dan mahsulot nomini olish
    # print(f"error id : {error_id}")
    error_data = error_info(error_id)
    # print(f"xatolik malumotlari: {error_data}")
    if error_data['photo_id']:
        # Surat URL'sini belgilash
        photo = error_data['photo_id']
         
        await callback_query.message.answer_photo(photo)

    else:
        await callback_query.message.answer(f"<b>{error_data['name']}:</b> Xatolik kodi haqida ma'lumot topilmadi.")




"""_______________"Savol yoki Takliflar" tugmasi bosilganda javob beruvchi handler_________________""" 
"""       Bu foydalanuvchi tigmani bosganini aniqlaydi va holatni belgilaydi handler         """  

# Savol yoki murojaat boshlash handler
@router.message(lambda message: message.text == "Savol yoki Takliflar")
async def ask_question_or_suggestion(message: Message, state: FSMContext):
    await message.answer(
        "Iltimos, savolingiz yoki taklifingizni yozib yuboring. Biz sizga imkon qadar tezroq javob beramiz.",
        reply_markup=cancel_kb,
    )
    await state.set_state(FAQ.murojaat)



"""_______________Yuqoridagilardan o'tgan barcha buyruq va xabarlarga javob beruvchi handler_________________"""
"""       Bu ko'rsailgan xatolik kodiga tegishli malumotlarni qaytaruvchi handler sifatida ham ishlaydi         """
    

# Murojaatni qabul qilish va adminlarga yuborish handler
@router.message(StateFilter(FAQ.murojaat))
async def faq(message: Message, state: FSMContext):
    user_message = message.text  # Foydalanuvchi yozgan matn
    user_id = message.from_user.id  # Foydalanuvchi ID
    user_full_name = message.from_user.full_name  # Foydalanuvchi to‘liq ismi
    user_username = message.from_user.username or "username mavjud emas"  # Foydalanuvchi username
    
    admin_users_id = admin_users()
    # Foydalanuvchi ma’lumotlarini holatga saqlash
    await state.update_data(
        murojaat=user_message, 
        user_id=user_id, 
        user_full_name=user_full_name, 
        user_username=user_username
    )

    # Foydalanuvchiga tasdiq xabarini yuborish
    await message.answer(
        "Qabul qilindi! Admin javobini kuting yoki muloqotni to‘xtating. Bu holatda ham admin albatta sizga javob qaytaradi.",
        reply_markup=cancel_kb,
    )

    # Adminlarga murojaatni yuborish
    for admin_id in admin_users_id:
        await bot.send_message(
            chat_id=admin_id,
            text=(
                f"📩 <b>Yangi murojaat!</b>\n\n"
                f"👤 Foydalanuvchi: {user_full_name}\n"
                f"🆔 ID: {user_id}\n"
                f"📎 Username: @{user_username}\n\n"
                f"📨 Murojaat matni:\n{user_message}"
            ),
            parse_mode="HTML"
        )




@router.message(lambda message: message.reply_to_message and "Yangi murojaat!" in message.reply_to_message.text)
async def admin_reply_handler(message: Message):
    try:
        # Reply qilingan xabardagi foydalanuvchi ID va murojaat matnini topish
        original_message = message.reply_to_message.text
        user_id_line = [line for line in original_message.split("\n") if "🆔 ID:" in line]
        user_message_line = [line for line in original_message.split("\n") if "📨 Murojaat matni:"]
        admin_users_id = admin_users()

        if not user_id_line:
            await message.answer("Foydalanuvchi ID sini aniqlab bo'lmadi.")
            return

        user_id = int(user_id_line[0].split("🆔 ID:")[1].strip())  # Foydalanuvchi ID ni olish
        # print(user_id)

        # Foydalanuvchiga javob yuborish
        try:
            await bot.send_message(
                chat_id=user_id,
                text=(f"👤 Admin sizga javob berdi:\n\n"
                      f"📩 {message.text}"),  # Adminning javobi
                parse_mode="HTML"
            )
            user_notified = True
        except Exception as e:
            user_notified = False
            print(f"Xatolik foydalanuvchiga yuborishda: {e}")

        # Adminlarga tasdiq yuborish
        for admin_id in admin_users_id:
            if admin_id != message.from_user.id:  # Javob bergan adminni o'ziga yubormaslik
                await bot.send_message(
                    chat_id=admin_id,
                    text=(f"⚠️ <b>Admin javob berdi!</b>\n\n"
                          f"👤 Foydalanuvchi ID: {user_id}\n"
                          f"📨 Foydalanuvchi murojaati:\n{user_message_line[-1]}\n\n"
                          f"📎 Javob bergan admin: {message.from_user.full_name}\n"
                          f"📨 Adminning javobi:\n{message.text}\n\n"
                          f"✅ Foydalanuvchiga xabar { 'YETIB BORDI' if user_notified else 'YETIB BORMADI (foydalanuvchi botni bloklagan yoki start bosmagan)' }"),
                    parse_mode="HTML"
                )

        # Javob bergan admin uchun tasdiq xabari
        if user_notified:
            await message.answer("Javob foydalanuvchiga muvaffaqiyatli yuborildi va boshqa adminlar xabardor qilindi.")
        else:
            await message.answer("⚠️ Foydalanuvchiga javob yuborilmadi! U botni bloklagan yoki start bosmagan bo‘lishi mumkin.")

    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")




"""_______________"Qo'llanma va Malumotlar" tugmasi bosilganda javob beruvchi handler_________________""" 

# Qo'llanma va Malumotlar tugmasi uchun handler
@router.message(lambda message: message.text == "Qo'llanma va Malumotlar")
async def ask_question_or_suggestion(message: Message, state: FSMContext):
    manuals = manual_info()  # Barcha qo'llanmalarni olish

    if not manuals:
        await message.answer("Hozircha hech qanday qo‘llanma yoki ma'lumot mavjud emas.")
        return

    await message.answer("Barcha qo'llanma va ma'lumotlarni ko'rishingiz mumkin.")

    found_valid_file = False  # Fayl topilganligini tekshirish uchun flag

    for manual in manuals:
        file_name = manual.get("name")
        file_id = manual.get("file_id")

        if file_name and file_id:
            try:
                # Faylni yuborishga harakat qilamiz
                await message.answer_document(
                    document=file_id,
                    caption=f"📂 : {file_name}",
                    parse_mode="HTML"
                )
                found_valid_file = True  # Agar fayl to'g'ri bo'lsa, flagni o'zgartiramiz

            except TelegramBadRequest:
                # print(f"Xatolik: {file_name} fayli ushbu botga tegishli emas.")
                continue  # Xato bo‘lsa, keyingi faylga o‘tish

    # Agar hech qanday fayl botga tegishli bo'lmasa
    if not found_valid_file:
        await message.answer("Kechirasiz hozircha hech qanday qo‘llanma yoki ma'lumot mavjud emas.")






"""       Bu foydalanuvchi tugmani bosganini aniqlaydi va holatni belgilaydigan handler         """

@router.message(lambda message: message.text == "Qo'llanma yoki Malumot qo'shish")
async def add_manual_or_info(message: Message, state: FSMContext):
    user_id = message.from_user.id
    admin_users_id = admin_users()  # Admin foydalanuvchilar ro'yxatini olish
    
    if user_id not in admin_users_id:
        # Foydalanuvchi admin emas, ularga xabar yuborib, funksiyani to'xtatish
        await message.answer("⚠️ Sizda malumot qo'shish huquqi yo'q.")
        return
    
    # Admin uchun jarayonni boshlash
    await message.answer(
        "📝 Qo'llanma yoki malumot qo'shishni davom ettirish uchun u haqida malumot kiriting.",
        reply_markup=cancel_kb,
    )
    await state.set_state(MAI.name)  # Holatni `name` ga o'rnatish




@router.message(MAI.name)
async def process_manual_name(message: Message, state: FSMContext):
    # Kiritilgan nomni olish
    manual_name = message.text

    # Vaqtincha saqlash uchun state ga qo'shish
    await state.update_data(name=manual_name)

    # Keyingi holatga o'tish
    await message.answer(
        f"📄 Ma'lumot qabul qilindi: <b>{manual_name}</b>.\n"
        "Endi faylni yuboring.",
        parse_mode="HTML",
        reply_markup=cancel_kb
    )
    await state.set_state(MAI.file)




@router.message(MAI.file)
async def process_manual_file(message: Message, state: FSMContext):
    user_id = message.from_user.id
    admin_users_id = admin_users()  # Admin foydalanuvchilar ro'yxatini olish

    # Asosiy menyuni dinamik ravishda yaratish
    main_kb = get_main_kb(user_id, admin_users_id)
    
    # Fayl ID va nomni olish
    document = message.document
    file_id = document.file_id

    # Oldingi state dan qo'llanma nomini olish
    state_data = await state.get_data()
    manual_name = state_data.get("name")

    # Ma'lumotni saqlash funksiyasini chaqirish
    save_manual(manual_name, file_id)

    # Adminni xabardor qilish
    await message.answer(
        f"✅ Qo'llanma saqlandi:\n\n"
        f"📄 {manual_name}\n"
        f"🆔 <b>Fayl ID:</b> {file_id}",
        reply_markup=main_kb,
        parse_mode="HTML",
    )

    # Holatni tozalash
    await state.clear()




# "Barcha foydalanuvchilarga xabar" tugmasi bosilganda
@router.message(lambda message: message.text == "Barcha foydalanuvchilarga xabar")
async def start_broadcast(message: Message, state: FSMContext):
    user_id = message.from_user.id
    admin_users_id = admin_users()  # Admin foydalanuvchilar ro'yxatini olish
    
    if user_id not in admin_users_id:
        # Foydalanuvchi admin emas, ularga xabar yuborib, funksiyani to'xtatish
        await message.answer("⚠️ Kechirasiz, sizda ushbu amalni bajarish huquqi yo'q.")
        return
    
    # Admin uchun jarayonni boshlash
    await message.answer(
        "📝 Barcha foydalanuvchilarga xabar yo'llash uchun malumot (fayl) kiriting.",
        reply_markup=cancel_kb,
    )
    await state.set_state(BroadcastStates.waiting_for_message)  # Holatni `name` ga o'rnatish





@router.message(BroadcastStates.waiting_for_message)
async def handle_broadcast_message(message: Message, state: FSMContext, bot: Bot):
    admin_users_id = admin_users()  # Admin foydalanuvchilar ro'yxatini olishuser_id = message.from_user.id
    user_id = message.from_user.id
    # Asosiy menyuni dinamik ravishda yaratish
    main_kb = get_main_kb(user_id, admin_users_id)
    if message.from_user.id not in admin_users_id:
        await message.answer("Kechirasiz, sizda ushbu amalni bajarish huquqi yo'q.")
        return

    success_count = 0
    fail_count = 0

    # Foydalanuvchi ro'yxati va statistikani olish
    all_users = len(all_info_users())
    active_users = [user for user in all_info_users() if user['is_active']]
    active_users_len = len(active_users)
    deactive_users = all_users - active_users_len

    # Fayl yoki matnni barcha aktiv foydalanuvchilarga yuborish
    for user in active_users:
        try:
            if message.content_type == ContentType.TEXT:
                await bot.send_message(chat_id=5998974847, text=message.text[:4096])
            elif message.content_type == ContentType.PHOTO:
                await bot.send_photo(chat_id=5998974847, photo=message.photo[-1].file_id, caption=message.caption)
            elif message.content_type == ContentType.DOCUMENT:
                await bot.send_document(chat_id=5998974847, document=message.document.file_id, caption=message.caption)
            elif message.content_type == ContentType.VIDEO:
                await bot.send_video(chat_id=5998974847, video=message.video.file_id, caption=message.caption)
            success_count += 1
        except Exception:
            fail_count += 1

    # Statistikani yuborish
    stats_message = (
        f"Xabar {success_count} ta foydalanuvchiga muvaffaqiyatli yuborildi.\n"
        f"{fail_count} ta foydalanuvchiga yuborishda xatolik yuz berdi.\n\n"
        f"👥 Umumiy foydalanuvchilar soni: {all_users}.\n"
        f"✅ Aktiv foydalanuvchilar soni: {active_users_len}.\n"
        f"⚠️ Aktiv bo'lmagan foydalanuvchilar soni: {deactive_users}."
    )
    await bot.send_message(chat_id=message.from_user.id, text=stats_message,
        reply_markup=main_kb,)

    # FSM holatini tozalash
    await state.clear()





"""       Bu admin "Qo'shish yoki o'zgartirish" tugmani bosganini aniqlaydi va holatni belgilaydigan handler         """
# "Qo'shish yoki o'zgartirish" tugmasi bosilganda
@router.message(lambda message: message.text == "Qo'shish yoki o'zgartirish")
async def start_broadcast(message: Message, state: FSMContext):
    user_id = message.from_user.id
    admin_users_id = admin_users()  # Admin foydalanuvchilar ro'yxatini olish
    
    if user_id not in admin_users_id:
        # Foydalanuvchi admin emas, ularga xabar yuborib, funksiyani to'xtatish
        await message.answer("⚠️ Kechirasiz, sizda ushbu amalni bajarish huquqi yo'q.")
        return
    
    # Admin uchun jarayonni boshlash
    await message.answer(
        "Bo'limni tanlashingiz mumkin.",
        reply_markup = add_or_update_info,
    )





"""       Bu admin "Foto qo'shish yoki o'zgartirish" tugmani bosganini aniqlaydi va holatni belgilaydigan handler         """
# "Foto qo'shish yoki o'zgartirish" tugmasi bosilganda
@router.message(lambda message: message.text == "Foto qo'shish yoki o'zgartirish")
async def start_broadcast(message: Message, state: FSMContext):
    user_id = message.from_user.id
    admin_users_id = admin_users()  # Admin foydalanuvchilar ro'yxatini olish
    
    if user_id not in admin_users_id:
        # Foydalanuvchi admin emas, ularga xabar yuborib, funksiyani to'xtatish
        await message.answer("⚠️ Kechirasiz, sizda ushbu amalni bajarish huquqi yo'q.")
        return
    
    # Admin uchun jarayonni boshlash
    keyboard = []
    buttons = ["Mahsulot", "Mahsulot turi", "Xatolik kodi", "❌ Bekor qilish"]
    for button in buttons:
        keyboard.append([KeyboardButton(text=f"{button}")])
    await message.answer(
        "🖼️ Foto qo'shish yoki o'zgartirish uchun kerakli bo'limni tanlang.",
        reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True),
    )
    await state.set_state(PhotoAddorUpdate.waiting_for_category)  # Holatni `name` ga o'rnatish



# Kategoriya tanlanganda
@router.message(lambda message: message.text in ["Mahsulot", "Mahsulot turi", "Xatolik kodi"], PhotoAddorUpdate.waiting_for_category)
async def category_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_category=message.text)

    # Mos ro‘yxatni chaqiramiz
    category_data = {
        "Mahsulot": all_products(),
        "Mahsulot turi": all_product_types(),
        "Xatolik kodi": all_errors()
    }
    
    items = category_data.get(message.text, [])
    prefix = {
        "Mahsulot": "prod_",
        "Mahsulot turi": "ty_",
        "Xatolik kodi": "err_"
    }.get(message.text, "")

    # Tugmalarni yaratish
    keyboard = generate_inline_keyboard(items, prefix)

    if keyboard:
        await message.answer("Iltimos, elementni tanlang:", reply_markup=keyboard)
        await state.set_state(PhotoAddorUpdate.waiting_for_item_selection)
    else:
        await message.answer("Hali hech qanday ma'lumot yo‘q!", reply_markup=ReplyKeyboardRemove())



# Element tanlanganda
@router.callback_query(PhotoAddorUpdate.waiting_for_item_selection)
async def item_chosen(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chosen_category = data.get("chosen_category")

    # Tugmadan tanlangan ID ni olish (xatolik bo‘lsa, javob qaytaramiz)
    try:
        chosen_item_id = callback.data.split('_')[-1]  # ID string formatda
    except (IndexError, ValueError):
        await callback.answer("❌ Noto‘g‘ri formatdagi tanlov!", show_alert=True)
        return

    # Kategoriya bo‘yicha mos elementlarni olish
    category_data = {
        "Mahsulot": all_products(),
        "Mahsulot turi": all_product_types(),
        "Xatolik kodi": all_errors(),
    }

    items = category_data.get(chosen_category, [])
    valid_items_with_name = {str(item["id"]): item["name"] for item in items}  # ID -> Name lug‘ati

    # Agar ID ro‘yxatda bo‘lmasa, xato chiqaramiz
    if chosen_item_id not in valid_items_with_name:
        await callback.answer("❌ Noto‘g‘ri tanlov! Iltimos, tugmalardan foydalaning.", show_alert=True)
        return

    chosen_item_name = valid_items_with_name[chosen_item_id]

    # To‘g‘ri tanlov bo‘lsa, saqlaymiz
    await state.update_data(chosen_item=chosen_item_id)
    await callback.message.edit_text(f"📸 Iltimos, {chosen_item_name} uchun yangi fotosuratni yuboring.")
    await state.set_state(PhotoAddorUpdate.waiting_for_photo)


# Noto‘g‘ri tanlovning oldini olish
@router.message(PhotoAddorUpdate.waiting_for_item_selection)
async def invalid_selection(message: Message, state: FSMContext):
    await message.answer("❌ Noto‘g‘ri tanlov! Iltimos, tugmalardan foydalaning.")



@router.message(PhotoAddorUpdate.waiting_for_photo)
async def process_photo(message: Message, state: FSMContext):
    # Tekshiruv: Foydalanuvchi rasm yuborganmi?
    if not message.photo:
        await message.answer("Iltimos, rasm yuboring!")
        return  # Xatolikni oldini olish uchun qaytib chiqamiz

    # Eng yuqori sifatdagi fotosurat ID-si
    photo_id = message.photo[-1].file_id  

    # Oldin saqlangan ma'lumotlarni olish
    data = await state.get_data()
    chosen_category = data.get("chosen_category")
    chosen_item_id = data.get("chosen_item")  # Oldin tanlangan mahsulot ID

    # Tanlangan kategoriya va ID tekshiruvi
    if not chosen_item_id:
        await message.answer("❌ Tanlangan mahsulot yoki kategoriya mavjud emas. Iltimos, qaytadan tanlang.")
        return

    if chosen_category == "Mahsulot":
        result = save_or_update_product(chosen_item_id, photo_id, type='photo')
    elif chosen_category == "Mahsulot turi":
        result = save_or_update_product_type(chosen_item_id, photo_id, type='photo')
    elif chosen_category == "Xatolik kodi":
        result = save_or_update_error(chosen_item_id, photo_id)
    else:
        await message.answer("❌ Tanlangan kategoriya mavjud emas.")
        return

    # Xatolikni tekshirish va javob qaytarish
    if isinstance(result, list) and len(result) > 0:
        result = result[0]  # Ro‘yxat bo‘lsa, birinchi elementni olamiz

    if isinstance(result, dict) and result.get("status") == "success":
        await message.answer("📸 Rasm muvaffaqiyatli yuklandi!", reply_markup=add_or_update_info)
    else:
        error_message = result.get("message", "Noma'lum xatolik yuz berdi.") if isinstance(result, dict) else "Noma'lum javob formati."
        await message.answer(f"⚠️ Xatolik yuz berdi: {error_message}")

    # Stateni tozalash
    await state.clear()







"""       Bu admin "Kitob qo'shish yoki o'zgartirish" tugmani bosganini aniqlaydi va holatni belgilaydigan handler         """
# "Foto qo'shish yoki o'zgartirish" tugmasi bosilganda
@router.message(lambda message: message.text == "Kitob qo'shish yoki o'zgartirish")
async def start_broadcast(message: Message, state: FSMContext):
    user_id = message.from_user.id
    admin_users_id = admin_users()  # Admin foydalanuvchilar ro'yxatini olish
    
    if user_id not in admin_users_id:
        # Foydalanuvchi admin emas, ularga xabar yuborib, funksiyani to'xtatish
        await message.answer("⚠️ Kechirasiz, sizda ushbu amalni bajarish huquqi yo'q.")
        return
    
    # Admin uchun jarayonni boshlash
    keyboard = []
    buttons = ["Mahsulot", "Mahsulot turi", "❌ Bekor qilish"]
    for button in buttons:
        keyboard.append([KeyboardButton(text=f"{button}")])
    await message.answer(
        "📖 Kitob qo'shish yoki o'zgartirish uchun kerakli bo'limni tanlang.",
        reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True),
    )
    await state.set_state(BookAddorUpdate.waiting_for_category)  # Holatni `name` ga o'rnatish



# Kategoriya tanlanganda
@router.message(lambda message: message.text in ["Mahsulot", "Mahsulot turi", "Xatolik kodi"], BookAddorUpdate.waiting_for_category)
async def category_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_category=message.text)

    # Mos ro‘yxatni chaqiramiz
    category_data = {
        "Mahsulot": all_products(),
        "Mahsulot turi": all_product_types(),
    }
    
    items = category_data.get(message.text, [])
    prefix = {
        "Mahsulot": "prod_",
        "Mahsulot turi": "ty_",
    }.get(message.text, "")

    # Tugmalarni yaratish
    keyboard = generate_inline_keyboard(items, prefix)

    if keyboard:
        await message.answer("Iltimos, elementni tanlang:", reply_markup=keyboard)
        await state.set_state(BookAddorUpdate.waiting_for_item_selection)
    else:
        await message.answer("Hali hech qanday ma'lumot yo‘q!", reply_markup=ReplyKeyboardRemove())



# Element tanlanganda
@router.callback_query(BookAddorUpdate.waiting_for_item_selection)
async def item_chosen(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chosen_category = data.get("chosen_category")

    # Tugmadan tanlangan ID ni olish (xatolik bo‘lsa, javob qaytaramiz)
    try:
        chosen_item_id = callback.data.split('_')[-1]  # ID string formatda
    except (IndexError, ValueError):
        await callback.answer("❌ Noto‘g‘ri formatdagi tanlov!", show_alert=True)
        return

    # Kategoriya bo‘yicha mos elementlarni olish
    category_data = {
        "Mahsulot": all_products(),
        "Mahsulot turi": all_product_types(),
    }

    items = category_data.get(chosen_category, [])
    valid_items_with_name = {str(item["id"]): item["name"] for item in items}  # ID -> Name lug‘ati

    # Agar ID ro‘yxatda bo‘lmasa, xato chiqaramiz
    if chosen_item_id not in valid_items_with_name:
        await callback.answer("❌ Noto‘g‘ri tanlov! Iltimos, tugmalardan foydalaning.", show_alert=True)
        return

    chosen_item_name = valid_items_with_name[chosen_item_id]

    # To‘g‘ri tanlov bo‘lsa, saqlaymiz
    await state.update_data(chosen_item=chosen_item_id)
    await callback.message.edit_text(f"📖 Iltimos, {chosen_item_name} uchun yangi kitob yuboring.")
    await state.set_state(BookAddorUpdate.waiting_for_book)


# Noto‘g‘ri tanlovning oldini olish
@router.message(BookAddorUpdate.waiting_for_item_selection)
async def invalid_selection(message: Message, state: FSMContext):
    await message.answer("❌ Noto‘g‘ri tanlov! Iltimos, tugmalardan foydalaning.")



@router.message(BookAddorUpdate.waiting_for_book)
async def process_book(message: Message, state: FSMContext):
    # Tekshiruv: Foydalanuvchi kitob yuborganmi?
    if not message.document:
        await message.answer("Iltimos, kitobni yuboring!")
        return  # Xatolikni oldini olish uchun qaytib chiqamiz

    # Kitob fayl ID-si
    book_id = message.document.file_id  

    # Oldin saqlangan ma'lumotlarni olish
    data = await state.get_data()
    chosen_category = data.get("chosen_category")
    chosen_item_id = data.get("chosen_item")  # Oldin tanlangan mahsulot ID

    # Tanlangan kategoriya va ID tekshiruvi
    if not chosen_item_id:
        await message.answer("❌ Tanlangan mahsulot yoki kategoriya mavjud emas. Iltimos, qaytadan tanlang.")
        return

    if chosen_category == "Mahsulot":
        result = save_or_update_product(chosen_item_id, book_id, type="book")
    elif chosen_category == "Mahsulot turi":
        result = save_or_update_product_type(chosen_item_id, book_id, type='book')
    else:
        await message.answer("❌ Tanlangan kategoriya mavjud emas.")
        return

    # Xatolikni tekshirish va javob qaytarish
    if isinstance(result, list) and len(result) > 0:
        result = result[0]  # Ro‘yxat bo‘lsa, birinchi elementni olamiz

    if isinstance(result, dict) and result.get("status") == "success":
        await message.answer("📖 Kitob muvaffaqiyatli yuklandi!", reply_markup=add_or_update_info)
    else:
        error_message = result.get("message", "Noma'lum xatolik yuz berdi.") if isinstance(result, dict) else "Noma'lum javob formati."
        await message.answer(f"⚠️ Xatolik yuz berdi: {error_message}")

    # Stateni tozalash
    await state.clear()









# Xabarlarni boshqaruvchi handler
@router.message()
async def handle_message(message: Message):
    # Agar foydalanuvchi matn yuborgan bo'lsa:
    if message.content_type == ContentType.TEXT:
        text_len = len(message.text)
        code = message.text.strip().upper()

        # Xatolik kodini tekshirish
        try:
            if search_error_info(code):
                error = search_error_info(code)
                await message.reply(f"❗ Kod: {error}\n")
            else:
                await message.reply(
                    "⚠️ Xato kodini izlash uchun uni tekshirib to‘g‘ri ko‘rinishda yuboring.\n\n"
                    "🔍 Masalan: E01 yoki e01"
                )
        except Exception as e:
            await message.answer(
                "⚠️ Kutilmagan xatolik yuz berdi:\n\n"
                "Iltimos, boshqa biror xabar yoki amaliyotni sinab ko'ring."
            )
    # Matndan boshqa turdagi fayllar yuborilganda:
    else:
        await message.answer(
            "⚠️ Siz faqat Xatolik kodlarini izlashingiz mumkin.\n\n 🔍 Masalan: E01 yoki e01"
        )

