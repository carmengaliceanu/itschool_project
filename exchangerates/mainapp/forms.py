from django import forms

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date must be greater than or equal to start date.")
        
        return cleaned_data


class ExchangeCalculatorForm(forms.Form):
    amount_in_eur = forms.FloatField(label="Amount in EUR")
    
    def clean_amount_in_eur(self):
        amount_in_eur = self.cleaned_data["amount_in_eur"]
        if amount_in_eur <= 0:
            raise forms.ValidationError("* Amount must be greater than 0.")
        
        return amount_in_eur