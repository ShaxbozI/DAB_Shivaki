import os
import shutil
from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

import qrcode
from io import BytesIO
from django.core.files import File
import base64




class Qr_code(models.Model):
    
    def file_upload_to(instance, filename):
        extension = filename.split('.')[-1]
        new_filename = f'{instance.link_name}.{extension}'
        return f'files/{instance.link_name}/{new_filename}'
    
    
    def qr_code_file_upload_to(instance, filename):
        return instance.file_upload_to(filename)
    
    link_name = models.CharField(max_length=300)
    qr_file = models.FileField(
        upload_to=file_upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
    )
    slug = models.SlugField(unique=True, blank=True)
    qr_code_link = models.URLField(blank=True, null=True)
    qr_code = models.ImageField(upload_to=qr_code_file_upload_to, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
    
    def delete(self, *args, **kwargs):
        folder_path = f'media/files/{self.link_name}'
        try:
            shutil.rmtree(folder_path)
        except FileNotFoundError:
            pass
        super().delete(*args, **kwargs)

    def clean(self):
        # Slug generatsiya qilish va tekshirish
        if not self.slug:
            self.slug = slugify(self.link_name)
        
        if Qr_code.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            raise ValidationError({
                'link_name': 'Ushbu nom bilan bog‘liq maʼlumotlar mavjud. Iltimos, boshqa nom tanlang.',
            })
    
    def save(self, *args, **kwargs):
        # Tekshiruvni chaqirish
        self.full_clean()
        
        # QR kodni faqat yangi obyekt yaratilganda yoki link_name o'zgarganda qayta yaratish
        if not self.qr_code or 'link_name' in kwargs.get('update_fields', []):
            qr_text = f"http://localhost:8000/book/{self.slug}/"
            # QR kod yaratish       
            qr_image = qrcode.make(qr_text, box_size=15)
            
            # File nomini kiritish
            file_name = f'qrc-{self.slug}.png'
            
            # So'nggi holatini saqlash uchun yangi Image obyekti yaratish
            qr_image_pil = qr_image.get_image()
            stream = BytesIO()
            qr_image_pil.save(stream, format='PNG')
            
            qr_image_data = stream.getvalue()
            qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')
            
            # QR kodni saqlas
            self.qr_code.save(file_name, File(stream), save=False)
            stream.close()
            
            # QR kod havolasini saqlash
            self.qr_code_link = qr_text
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.link_name


 
class Bot_Users(models.Model):
    user_id = models.BigIntegerField()
    name = models.CharField(max_length=300)
    username = models.CharField(max_length=300, blank=True, null=True)
    admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Bot User"
        verbose_name_plural = "Bot Users"
        
    def __str__(self):
        return self.name
    


class Type_Protucts(models.Model):
    name = models.CharField(max_length=300)
    photo_id = models.TextField(null=True, blank=True)
    book_id = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Type Protuct"
        verbose_name_plural = "Type Protucts"
    
    def __str__(self):
        return self.name
    
    
class SubType_Protucts(models.Model):
    name = models.CharField(max_length=300)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Protuct Sub-Type"
        verbose_name_plural = "Protuct Sub-Types"
    
    def __str__(self):
        return self.name


class Products(models.Model):
    product_type = models.ForeignKey(Type_Protucts, on_delete=models.CASCADE)
    product_sub_type = models.ForeignKey(SubType_Protucts, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=300)
    photo_id = models.TextField(null=True, blank=True)
    book_id = models.TextField(null=True, blank=True)
    video_link = models.URLField(blank=True, null=True)
    producing_now = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.name
    

class Type_Errors(models.Model):
    product = models.ManyToManyField(Products)
    product_type = models.ForeignKey(Type_Protucts, on_delete=models.CASCADE)
    name = models.CharField(max_length=5)
    info = models.TextField()
    photo_id = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Type Error"
        verbose_name_plural = "Type Errors"
    
    def __str__(self):
        return self.name
    

class Manual_info(models.Model):
    name = models.TextField()
    file_id = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Manual and Info"
        verbose_name_plural = "Manuals and Info"
    
    def __str__(self):
        return self.file_id
