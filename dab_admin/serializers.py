from rest_framework import serializers

from .models import Bot_Users, Manual_info, Type_Errors, Type_Protucts, Products



class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot_Users
        fields = ['user_id', 'name', 'username', 'is_active', 'admin']

    def update(self, instance, validated_data):
        # If the user exists and the `is_active` field is updated
        instance.name = validated_data.get('name', instance.name)
        instance.username = validated_data.get('username', instance.username)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    def create(self, validated_data):
        # Create new user if not exists
        user = Bot_Users.objects.create(**validated_data)
        return user
        

class TypeErrorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Type_Errors
        fields = '__all__'


class ManualInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Manual_info
        fields = ['name', 'file_id']
    
    def update(self, instance, validated_data):
        # If the user exists and the `is_active` field is updated
        instance.name = validated_data.get('name', instance.name)
        instance.file_id = validated_data.get('file_id', instance.file_id)
        instance.save()
        return instance

    def create(self, validated_data):
        # Create new user if not exists
        manual = Manual_info.objects.create(**validated_data)
        return manual


class TypeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_Protucts
        fields = '__all__'
        
    def to_representation(self, instance):
        # Obyektni dastlabki ko'rinishga aylantirish
        representation = super().to_representation(instance)

        # Har bir maydonni tekshirish va '-' ni qo'llash
        for field, value in representation.items():
            if value in [None, '', []]:  # Bo'sh qiymatlar uchun
                representation[field] = '-'
        return representation

  
        
class ProductSerializer(serializers.ModelSerializer):
    product_type = serializers.CharField(source='product_type.name')  # Mahsulot turi
    product_sub_type = serializers.CharField(source='product_sub_type.name', allow_null=True)  # Ichki tur
    photo_id = serializers.CharField(required=False)  # Photo talab emas
    book_id = serializers.CharField(required=False)  # File talab emas
    video_link = serializers.URLField(required=False)  # URL talab emas

    class Meta: 
        model = Products
        fields = ['id', 'name', 'photo_id', 'book_id', 'video_link', 'create_at', 'producing_now', 'product_type', 'product_sub_type']
    




class SaveorUpdateTypeProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_Protucts
        fields = ["id", "photo_id", "book_id"]

    def update(self, instance, validated_data):
        # Faqat mavjud bo‘lgan ma'lumotlarni yangilash
        for key, value in validated_data.items():
            if value is not None:  # Agar yangi qiymat `None` bo‘lmasa, yangilash
                setattr(instance, key, value)
        instance.save()
        return instance



class SaveorUpdateProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["id", "photo_id", "book_id"]

    def update(self, instance, validated_data):
        # Faqat mavjud bo‘lgan ma'lumotlarni yangilash
        for key, value in validated_data.items():
            if value is not None:  # Agar yangi qiymat `None` bo‘lmasa, yangilash
                setattr(instance, key, value)
        instance.save()
        return instance



class SaveorUpdateTypeErrorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_Errors
        fields = ["id", "photo_id",]

    def update(self, instance, validated_data):
        # Faqat mavjud bo‘lgan ma'lumotlarni yangilash
        for key, value in validated_data.items():
            if value is not None:  # Agar yangi qiymat `None` bo‘lmasa, yangilash
                setattr(instance, key, value)
        instance.save()
        return instance