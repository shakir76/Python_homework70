from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.core.validators import MinLengthValidator
from webapp.models import Tag, Article





# class ArticleForm(forms.Form):
#     title = forms.CharField(max_length=50, required=True, label='Title')
#     author = forms.CharField(max_length=50, required=True, label='Author')
#     content = forms.CharField(max_length=3000, required=True, label='Content',
#                               widget=widgets.Textarea(attrs={"cols": 40, "rows": 3}))
#     tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
#                                           required=False, label='Teg')

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ["title", "author", "content", "tags"]
        widgets = {
            "tags": widgets.CheckboxSelectMultiple,
            "content": widgets.Textarea(attrs={"placeholder": "введите контент"})
        }

    # def clean_title(self):
    #     title = self.cleaned_data.get("title")
    #     if len(title) > 7:
    #         raise ValidationError("Название должно быть  короче 7 символов")
    #     return title

    def clean(self):
        if self.cleaned_data.get("title") == self.cleaned_data.get("content"):
            raise ValidationError("Название и описание не могут совпадать")
        return super().clean()
