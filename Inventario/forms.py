from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario,Producto,Categoria # Asegúrate de que esto apunta a tu modelo correcto
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'disponible', 'imagen', 'categoria']
        
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is None:
            return 0
        return stock
    
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if not imagen:
            raise forms.ValidationError("La imagen es obligatoria.")
        return imagen
        

#Formulario para agregar usuarios 
class CustomUserCreationForm(UserCreationForm):
    usuario = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Usuario'})
    )
    nombre = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre completo'})
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'})
    )

    class Meta:
        model = Usuario
        fields = ('usuario', 'nombre', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('usuario')
        if usuario and Usuario.objects.filter(usuario=usuario).exists():
            self.add_error('usuario', 'Este nombre de usuario ya está en uso')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.usuario = self.cleaned_data['usuario']
        user.nombre = self.cleaned_data['nombre']
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True  # Asegurarnos que el usuario está activo
        if commit:
            user.save()
        return user

#Formulario para agregar las categorias
class CategoriaForm(forms.ModelForm):
    
    class Meta:
        model = Categoria
        fields = ['nombre']  # Solo incluye el campo nombre



