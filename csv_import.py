import pandas as pd
from datetime import datetime


import os
import sys


# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GPCRtrack.settings')

import django
django.setup()

from app.models import ConstructItem, ApplicationItem


csv_file_path = 'data/export_all_application_data.csv'
data_frame = pd.read_csv(csv_file_path)

for _, row in data_frame.iterrows():
    construct_number = row['construct_number']
    P = row['P']
    biomass = row['biomass']
    expression_system = row['expression_system']
    application_user = row['application_user']
    comment = row['comment']
    application_time = datetime.strptime(row['application_time'], '%Y-%m-%d %H:%M:%S.%f%z')

    tt=ApplicationItem(construct_number=construct_number,
                          P=P,
                          biomass=biomass,
                          expression_system=expression_system,
                          application_user=application_user,
                          comment=comment,
                          application_time=application_time
                          )
    tt.application_time = application_time
    tt.save()

    print(f'saving {row}')

csv_file_path = 'data/export_all_construct_data.csv'
data_frame = pd.read_csv(csv_file_path)

for _, row in data_frame.iterrows():
    construct_number = row['construct_number']
    receptor = row['receptor']
    DNA_sequence = row['DNA_sequence']
    description = row['description']
    comment = row['comment']
    user = row['user']
    application_time = datetime.strptime(row['application_time'], '%Y-%m-%d %H:%M:%S.%f%z')

    tt = ConstructItem(construct_number=construct_number,
                        receptor=receptor,
                        DNA_sequence=DNA_sequence,
                        description=description,
                        comment=comment,
                        user=user,
                        application_time=application_time
                        )
    tt.application_time = application_time
    tt.save()

    print(f'saving {row}')
