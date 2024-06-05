from django.contrib import admin, messages
import django.contrib.admin.helpers
from django.http import HttpResponse
from django.utils.encoding import smart_str, iri_to_uri

from .models import *
from .helper import generate_business_trip_doc


def generate_business_trip_doc_run(modeladmin, request, queryset):
    id_dict = request.POST.getlist('_selected_action')
    if len(id_dict) == 1:  # Проверка, что указана только один заказ для создания документа
        response_file_path = generate_business_trip_doc(id_dict[0])
        print(response_file_path)
        with open(response_file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = f'attachment; filename={iri_to_uri(response_file_path.split("/")[-1])}'
            response['X-Sendfile'] = smart_str(response_file_path)
            return response
    else:
        messages.error(request, message=f'Укажите один документ, который хотите сформировать')


generate_business_trip_doc_run.short_description = 'Сгенерировать документ для командировки'


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    params = ('name', 'departament', 'post', 'phone_number')
    list_display = params
    list_filter = params
    search_fields = params


@admin.register(WorkerPost)
class WorkerPost(admin.ModelAdmin):
    params = ('title',)
    list_display = params
    list_filter = params
    search_fields = params


@admin.register(WorkerDepartament)
class WorkerDepartament(admin.ModelAdmin):
    params = ('name',)
    list_display = params
    list_filter = params
    search_fields = params


@admin.register(BusinessTrip)
class BusinessTripAdmin(admin.ModelAdmin):
    params = ('city', 'worker', 'reason', 'depart_date', 'duration',)

    list_display = params
    list_filter = params
    search_fields = params

    actions = (generate_business_trip_doc_run,)

    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST and request.POST['action'] == 'generate_business_trip_doc_run':
            if not request.POST.getlist(django.contrib.admin.helpers.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in BusinessTrip.objects.all()[0:2]:
                    post.update({django.contrib.admin.helpers.ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(BusinessTripAdmin, self).changelist_view(request, extra_context)

    def download_file(self, request, pk):
        response = HttpResponse(content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="whatever.txt"'
        # generate dynamic file content using object pk
        response.write('whatever content')
        return response

@admin.register(BusinessTripReason)
class BusinessTripReason(admin.ModelAdmin):
    params = ('reason',)
    list_display = params
    list_filter = params
    search_fields = params


@admin.register(BusinessTripCity)
class BusinessTripCity(admin.ModelAdmin):
    params = ('city', 'daily_allowance', )
    list_display = params
    list_filter = params
    search_fields = params


@admin.register(TelegramInfo)
class TelegramInfo(admin.ModelAdmin):
    params = ('telegram_login', )
    list_display = params
    list_filter = params
    search_fields = ('telegram_login', 'telegram_id')


@admin.register(Order)
class Order(admin.ModelAdmin):
    params = ('docs', 'client', 'worker', 'price',)

    list_display = params
    list_filter = params
    search_fields = params


@admin.register(Docs)
class Docs(admin.ModelAdmin):
    params = ('file_name', )
    list_display = params
    list_filter = params
    search_fields = params


@admin.register(DocsType)
class DocsType(admin.ModelAdmin):
    params = ('type', )
    list_display = params
    list_filter = params
    search_fields = params


@admin.register(Client)
class Client(admin.ModelAdmin):
    params = ('name', 'entity', 'company_id', 'phone_number', 'mail',)
    list_display = params
    list_filter = params
    search_fields = params


@admin.register(ClientCompany)
class ClientCompany(admin.ModelAdmin):
    params = ('title', 'inn',)
    list_display = params
    list_filter = params
    search_fields = params


@admin.register(Product)
class Product(admin.ModelAdmin):
    params = ('order_id', 'product_params', 'count',)
    list_display = params
    list_filter = params
    search_fields = params


@admin.register(ProductParams)
class ProductParams(admin.ModelAdmin):
    params = ('name', 'product_type', 'price',)
    list_display = params
    list_filter = params
    search_fields = params


@admin.register(ProductType)
class ProductType(admin.ModelAdmin):
    params = ('name',)
    list_display = params
    list_filter = params
    search_fields = params
