from django import forms


class ContactUsForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder':'Username',
                'required':True,
                'name':'name',
                'type':'text',
                'id':'required'
                }
                ))


    email = forms.CharField(
        widget = forms.TextInput(
                attrs={
                    'placeholder':'Email',
                    'required':True,
                    'id':'required',
                    'type':'email',
                    'name':'email',
                }
            ))

    subject = forms.CharField(
        widget = forms.TextInput(
                attrs={
                    'placeholder':'Subject of Mail',
                    'required':True,
                    'id':'required',
                    'type':'text',

                }
                ))

    message = forms.CharField(
        widget = forms.Textarea(
                attrs={
                    'placeholder':'Enter your message',
                    'required':True,
                    'id':'required',
                    'name':'message',
            })
        )
