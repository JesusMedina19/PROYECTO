from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario,Producto,Categoria # Asegúrate de que esto apunta a tu modelo correcto
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'disponible', 'imagen', 'categoria']
    
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if not imagen:
            raise forms.ValidationError("La imagen es obligatoria.")
        return imagen
        

#Formulario para agregar usuarios 
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('usuario', 'nombre', 'password1', 'password2')  # Asegúrate de que estos coincidan con tu modelo

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

#Formulario para agregar las categorias
class CategoriaForm(forms.ModelForm):
    
    class Meta:
        model = Categoria
        fields = ['nombre']  # Solo incluye el campo nombre
        
        

