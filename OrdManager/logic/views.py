from django.http import request, JsonResponse
from django.shortcuts import render, redirect
from django.db import connections
from django.http import QueryDict
import datetime
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from logic.forms import StaffForm, OrdersForm
from logic.models import Staff, Orders, User


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class MainPage(TemplateView):
    template_name = 'logic/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainPage, self).get_context_data(**kwargs)
        if self.request.user.is_anonymous:
            context['staff'] = []
        else:
            context['staff'] = Staff.objects.filter(company=self.request.user)
        context['groups'] = {'ПАСТА': "group16", 'ПОСУДА': "group17", 'ЗАКУСКИ, САЛАТЫ': "group20",
                             'ДЕСЕРТЫ': "group21", 'ГОРЯЧИЕ НАПИТКИ': "group22",
                             'ПИЦЦА, ХЛЕБ': "group23", 'ХОЛОДНЫЕ НАПИТКИ': "group24", 'АЛКОГОЛЬ': "group25",
                             'ПЕРВЫЕ БЛЮДА, ЗАВТРАКИ': "group28", 'ОСНОВНЫЕ БЛЮДА': 'group39'}
        context['date'] = datetime.date.today()
        with connections['source'].cursor() as cursor:
            if 'search' in self.request.GET:
                question = self.request.GET.get('search')
                if question is not None and question != '':
                    cursor.execute(f'SELECT shifr, shifr_1, text, price, acp_textprn FROM items WHERE text '
                                   f'LIKE "%{question}%"')
                    context['result'], context['is_search'] = cursor.fetchall(), 1
            else:
                # cursor.execute('SELECT * FROM groups')
                # context['groups'] = cursor.fetchall()
                cursor.execute('SELECT shifr, shifr_1, text, price, acp_textprn, netto FROM items')
                db_set = cursor.fetchall()
                group_num_set, context['is_search'] = set(), 0
                for elem in db_set:
                    elem = list(elem)
                    price = float(elem[3]/100)
                    elem.insert(3, price)
                    if not elem[1] in group_num_set:
                        group_num_set.add(elem[1])
                        context[f'group{elem[1]}'] = []
                    context[f'group{elem[1]}'].append(elem)
            context['form'] = StaffForm()
            context['orders'] = Orders.objects.filter(data_of_buy=context['date'])
        return context

    def post(self, request):
        form = StaffForm()
        form = form.save(commit=False)
        form.company = request.user
        form.surname = request.POST.get('surname')
        form.first_name, form.second_name = request.POST.get('first_name'), request.POST.get('second_name')
        form.save()
        return redirect('main')


class ToBuy(View):

    def post(self, request):
        buy_id, buyer_id = request.POST['buyId'], request.POST['buyer_id']
        name_of_buy, price = request.POST['name'], float(request.POST['price'].replace(',', '.'))
        form = OrdersForm().save(commit=False)
        form.buyer = Staff.objects.get(pk=buyer_id)
        form.name_of_buy, form.price_of_buy, form.buy_id = name_of_buy, price, buy_id
        form.save()
        return JsonResponse({'status': 'success'})

    def delete(self, request):
        request_data = QueryDict(request.body)
        if 'buyerToDell' in request_data:
            buyer_to_delete = request_data.get('buyerToDell')
            Staff.objects.get(pk=buyer_to_delete).orders_set.all().delete()
        elif 'id' in request_data:
            pk_to_delete = request_data.get('id')
            Orders.objects.filter(pk=pk_to_delete).delete()
        elif 'companyid' in request_data:
            company_pk_to_delete = request_data.get('companyid')
            staff = User.objects.get(pk=company_pk_to_delete).staff_set.all().prefetch_related('orders_set')
            for worker in staff:
                worker.orders_set.all().delete()
        return JsonResponse({'status': 'success'})

    def patch(self, request):
        request_data = QueryDict(request.body)
        if 'companyid' in request_data:
            company_id = request_data.get('companyid')
            staff = Staff.objects.filter(company_id=company_id).prefetch_related('orders_set')
            for employee in staff:
                employee.orders_set.all().update(status=1)
        else:
            new_amount, pk_to_change_amount = request_data.get('amount'), request_data.get('id')
            Orders.objects.filter(pk=pk_to_change_amount).update(amount=new_amount)
        return JsonResponse({'status': 'success'})


class ChangeStaff(View):

    def delete(self, request):
        request_data = QueryDict(request.body)
        pk_to_delete = request_data.get('id')
        Staff.objects.filter(pk=pk_to_delete).delete()
        return JsonResponse({'status': 'success'})

    def patch(self, request):
        request_data = QueryDict(request.body)
        new_name, pk_to_change_amount = request_data.get('name'), request_data.get('id')
        new_surname, new_second_name = request_data.get('surname'), request_data.get('secondname')
        Staff.objects.filter(pk=pk_to_change_amount).update(first_name=new_name, surname=new_surname,
                                                            second_name=new_second_name)
        return JsonResponse({'status': 'success'})
