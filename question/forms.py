from question.models import Question, User, Answer, Tag
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from PIL import Image
from io import BytesIO
from uuid import uuid4

from base64 import b64decode as b64d


class SignupForm(UserCreationForm):
    # class Meta:
    #     model = User
    #     fields = ['username', 'first_name', 'last_name', 'email', 'password']

    password = forms.CharField(max_length=128, label=u'Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=128, label=u'Подтверждение', widget=forms.PasswordInput)

    def clean(self):
        super(SignupForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('password2')
        if password != confirm:
            raise forms.ValidationError({'password2': 'Passwords don\'t match.'})
        return self.cleaned_data

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', )


# class LoginForm(AuthenticationForm):
#     pass
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password']

class ProfileEditForm(ModelForm):

    new_password = forms.PasswordInput()
    new_password_repeat = forms.PasswordInput()

    def clean_new_password(self):
        # NO
        if self.data['new_password']:
            validate_password(self.data['new_password'])
            if self.data['new_password'] != self.data['new_password_repeat']:
                raise forms.ValidationError(
                    {'new_password': 'New password doesn\'t match with its '
                                     'confirmation'})
            if check_password(self.data['password'], self.instance.password):
                raise forms.ValidationError({'old_password': 'Wrong password'})
        return self.data['new_password']

    def clean(self):
        super().clean()

        # not calling super.clean() because not all fields need validation
        # furthermore for some fields validation means nothing
        # they just live their life the way the choose to

        errors = {}
        if self.data['new_password']:
            try:
                validate_password(self.data['new_password'])
            except forms.ValidationError as e:
                errors['new_password'] = [e.error_list]

        if errors:
            raise forms.ValidationError(errors)

        return self.cleaned_data

    def save(self, **kwargs):
        super().save(**kwargs)
        if 'upload' in self.files:
            try:
                upload = Image.open(self.files['upload'])
            except IOError:
                pass
            else:
                io = BytesIO()
                upload.thumbnail((256, 256), Image.ANTIALIAS)
                upload.save(io, format='JPEG', quality=100)
                self.instance.upload.save(f'{uuid4()}.jpg', io)
        return self.instance

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class MultiTagField(forms.Field):
    def to_python(self, value):
        if not value:
            return []
        return [x.strip() for x in value.split(',') if x.strip()]

    def validate(self, value):
        super().validate(value)
        if not 1 <= len(value) <= 12:
            raise forms.ValidationError({'tags': '1 to 12 tags are required.'})


class QuestionCreateForm(ModelForm):
    tags = MultiTagField()

    def clean(self):
        super().clean()
        return self.cleaned_data

    def save(self, **kwargs):
        tags = []
        for t in self.cleaned_data['tags']:
            tag = Tag.objects.filter(title=t).first()
            if tag:
                tags.append(tag)
            else:
                new_tag = Tag(title=t)
                new_tag.save()
                tags.append(new_tag)

        q = Question(author=kwargs['author'],
                     title=self.cleaned_data['title'],
                     text=self.cleaned_data['text'])
        q.save()

        q.add_tags(tags)
        return q

    class Meta:
        model = Question
        fields = ['title', 'text']


class AnswerForm(ModelForm):
    def clean(self):
        super().clean()
        return self.cleaned_data

    def save(self, **kwargs):
        a = Answer()


    class Meta:
        model = Question
        fields = ['text']
