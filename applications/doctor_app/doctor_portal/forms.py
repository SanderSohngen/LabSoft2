from django import forms
from .models import Consulta
from .models import Paciente

class ConsultaForm(forms.ModelForm):

    class Meta:
        model = Consulta
        fields = ('info_consulta',)

