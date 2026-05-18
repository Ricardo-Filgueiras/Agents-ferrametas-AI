from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user'

urlpatterns = [
    # Custom Register View
    path('register/', views.register, name='register'),
    
    # Native Auth Views
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Native Password Reset Views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/<uuid:pk>/', views.clientes_detail, name='clientes_detail'),
    path('clientes/create/', views.clientes_create, name='clientes_create'),
    path('clientes/update/<uuid:pk>/', views.clientes_update, name='clientes_update'),
    path('clientes/delete/<uuid:pk>/', views.clientes_delete, name='clientes_delete'),
    path('clientes/<uuid:cliente_pk>/documentos/', views.documentos_list, name='documentos_list'),
    path('clientes/<uuid:cliente_pk>/documentos/<uuid:pk>/', views.documentos_detail, name='documentos_detail'),
    path('clientes/<uuid:cliente_pk>/documentos/create/', views.documentos_create, name='documentos_create'),
    path('clientes/<uuid:cliente_pk>/documentos/update/<uuid:pk>/', views.documentos_update, name='documentos_update'),
    path('clientes/<uuid:cliente_pk>/documentos/delete/<uuid:pk>/', views.documentos_delete, name='documentos_delete'),
    
]
