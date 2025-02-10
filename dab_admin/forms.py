from django import forms
from .models import Qr_code

class QrCodeForm(forms.ModelForm):
    class Meta:
        model = Qr_code
        fields = '__all__'

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if Qr_code.objects.filter(slug=slug).exists():
            raise forms.ValidationError("Bu nom allaqachon mavjud, boshqa nom tanlang.")
        return slug