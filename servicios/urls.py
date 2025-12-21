from django.urls import path
from . import views

urlpatterns = [
   path("", views.index, name="servicios"),
   path("view/<int:id>", views.view, name="servicio_view"),
   path("edit/<int:id>", views.edit, name="servicio_edit"),
   path("create/", views.create, name="servicio_create"),
   path("delete/<int:id>", views.delete, name="servicio_delete"),
   path('dashboard/', views.dashboard, name='servicio_dashboard'),
   
   # Rutas para ingresos diarios
   path('ingresos/registrar/', views.registrar_ingresos, name='registrar_ingresos'),
   path('ingresos/lista/', views.lista_ingresos, name='lista_ingresos'),
   path('ingresos/editar/<int:id>', views.editar_ingreso, name='editar_ingreso'),
   path('ingresos/eliminar/<int:id>', views.eliminar_ingreso, name='eliminar_ingreso'),
   
   path('<letter>', views.index, name='servicios')
]