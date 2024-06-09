from django.contrib.auth import views as auth_views
from django.urls import path
from .views import home, register_view, dashboard, logout_view, cadastrar_iphone, estoque, editar_iphone, remover_iphone, buscar_iphones

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('cadastrar_iphone/', cadastrar_iphone, name='cadastrar_iphone'),
    path('estoque/', estoque, name='estoque'),
    path('editar_iphone/<int:pk>/', editar_iphone, name='editar_iphone'),
    path('remover_iphone/<int:pk>/', remover_iphone, name='remover_iphone'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name='password_reset_complete'),
    path('buscar_iphones/', buscar_iphones, name='buscar_iphones'),
]
