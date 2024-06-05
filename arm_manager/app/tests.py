import os
import django
import openpyxl
import pandas as pd

os.environ['DJANGO_SETTINGS_MODULE'] = 'arm_manager.settings'
django.setup()

from app.models import BusinessTrip
from arm_manager.settings import MEDIA_ROOT
from app.helper import generate_business_trip_doc

def generate_excel():

    worker = 'Кожан'

    depart_date = '2024-06-06'

    csv_sample_path = pd.read_csv(f'{MEDIA_ROOT}/media/static/business_trip.csv', sep=';', encoding='latin-1')

    xlsx_path = f'{MEDIA_ROOT}/media/static/командировка_{worker}_{depart_date}.xlsx'

    # print(csv_sample_path)
    # print(xlsx_path)

    wb = openpyxl.load_workbook(f'{MEDIA_ROOT}/media/static/business_trip.xlsx')

    sheet = wb.active

    sheet['B1'].value = '228'

    sheet['C1'].value = '2024-05-06'

    wb.save(xlsx_path)


generate_business_trip_doc(1)
