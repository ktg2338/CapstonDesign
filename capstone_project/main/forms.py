from django import forms

class Company(forms.Form):
    company_set = (
        ('삼성전자', '삼성전자'),
        ('LG전자', 'LG전자'),
        ('NAVER', '네이버'),
        ('카카오', '카카오')
    )

    #company_name = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=company_set)
    company_name_text = forms.CharField(widget=forms.TextInput, max_length=20)
