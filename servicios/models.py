from django.db import models
from datetime import date

class Servicios(models.Model):
    fecha = models.DateField(default=date.today) 
    cliente = models.CharField(max_length=50, blank=False, null=False) 
    servicio= models.CharField(max_length=50, blank=False, null=False) 
    precio = models.DecimalField(max_digits=7, decimal_places=2)
    metodo_pago = models.CharField(max_length=50, blank=False, null=False) 
    barbero = models.CharField(max_length=50, blank=False, null=False) 
    
    def __str__(self):
        return f"Cliente: {self.cliente}\n - Servicio: {self.servicio}\n - Fecha: {self.fecha}\n - Peluquero:  {self.barbero}"

# Modelo para gestionar ingresos diarios
class IngresosDiarios(models.Model):
    fecha = models.DateField(default=date.today, unique=True)  # unique=True para evitar duplicados por día
    efectivo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tarjeta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transferencia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = "Ingreso Diario"
        verbose_name_plural = "Ingresos Diarios"
        ordering = ['-fecha']  # Ordena por fecha descendente
    
    def __str__(self):
        return f"Ingresos del {self.fecha}"
    
    @property
    def total(self):
        """Calcula el total de ingresos del día"""
        return self.efectivo + self.tarjeta + self.transferencia