from app.models import *
import openpyxl

from datetime import date, timedelta

from arm_manager.settings import MEDIA_ROOT


def generate_business_trip_doc(trip_id):
    # Получение объекта из базы данных
    trip_data = BusinessTrip.objects.get(id=trip_id)

    # Путь для конечного файла
    xlsx_path = f'{MEDIA_ROOT}/media/static/Командировка_{trip_data.worker.name}_{trip_data.depart_date}.xlsx'

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

    work_book.save(xlsx_path)

    return xlsx_path
