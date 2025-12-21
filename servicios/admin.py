from django.contrib import admin
from .models import Servicios, IngresosDiarios

admin.site.register(Servicios)
@admin.register(IngresosDiarios)
class IngresosDiariosAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'efectivo', 'tarjeta', 'transferencia', 'get_total')
    fields = ('fecha', 'efectivo', 'tarjeta', 'transferencia')  # Todos los campos visibles
    
    def get_total(self, obj):
        return f"${obj.total}"
    get_total.short_description = 'Total'
