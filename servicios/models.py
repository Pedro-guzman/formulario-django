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
    
