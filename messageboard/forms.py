# messageboard/forms.py

from django import forms

from .models import Comment, Message


class MessageboardForm(forms.ModelForm):
    nickname = forms.CharField(
        max_length=100, label='ニックネーム', initial='unknown')

    class Meta:
        model = Message
        fields = (
            'message',
        )
        labels = {
            'message': 'メッセージ',
        }
        widgets = {
            'message': forms.Textarea,
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if 'test' in message:
            raise forms.ValidationError('testという文言は含められません')
        return message


# class MessageboardForm(forms.Form):
#     message = forms.CharField(
#         max_length=240,
#         label='メッセージ',
#         widget=forms.Textarea(
#             attrs={'class': 'uk-textarea', 'placeholder': '240文字いないで入力'},
#         ))
#     nickname = forms.CharField(
#         max_length=100,
#         label='ニックネーム',
#         widget=forms.TextInput(
#             attrs={'class': 'uk-input', 'placeholder': '表示される名前'},
#         ))


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = (
            'comment',
        )

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        ng_words = ["ばか", "バカ", "あほ", "アホ"]
        for ng_word in ng_words:
            if ng_word in comment:
                raise forms.ValidationError(f'{ng_word}という文言は含められません')
        return comment
