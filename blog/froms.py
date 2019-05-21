from django import forms
from blog import models

class CommentForm(forms.ModelForm):
    host = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'host', 'class': 'form-control', 'placeholder': 'http://'}))
    class Meta:
        model = models.Comment
        fields = ('name', 'email', 'host', 'text')
        widgets = {
            'name' : forms.TextInput(attrs={'id':'name', 'class':'form-control', 'placeholder': '请输入昵称'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder': '请输入邮箱'}),
            'host': forms.TextInput(attrs={'id': 'host', 'class': 'form-control', 'placeholder': 'http://'}),
            'text': forms.Textarea(attrs={'id':'content', 'rows':'10', 'cols':'50', 'class': 'form-control', 'placeholder': '请输入评论内容'}),
        }

        # def __init__(self, *args, **kwargs):
        #     super(CommentForm, self).__init__(*args, **kwargs)
        #     self.fields['host']'.required = False

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['host'].required = False
