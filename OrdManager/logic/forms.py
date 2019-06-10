from django.forms import ModelForm

from logic.models import Staff, Orders


class StaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['surname', 'first_name', 'second_name']


class OrdersForm(ModelForm):
    class Meta:
        model = Orders
        fields = ['buyer', 'buyId', 'name_of_buy', 'price_of_buy']
