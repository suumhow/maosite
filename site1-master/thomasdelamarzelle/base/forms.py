from django.forms import ModelForm
from .models import Student, Product

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'