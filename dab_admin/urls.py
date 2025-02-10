from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductErrors, 
    TypeProductsApiView, 
    TypeErrorsApiView, 
    ProductsApiView, 
    SaveOrUpdateUser, 
    GetUserApiView, 
    TypeErrors,
    ManualInfoApiView,
    SaveOrUpdateManual,
    SaveOrUpdateError,
    SaveOrUpdateProduct,
    SaveOrUpdateProductType,
    )
 
 
router = DefaultRouter()
 
 

urlpatterns = [
    path('type/', TypeProductsApiView.as_view()),
    path('error/', TypeErrorsApiView.as_view()),
    path('product/', ProductsApiView.as_view()),
    path('save_or_update_user/', SaveOrUpdateUser.as_view(), name='save_or_update_user'),
    path('get_users/', GetUserApiView.as_view(), name='get_users'),
    path('product_errors/', ProductErrors.as_view(), name='product_errors'),
    path('type_errors/', TypeErrors.as_view(), name='type_errors'),
    path('manual/', ManualInfoApiView.as_view(), name='manual_info'),
    path('save_manual/', SaveOrUpdateManual.as_view(), name='manual_info'),
    
    path('save_or_update_product_type/', SaveOrUpdateProductType.as_view(), name='save_or_update_product_type'),
    path('save_or_update_product/', SaveOrUpdateProduct.as_view(), name='save_or_update_product'),
    path('save_or_update_error/', SaveOrUpdateError.as_view(), name='save_or_update_error'),
]