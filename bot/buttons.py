# Create your keyboards here.
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.markdown import hbold
from api import product_types, products, product_info, type_errors




def back_button(page, name):
    return InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"paginator_{page}_{name}")




def get_main_kb(user_id, admin_users_id):
    # Oddiy tugmalar
    keyboard = [
        [KeyboardButton(text="Mahsulotlar")],
        [KeyboardButton(text="Xatolik kodlari")],
        [KeyboardButton(text="Qo'llanma va Malumotlar")],
        [KeyboardButton(text="Savol yoki Takliflar")],
    ]
    
    # Agar foydalanuvchi admin bo'lsa, "Malumot qo'shish" tugmasini qo'shamiz
    if user_id in admin_users_id:
        keyboard.append([KeyboardButton(text="Qo'shish yoki o'zgartirish")])
        keyboard.append([KeyboardButton(text="Barcha foydalanuvchilarga xabar")])

    # Klaviatura yaratish
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Kerakli tugmani tanlang!",
    )



add_or_update_info = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Foto qo'shish yoki o'zgartirish"),
        ],
        [
            KeyboardButton(text="Kitob qo'shish yoki o'zgartirish"),
        ],
        [
            KeyboardButton(text="Qo'llanma yoki Malumot qo'shish"),
        ],
        [
            KeyboardButton(text="🏠 Asosiyga qaytish"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Qo'shish yoki o'zgartitish uchun kerakli bo'limni tanlang!",
    selective=True
)



cancel_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌ Bekor qilish"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Jarayonni bekor qilishingiz mumkin!",
    selective=True
)




product_types_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        *[[InlineKeyboardButton(text=f"{name}", callback_data=f"paginator_2_{name}")] for name in product_types()],
        [InlineKeyboardButton(text="🗃️ Ishlab chiqarish to'xtatilgan mahsulatlar", callback_data="paginator_30_noproduc")],
        [InlineKeyboardButton(text="🏠 Asosiyga qaytish", callback_data="asosiy_sahifa")],
    ],
    resize_keyboard=True,
)




error_types_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        *[[InlineKeyboardButton(text=f"{name}", callback_data=f"paginator_21_{name}")] for name in product_types()],
        [InlineKeyboardButton(text="🏠 Asosiyga qaytish", callback_data="asosiy_sahifa")],
    ],
    resize_keyboard=True,
)




def paginator(page, item=None):
    asosiy = InlineKeyboardButton(text="🏠 Asosiyga qaytish", callback_data="asosiy_sahifa")
    title = "Bo'lim tanlang"  # Default title

    if page == 1:
        arxiv = InlineKeyboardButton(text="🗃️ Ishlab chiqarish to'xtatilgan mahsulatlar", callback_data=f"paginator_30_noproduc")
        title = "Mahsulot turlari"
        product_types_kb = [
            [InlineKeyboardButton(text=f"{name}", callback_data=f"paginator_2_{name}")]
            for name in product_types()
        ]
        product_types_kb.append([arxiv])
        product_types_kb.append([asosiy])
        return {"title": title, "keyboard": InlineKeyboardMarkup(inline_keyboard=product_types_kb)}

    elif page == 2 and item:
        back_btn = back_button(page - 1, item)
        produkt_type = item.lower()
        all_products = products()
        
        # Ichki turlarni aniqlash
        sub_types = list(set([
            product['product_sub_type'] for product in all_products
            if product.get('product_type', '').lower() == produkt_type and product['producing_now'] and product['product_sub_type']
        ]))
        
        # Tugmalarni yaratish
        if sub_types:  # Agar ichki turlar mavjud bo'lsa
            title = "Mahsulot ichki turlari"
            products_kb = [
                [InlineKeyboardButton(text=f"{sub_type}", callback_data=f"paginator_4_{sub_type}")]
                for sub_type in sub_types
            ]
            # Orqaga tugmasi qo'shiladi
            if back_btn:
                products_kb.append([back_btn])
            products_kb.append([asosiy])
            
            return {"title": title, "keyboard": InlineKeyboardMarkup(inline_keyboard=products_kb)}
        else:  # Agar ichki turlar mavjud bo'lmasa
            title = "Mahsulotlar"
            filtered_products = [
                product for product in all_products
                if product.get('product_type', '').lower() == produkt_type and product['producing_now'] and not product['product_sub_type']
            ]
            products_kb = [
                [InlineKeyboardButton(text=f"{product['name']}", callback_data=f"paginator_3_{product['name']}")]
                for product in filtered_products
            ]
            # Orqaga tugmasi qo'shiladi
            if back_btn:
                products_kb.append([back_btn])
            products_kb.append([asosiy])
            
            return {"title": title, "keyboard": InlineKeyboardMarkup(inline_keyboard=products_kb)}

    elif page == 3 and item:
    # Sahifa 3 uchun kontent
        product_name = item.lower()
        product_data = product_info(product_name)
        title = "Mahsulot haqida"
        if not product_data:
            return InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f'paginator_2_{item}')],
            ])
        
        buttons = []
        # "Texnik ma'lumot" va "Videomalumotni ko'ring" tugmalari bir qatorda
        row1 = []

        # Video tugmasi (faqat video_link mavjud bo‘lsa)
        video_link = product_data.get('video_link')
        if video_link:
            row1.append(InlineKeyboardButton(text="📺 Video ma'lumot", url=video_link))
        if row1:
            buttons.append(row1)
        # Xatolik kodlari tugmasi
        buttons.append([InlineKeyboardButton(text="⚙️ Mahsulotning Xatolik kodlari", callback_data=f'errors_{product_name}')])

        # Orqaga qaytish tugmasi
        buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"paginator_2_{product_data['product_type']}")])
        buttons.append([asosiy])
        
        return {"title": title, "keyboard": InlineKeyboardMarkup(inline_keyboard=buttons)}
    
    elif page == 4 and item:
        # Sahifa 4 uchun kontent
        all_products = products()
        product_type = ''
        title = f"{item.title()} Mahsulotlari"
        if not product_type:
            for product in all_products:
                if product['product_sub_type'] == item:
                    product_type = product['product_type']
        # print(f"bu mahsulot turi: {product_type}")
        back_btn = back_button(page - 2, product_type)
        
        filtered_products = [
                product for product in all_products
                if product['producing_now'] and product['product_sub_type'] == item
            ]
        products_kb = [
            [InlineKeyboardButton(text=f"{product['name']}", callback_data=f"paginator_3_{product['name']}")]
            for product in filtered_products
        ]
        
        products_kb.append([back_btn])
        products_kb.append([asosiy])
        
        return {"title": title, "keyboard": InlineKeyboardMarkup(inline_keyboard=products_kb)}
    
    
    
    # Xatolik tugmalari uchun
    elif page == 20:
        title = f"Tur bo'yicha yuzaga kelishi mumkin bo'lgan xatoliklarni ko'rishingiz mumkin bunig uchun turni tanlang"
        product_types_kb = [
            [InlineKeyboardButton(text=f"{name}", callback_data=f"paginator_21_{name}")]
            for name in product_types()
        ]
        product_types_kb.append([asosiy])
        return {"title": title, "keyboard": InlineKeyboardMarkup(inline_keyboard=product_types_kb)}
    
    elif page == 21 and item:
        title = f"{hbold(item.title())} - ushbu mahsulot turida yuzaga kelishi mumkin bo'lgan xatoliklar"

        back_btn = back_button(page-1, item)
        # print(f"bu mahsulot turi: {item}")
        errors_with_type = type_errors(item)
        # Xatolik kodlari tugmalarini yaratish
        error_buttons = [
            InlineKeyboardButton(text=f"{error_item['name']}", callback_data=f'error_{error_item["id"]}')
            for error_item in errors_with_type
        ]
        
        # Xatolik kodlarini 5 tadan bo'lib chiqarish
        error_rows = [error_buttons[i:i+5] for i in range(0, len(error_buttons), 5)]
        
        # InlineKeyboardMarkup uchun tugmalarni to'g'ri formatda tayyorlash
        product_types_kb = []
        for row in error_rows:
            product_types_kb.append(row)  # error_rows tugmalarini qo'shish

        # Back va asosiy tugmalarini qo'shish
        product_types_kb.append([back_btn])  # back_btn tugmasini qo'shish
        product_types_kb.append([asosiy])  # asosiy tugmasini qo'shish

        return {"title": title, "keyboard": InlineKeyboardMarkup(inline_keyboard=product_types_kb)}
    
    
    
    # Arxivdagi mahsulotlar
    elif page == 30:
        title = f"Ishlab chiqarish to'xtatilgan Mahsulot uchun turni tanlang"
        back_btn = back_button(page=1, name=item)
        product_types_kb = [
            [InlineKeyboardButton(text=f"{name}", callback_data=f"paginator_31_{name}")]
            for name in product_types()
        ]
        product_types_kb.append([back_btn])
        product_types_kb.append([asosiy])
        return {"title": title, "keyboard": InlineKeyboardMarkup(inline_keyboard=product_types_kb)}
    
    elif page == 31 and item:
        back_btn = back_button(page - 1, item)
        produkt_type = item.lower()
        all_products = products()
        
        # Ichki turlarni aniqlash
        sub_types = list(set([
            product['product_sub_type'] for product in all_products
            if product.get('product_type', '').lower() == produkt_type and product['product_sub_type'] and not product['producing_now']
        ]))
        
        # Tugmalarni yaratish
        if sub_types:  # Agar ichki turlar mavjud bo'lsa
            # print(f"ichki tur {sub_types}")
            title = f"Mahsulot ichki turlari"
            products_kb = [
                [InlineKeyboardButton(text=f"{sub_type}", callback_data=f"paginator_33_{sub_type}")]
                for sub_type in sub_types
            ]
            # Orqaga tugmasi qo'shiladi
            if back_btn:
                products_kb.append([back_btn])
            products_kb.append([asosiy])
            
            return {"title": title, "keyboard": InlineKeyboardMarkup(inline_keyboard=products_kb)}
        else:  # Agar ichki turlar mavjud bo'lmasa
            title = f"Mahsulotlar"
            filtered_products = [
                product for product in all_products
                if product.get('product_type', '').lower() == produkt_type and not product['producing_now'] and not product['product_sub_type']
            ]
            products_kb = [
                [InlineKeyboardButton(text=f"{product['name']}", callback_data=f"paginator_32_{product['name']}")]
                for product in filtered_products
            ]
            # Orqaga tugmasi qo'shiladi
            if back_btn:
                products_kb.append([back_btn])
            products_kb.append([asosiy])
            
            return {"title": title, "keyboard": InlineKeyboardMarkup(inline_keyboard=products_kb)}

    elif page == 32 and item:
    # Sahifa 3 uchun kontent
        product_name = item.lower()
        product_data = product_info(product_name)
        title = "Mahsulot haqida"
        if not product_data:
            return InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f'paginator_31_{item}')],
            ])
        
        buttons = []
        # "Texnik ma'lumot" va "Videomalumotni ko'ring" tugmalari bir qatorda
        row1 = []

        # Video tugmasi (faqat video_link mavjud bo‘lsa)
        video_link = product_data.get('video_link')
        if video_link:
            row1.append(InlineKeyboardButton(text="📺 Video ma'lumot", url=video_link))
        if row1:
            buttons.append(row1)
        # Xatolik kodlari tugmasi
        buttons.append([InlineKeyboardButton(text="⚙️ Mahsulotning Xatolik kodlari", callback_data=f'errors_{product_name}')])

        # Orqaga qaytish tugmasi
        buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"paginator_31_{product_data['product_type']}")])
        buttons.append([asosiy])
        
        return {"title": title, "keyboard": InlineKeyboardMarkup(inline_keyboard=buttons)}
    
    elif page == 33 and item:
        # Sahifa 4 uchun kontent
        all_products = products()
        product_type = ''
        title = f"{item.title()} Mahsulotlari"
        if not product_type:
            for product in all_products:
                if product['product_sub_type'] == item:
                    product_type = product['product_type']
        # print(f"bu mahsulot turi: {product_type}")
        back_btn = back_button(page - 2, product_type)
        
        filtered_products = [
                product for product in all_products
                if product['producing_now'] and product['product_sub_type'] == item
            ]
        products_kb = [
            [InlineKeyboardButton(text=f"{product['name']}", callback_data=f"paginator_32_{product['name']}")]
            for product in filtered_products
        ]
        
        products_kb.append([back_btn])
        products_kb.append([asosiy])
        
        return {"title": title, "keyboard": InlineKeyboardMarkup(inline_keyboard=products_kb)}

    


    return {"title": title, "keyboard": InlineKeyboardMarkup(inline_keyboard=[[asosiy]])}






def generate_inline_keyboard(items, prefix):
    """
    Inline tugmalarni dinamik yaratish uchun funksiya.
    
    :param items: ID va nomdan iborat ro'yxat ( [{"id": 1, "name": "Shampun"}, ...] )
    :param prefix: Tugmalar uchun callback_data prefixi (masalan, 'prod_' yoki 'type_')
    :return: InlineKeyboardMarkup yoki None (bo'sh bo'lsa)
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    for item in items:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=item["name"], callback_data=f"{prefix}{item['id']}")
        ])
    
    # Agar tugmalar bo'sh bo'lsa, None qaytarish
    return keyboard if keyboard.inline_keyboard else None

