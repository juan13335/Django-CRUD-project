from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('singup/', views.singup, name='singup'),
    path('logout/', views.singout, name='logout'),
    path('singin/', views.singin, name='singin'),
    path('createform/', views.create_form, name='createform'),
    path('listarform/', views.consultar_form, name='listarform'),
    path('listarformcomp/', views.consultar_form_comp, name='listarformcomp'),
    # El parametro usando en el path se usa cuando se tiene que buscar por id/entero, puede ir cambiando
    path('listarform/<int:det_id>/', views.detalle_form, name='detalleform'),
    path('listarform/<int:det_id>/completo', views.form_completo, name='form_completo'),
    path('listarform/<int:det_id>/eliminado', views.form_eliminado, name='form_eliminado'),
]