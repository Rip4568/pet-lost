from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.utils.translation import gettext_lazy as _

from announcement.models import Announcement, Comment
from pet.models import Pet, Picture
from users.models import User


class AuthenticationForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('password',)


class UserCreationForm(BaseUserCreationForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('email', 'first_name')
        field_classes = {'email': forms.EmailField}

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise forms.ValidationError(
                'Este campo é obrigatório'
            )
        if not isinstance(first_name, str):
            raise forms.ValidationError(
                'Nome inválido'
            )
        if not first_name.replace(' ', '').isalpha():
            raise forms.ValidationError(
                'Não são aceitos caracteres especiais'
            )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PersonalDataForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'org_name',
            'description',
        )


class AddressDataForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].required = True
        self.fields['number'].required = True
        self.fields['district'].required = True
        self.fields['city'].required = True
        self.fields['city'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = (
            'address',
            'number',
            'complement',
            'district',
            'postal_code',
            'city',
        )


class ContactDataForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'phone_number',
            'mobile_phone_number',
            'share_phone',
            'share_email',
        )


class SocialDataForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'url_facebook_profile',
            'url_facebook_page',
            'url_twitter',
            'url_instagram',
        )


class AnnouncementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['pet'].queryset = Pet.objects.filter(user=self.user)
        self.fields['pet'].label_from_instance = lambda pet: '{name}'.format(name=pet.name)
        self.fields['pet'].help_text = 'Selecione o Pet ao que este anúncio se refere'
        self.fields['active'].help_text = 'Ative este anúncio para divulgá-lo no site'
        self.fields['situation'].help_text = 'Se o pet for seu e está desaparecido, selecione "desaparecido". ' \
                                             'Caso tenha encontrado um pet perdido na rua, selecione "encontrado"'
        self.fields['description'].help_text = 'Dê informações detalhadas sobre o ocorrido que ' \
                                               'ajudem outras pessoas à identificar seu pet.'
        self.fields['last_seen_district'].help_text = 'Digite o nome do bairro em que ele foi visto por último'
        self.fields['last_seen_city'].help_text = 'Selecione a cidade em que ele foi visto por último'
        self.fields['lost_date'].help_text = 'Preencha apenas se a situação for "desaparecido"'
        self.fields['found_date'].help_text = 'Preencha apenas se a situação for "encontrado"'

    class Meta:
        model = Announcement
        fields = (
            'pet',
            'active',
            'situation',
            'description',
            # 'rescued',
            # 'rescued_date',
            'last_seen_district',
            'last_seen_city',
            'lost_date',
            'found_date',
        )


class PetChangeForm(forms.ModelForm):

    class Meta:
        model = Pet
        fields = (
            'name',
            'sex',
            'breed',
            'description',
        )


class PictureChangeForm(forms.ModelForm):

    class Meta:
        model = Picture
        fields = ('image',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('description',)
