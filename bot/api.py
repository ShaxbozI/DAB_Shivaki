import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"



def users():
    # API manziliga so'rov yuborish
    url = f"{BASE_URL}/get_users/"
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Xatolik yuz bersa, istisno ko'taradi.
        
        # JSON formatidagi javobni olish
        get_data_list = response.json()

        # Natijani qayta ishlash
        data_list = [item["user_id"] for item in get_data_list]

        return data_list
    except requests.exceptions.RequestException as e:
        print(f"Xatolik yuz berdi: {e}")
        return None


def all_info_users():
    # API manziliga so'rov yuborish
    url = f"{BASE_URL}/get_users/"
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Xatolik yuz bersa, istisno ko'taradi.
        
        # JSON formatidagi javobni olish
        get_data_list = response.json()

        # Natijani qayta ishlash
        data_list = [item for item in get_data_list]

        return data_list
    except requests.exceptions.RequestException as e:
        print(f"Xatolik yuz berdi: {e}")
        return None



def manual_info():
    # API manziliga so'rov yuborish
    url = f"{BASE_URL}/manual/"
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Xatolik yuz bersa, istisno ko'taradi.
        
        # JSON formatidagi javobni olish
        get_data_list = response.json()

        # Agar API javobi to'g'ri formatda bo'lsa, data_list ni olish
        if isinstance(get_data_list, list):
            return get_data_list
        else:
            print("Xato: API javobi kutilgan formatda emas.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Xatolik yuz berdi: {e}")
        return None



def admin_users():
    # API manziliga so'rov yuborish
    url = f"{BASE_URL}/get_users/"
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Xatolik yuz bersa, istisno ko'taradi.
        
        # JSON formatidagi javobni olish
        get_data_list = response.json()

        # Faqat admin bo'lgan foydalanuvchilarni olish
        # print(get_data_list)
        admin_users = [user for user in get_data_list if user.get('admin') and user.get('is_active')]
        data_list = [item["user_id"] for item in admin_users]

        return data_list
    except requests.exceptions.RequestException as e:
        print(f"Xatolik yuz berdi: {e}")
        return None



def save_or_update_user(user_id, name, username=None, is_active=True):
    # API manziliga so'rov yuborish
    response = requests.get(f"{BASE_URL}/save_or_update_user/", params={
        'user_id': user_id,
        'name': name,
        'username': username if username else "",  # If username is None, send an empty string
        'is_active': is_active
    })

    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'error', 'message': 'Django API bilan bog‘lanishda xatolik yuz berdi.'}



def save_manual(name, file_id):
    # API manziliga so'rov yuborish
    response = requests.get(f"{BASE_URL}/save_manual/", params={
        'name': name,
        'file_id': file_id
    })

    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'error', 'message': 'Django API bilan bog‘lanishda xatolik yuz berdi.'}



def product_types():
    # API manziliga so'rov yuborish
    url = f"{BASE_URL}/type/"
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Xatolik yuz bersa, istisno ko'taradi.
        
        # JSON formatidagi javobni olish
        get_data_list = response.json()

        # Natijani qayta ishlash
        data_list = [item["name"] for item in get_data_list]

        return data_list
    except requests.exceptions.RequestException as e:
        print(f"Xatolik yuz berdi: {e}")
        return None



def all_product_types():
    # API manziliga so'rov yuborish
    url = f"{BASE_URL}/type/"
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Xatolik yuz bersa, istisno ko'taradi.
        
        # JSON formatidagi javobni olish
        get_data_list = response.json()

        # ID va nomlarni lug‘at shaklida qaytarish
        data_list = [{"id": item["id"], "name": item["name"]} for item in get_data_list]

        return data_list
    except requests.exceptions.RequestException as e:
        print(f"Xatolik yuz berdi: {e}")
        return None



def all_products():
    # API manziliga so'rov yuborish
    url = f"{BASE_URL}/product/"
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Xatolik yuz bersa, istisno ko'taradi.
        
        # JSON formatidagi javobni olish
        get_data_list = response.json()

        # ID va nomlarni lug‘at shaklida qaytarish
        data_list = [{"id": item["id"], "name": item["name"]} for item in get_data_list]

        return data_list
    except requests.exceptions.RequestException as e:
        print(f"Xatolik yuz berdi: {e}")
        return None



def all_errors():
    # API manziliga so'rov yuborish
    url = f"{BASE_URL}/error/"
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Xatolik yuz bersa, istisno ko'taradi.
        
        # JSON formatidagi javobni olish
        get_data_list = response.json()

        # ID va nomlarni lug‘at shaklida qaytarish
        data_list = [{"id": item["id"], "name": item["name"]} for item in get_data_list]

        return data_list
    except requests.exceptions.RequestException as e:
        print(f"Xatolik yuz berdi: {e}")
        return None
    


def products():
    # API manziliga so'rov yuborish
    url = f"{BASE_URL}/product/"
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Xatolik yuz bersa, istisno ko'taradi.
        
        # JSON formatidagi javobni olish
        get_data_list = response.json()  # To'liq ma'lumotlarni qaytaradi
        return get_data_list  # To'liq mahsulot ma'lumotlarini qaytarish
    except requests.exceptions.RequestException as e:
        print(f"Xatolik yuz berdi: {e}")
        return []



def product_info(name):
    # API manziliga so'rov yuborish
    url = f"{BASE_URL}/product/"
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Xatolik yuz bersa, istisno ko'taradi.

        # JSON formatidagi javobni olish
        get_data_list = response.json()

        # Mahsulotni nomiga qarab qidirish
        product = next((item for item in get_data_list if item['name'].lower() == name.lower()), None)
        
        return product
    except requests.exceptions.RequestException as e:
        print(f"Xatolik yuz berdi: {e}")
        return None
    
    

def error_info(id):
    url = f"{BASE_URL}/error/"
    # print(f"xatolik id: {id}")
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Xatolik yuz bersa, istisno ko'taradi.

        # JSON formatidagi javobni olish
        get_data_list = response.json()
        
        # Bir xil id ostidagi barcha xatolikni qidirish
        error = next((item for item in get_data_list if item['id'] == int(id)), None)

        # Agar xatolik mavjud bo'lsa, ularni qaytarish
        if error:
            return error
        else:
            return None  # Agar mos xatolik topilmasa

    except requests.exceptions.RequestException as e:
        print(f"Xatolik yuz berdi: {e}")
        return None



def search_error_info(name):
    url = f"{BASE_URL}/error/"
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Xatolik yuz bersa, istisno ko'taradi.

        # JSON formatidagi javobni olish
        get_data_list = response.json()

        # Bir xil nom ostidagi barcha xatoliklarni qidirish
        errors = [item for item in get_data_list if item['name'].lower() == name.lower()]

        # Agar xatoliklar mavjud bo'lsa, ularni qaytarish
        if errors:
            return errors
        else:
            return None  # Agar mos xatoliklar topilmasa

    except requests.exceptions.RequestException as e:
        print(f"Xatolik yuz berdi: {e}")
        return None



def product_errors(name):
    url = f"{BASE_URL}/product_errors/?name={name}"
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Xatolik yuz bersa, istisno ko'taradi.

        # JSON formatidagi javobni olish
        get_data_list = response.json()

        return get_data_list  # to'liq ro'yxatni qaytarish

    except requests.exceptions.RequestException as e:
        print(f"Xatolik yuz berdi: {e}")
        return None



def type_errors(name):
    url = f"{BASE_URL}/type_errors/?name={name.lower()}"
    # print(f"xatolik turi api: {name}")
    try:
        response = requests.get(url=url)
        response.raise_for_status()  # Xatolik yuz bersa, istisno ko'taradi.

        # JSON formatidagi javobni olish
        get_data_list = response.json()

        return get_data_list  # to'liq ro'yxatni qaytarish

    except requests.exceptions.RequestException as e:
        print(f"Xatolik yuz berdi: {e}")
        return None



def save_or_update_product_type(id, item_id, type):
    # API manziliga so'rov yuborish
    response = requests.post(
        f"{BASE_URL}/save_or_update_product_type/",
        json={
            'id': id,
            'photo_id': item_id if type == 'photo' else None,
            'book_id': item_id if type == 'book' else None,
        },
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'error', 'message': 'Django API bilan bog‘lanishda xatolik yuz berdi.'}



def save_or_update_product(id, item_id, type):
    # API manziliga so'rov yuborish
    response = requests.post(
        f"{BASE_URL}/save_or_update_product/",
        json={
            'id': id,
            'photo_id': item_id if type == 'photo' else None,
            'book_id': item_id if type == 'book' else None,
        },
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'error', 'message': 'Django API bilan bog‘lanishda xatolik yuz berdi.'}



def save_or_update_error(id, photo_id):
    # API manziliga so'rov yuborish
    response = requests.post(
        f"{BASE_URL}/save_or_update_error/",
        json={
            'id': id,
            'photo_id': photo_id,
        },
        headers={'Content-Type': 'application/json'}
    )

    # print("API Response:", response.text)
    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'error', 'message': 'Django API bilan bog‘lanishda xatolik yuz berdi.'}