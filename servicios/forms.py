# forms.py
from django.forms import ModelForm, Select
from .models import Servicios
from django.forms import DateInput 

class ServiceForm(ModelForm):
    class Meta:
        model = Servicios
        fields = '__all__'
        widgets = {
            'servicio': Select(attrs={'class': 'form-select'}, choices=[
                ('Corte', 'Corte'),
                ('Barba + Corte', 'Barba + Corte'),
                ('Barba', 'Barba'),
                ('Ceja', 'Ceja'),
                ('Contornos', 'Contornos'),
                ('Barba + Ceja', 'Barba + Ceja'),
                ('Corte + Ceja', 'Corte + Ceja'),
                ('Barba + Ceja + Corte', 'Barba + Ceja + Corte'),
            ]),
            'metodo_pago': Select(attrs={'class': 'form-select'}, choices=[
                ('Efectivo', 'Efectivo'),
                ('Tarjeta', 'Tarjeta'),
                ('Transferencia', 'Transferencia')
            ]),
            'barbero': Select(attrs={'class': 'form-select'}, choices=[
                ('Peter', 'Peter'),
                ('Frank', 'Frank'),
            ]),
            'fecha': DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ not in ['Select', 'DateInput']:
                field.widget.attrs.update({'class': 'form-control'})