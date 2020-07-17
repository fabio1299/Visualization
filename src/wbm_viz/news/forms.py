from django import forms
from bootstrap_datepicker_plus import DatePickerInput,YearPickerInput

class DataScopeForm(forms.Form):
    year = forms.IntegerField(initial=1975, min_value=1975, max_value=2060, required=True,
                              widget=YearPickerInput(format='%Y',attrs={'id':'data_scope_year'}))
    # model = forms.ChoiceField(choices=[('GFDL', 'GFDL-ESM2M_RCP2p6_Final925'),
    #                                    ('value','human_readable'),
    #                                    ]
    #                           )

class DistancePlotForm(forms.Form):
    day = forms.DateField(
        widget=DatePickerInput(attrs={'id': 'datetimepicker1'})
    )