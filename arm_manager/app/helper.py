import os
import openpyxl

from app.models import BusinessTrip, Order, Product
from datetime import date, timedelta
from django.db.models import Sum, F
from arm_manager.settings import MEDIA_ROOT


def generate_business_trip_doc(trip_id):
    # Получение объекта из базы данных
    trip_data = BusinessTrip.objects.get(id=trip_id)

    # Путь для конечного файла
    xlsx_path = f'{MEDIA_ROOT}/media/static/Командировка_{trip_data.worker.name}_{trip_data.depart_date}.xlsx'

    # Если файл уже существует, то сразу вернется его путь
    if os.path.exists(xlsx_path):
        return xlsx_path

    # Подгрузка шаблона для генерации конечного файла
    work_book = openpyxl.load_workbook(f'{MEDIA_ROOT}/media/static/business_trip.xlsx')

    # Переход на активную страницу документа (первую)
    sheet = work_book.active

    # Проставление значений в таблицу
    sheet['E7'].value = trip_id
    sheet['F7'].value = date.today()
    sheet['D12'].value = trip_data.worker.name
    sheet['D13'].value = trip_data.worker.departament.name
    sheet['D14'].value = trip_data.worker.post.title
    sheet['D15'].value = trip_data.city.city
    sheet['D17'].value = trip_data.depart_date
    sheet['D18'].value = trip_data.depart_date + timedelta(days=trip_data.duration)
    sheet['D19'].value = trip_data.duration
    sheet['D20'].value = trip_data.reason.reason

    # Сохранение листа в конечный файл
    work_book.save(xlsx_path)

    return xlsx_path


def generate_order_doc(order_id):
    # Получение объекта заказа из базы данных
    order_data = Order.objects.get(id=order_id)

    # Путь для конечного файла
    xlsx_path = f'{MEDIA_ROOT}/media/static/Накладная_{order_data.client.name}_{date.today()}.xlsx'

    # Если файл уже существует, то сразу вернется его путь
    if os.path.exists(xlsx_path):
        return xlsx_path

    # Получение query_set для подзапросов
    product_query = Product.objects.filter(order_id=order_id)

    # Основной запрос с информацией о заказе
    product_data = product_query.values('product_params_id__name',
                                        'count',
                                        'product_params_id__price')
    # Подсчет общей стоимости
    full_price = product_query.aggregate(sum_product=Sum(F('product_params_id__price') * F('count')))['sum_product']

    # Количество единиц товара в заказе
    product_counts = product_query.aggregate(count=Sum(F('count')))['count']

    # Подгрузка шаблона для генерации конечного файла
    work_book = openpyxl.load_workbook(f'{MEDIA_ROOT}/media/static/invoice.xlsx')

    # Переход на активную страницу документа (первую)
    sheet = work_book.active

    # Проставление значений в таблицу
    sheet['H2'].value = f'№{order_id} от {date.today()}'
    sheet['D6'].value = f'{order_data.client.name} {order_data.client.company_id.title if order_data.client.entity else ""}'
    sheet['D31'].value = product_counts
    sheet['D33'].value = full_price
    sheet['D35'].value = order_data.worker.name
    sheet['D38'].value = order_data.client.name

    # Начинаем заполнять строчки с информацией о продукте
    for i, product in enumerate(product_data):
        sheet[f'B{14+i}'].value = i + 1
        sheet[f'C{14+i}'].value = product['product_params_id__name']
        sheet[f'H{14+i}'].value = 'шт'
        sheet[f'K{14+i}'].value = product['count']
        sheet[f'L{14+i}'].value = product['product_params_id__price']
        sheet[f'M{14+i}'].value = product['product_params_id__price'] * product['count']

    # Сохранение листа в конечный файл
    work_book.save(xlsx_path)

    return xlsx_path
