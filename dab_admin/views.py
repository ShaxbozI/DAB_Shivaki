from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import SaveorUpdateProductsSerializer, SaveorUpdateTypeErrorsSerializer, SaveorUpdateTypeProductsSerializer, TypeProductSerializer, TypeErrorSerializer, BotUserSerializer, ProductSerializer, ManualInfoSerializer
from .models import Type_Protucts, Type_Errors, Bot_Users, Products, Manual_info





class ManualInfoApiView(generics.ListAPIView):
    serializer_class = ManualInfoSerializer
    permission_classes = [AllowAny, ]
    
    def get_queryset(self):
        queryset = Manual_info.objects.all()
        return queryset


class SaveOrUpdateManual(APIView):
    def get(self, request):
        # Query parametersdan ma'lumotlarni olish
        name = request.GET.get('name')
        file_id = request.GET.get('file_id')

        if not name or not file_id:
            return Response(
                {"error": "Both 'name' and 'file_id' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Modelda mavjudligini tekshirish
        manual = Manual_info.objects.filter(file_id=file_id).first()

        if manual:
            # Agar mavjud bo'lsa, yangilash
            serializer = ManualInfoSerializer(manual, data={'name': name}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"status": "success", "message": "Manual updated successfully."},
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Agar mavjud bo'lmasa, yangi qo'shish
            serializer = ManualInfoSerializer(data={'name': name, 'file_id': file_id})
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"status": "success", "message": "Manual created successfully."},
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserApiView(generics.ListAPIView):
    serializer_class = BotUserSerializer
    permission_classes = [AllowAny, ]
    
    def get_queryset(self):
        queryset = Bot_Users.objects.all()
        return queryset


class SaveOrUpdateUser(APIView):
    def get(self, request):
        # Get user data from the query parameters
        user_id = request.GET.get('user_id')
        name = request.GET.get('name')
        username = request.GET.get('username', None)  # username is optional
        is_active = request.GET.get('is_active', True)

        if not user_id or not name:
            return Response({"error": "User ID and Name are required!"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user already exists
        user = Bot_Users.objects.filter(user_id=user_id).first()
        
        if user:
            # Update user if exists
            serializer = BotUserSerializer(user, data={'name': name, 'username': username, 'is_active': is_active}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "User updated successfully."})
            return Response({"error": "Failed to update user"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Create new user if doesn't exist
            serializer = BotUserSerializer(data={'user_id': user_id, 'name': name, 'username': username, 'is_active': is_active})
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "User created successfully."})
            return Response({"error": "Failed to create user"}, status=status.HTTP_400_BAD_REQUEST)


class TypeProductsApiView(generics.ListAPIView):
    serializer_class = TypeProductSerializer
    permission_classes = [AllowAny, ]
    
    def get_queryset(self):
        queryset = Type_Protucts.objects.all()
        return queryset


class TypeErrorsApiView(generics.ListAPIView):
    serializer_class = TypeErrorSerializer
    permission_classes = [AllowAny, ]
    
    def get_queryset(self):
        queryset = Type_Errors.objects.all()
        return queryset


class ProductsApiView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Products.objects.all()



class ProductErrors(APIView):
    def get(self, request):
        name = request.GET.get('name')

        if not name:
            return Response({"error": "Mahsulot nomi kiritilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        # Mahsulotni qidirish (nom bo‘yicha)
        product = Products.objects.filter(name__iexact=name).first()

        if not product:
            return Response({"error": "Mahsulot topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        # Mahsulot bilan bog'liq barcha xatoliklarni olish
        errors = Type_Errors.objects.filter(product=product).values('id', 'name', 'info', 'photo_id')

        # Agar xatoliklar topilmasa
        if not errors:
            return Response({"message": "Ushbu mahsulot uchun xatolik kodlari topilmadi."}, status=status.HTTP_200_OK)

        return Response(list(errors), status=status.HTTP_200_OK)



class TypeErrors(APIView):
    def get(self, request):
        name = request.GET.get('name') 

        if not name:
            return Response({"error": "Mahsulot turi kiritilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        # Mahsulotni qidirish (nom bo‘yicha)
        type_product = Type_Protucts.objects.filter(name__iexact=name).first()

        if not type_product:
            return Response({"error": "Mahsulot turi topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        # Mahsulot bilan bog'liq barcha xatoliklarni olish
        errors = Type_Errors.objects.filter(product_type=type_product).values('id', 'name', 'info', 'photo_id')

        # Agar xatoliklar topilmasa
        if not errors:
            return Response({"message": "Ushbu mahsulot turi uchun xatoliklar topilmadi."}, status=status.HTTP_200_OK)

        return Response(list(errors), status=status.HTTP_200_OK)








class SaveOrUpdateProduct(APIView):
    def post(self, request):
        product_id = request.data.get('id')  
        photo_id = request.data.get('photo_id')
        book_id = request.data.get('book_id')

        if not product_id:
            return Response({"error": "Product ID is required!"}, status=status.HTTP_400_BAD_REQUEST)

        # Mahsulotni tekshirish
        product = Products.objects.filter(id=product_id).first()

        if product:
            # Mahsulot mavjud bo‘lsa, yangilash
            serializer = SaveorUpdateProductsSerializer(product, data={'photo_id': photo_id, 'book_id': book_id}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "Product updated successfully."})
            return Response({"error": "Failed to update product"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Mahsulot mavjud bo‘lmasa, yangisini yaratish
            serializer = SaveorUpdateProductsSerializer(data={'id': product_id, 'photo_id': photo_id, 'book_id': book_id})
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "Product created successfully."})
            return Response({"error": "Failed to create product"}, status=status.HTTP_400_BAD_REQUEST)


class SaveOrUpdateProductType(APIView):
    def post(self, request):
        product_type_id = request.data.get('id')
        photo_id = request.data.get('photo_id')
        book_id = request.data.get('book_id')

        if not product_type_id:
            return Response({"error": "Product Type ID is required!"}, status=status.HTTP_400_BAD_REQUEST)

        product_type = Type_Protucts.objects.filter(id=product_type_id).first()

        if product_type:
            serializer = SaveorUpdateTypeProductsSerializer(product_type, data={'photo_id': photo_id, 'book_id': book_id}, partial=True)
        else:
            serializer = SaveorUpdateTypeProductsSerializer(data={'id': product_type_id, 'photo_id': photo_id, 'book_id': book_id})

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "Product Type updated successfully." if product_type else "Product Type created successfully."})
        return Response({"error": "Failed to process request"}, status=status.HTTP_400_BAD_REQUEST)


class SaveOrUpdateError(APIView):
    def post(self, request):
        error_id = request.data.get('id')
        photo_id = request.data.get('photo_id')

        # print(photo_id)
        
        if not error_id:
            return Response({"error": "Error ID is required!"}, status=status.HTTP_400_BAD_REQUEST)

        error = Type_Errors.objects.filter(id=error_id).first()

        if error:
            serializer = SaveorUpdateTypeErrorsSerializer(error, data={'photo_id': photo_id}, partial=True)
        else:
            serializer = SaveorUpdateTypeErrorsSerializer(data={'id': error_id, 'photo_id': photo_id})

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "Error updated successfully." if error else "Error created successfully."})
        return Response({"error": "Failed to process request"}, status=status.HTTP_400_BAD_REQUEST)







