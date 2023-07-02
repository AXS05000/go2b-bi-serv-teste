from __future__ import absolute_import, unicode_literals

import os

import openpyxl
from celery import shared_task
from django.core.paginator import Paginator

from .models import Beneficios_Mala


@shared_task
def importar_excel_beneficios(filepath):
    workbook = openpyxl.load_workbook(filepath, read_only=True)
    sheet = workbook.active

    rows = list(sheet.iter_rows(min_row=2, values_only=True))  # Converter o gerador em uma lista

    paginator = Paginator(rows, 1000)  # 1000 linhas por página

    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        for row in page.object_list:
            Beneficios_Mala.objects.update_or_create(
                id=row[0],
                defaults={
                    'comp': row[1],
                    'codigo': row[2],
                    'codigo_fc': row[3],
                    'aut': row[4],
                    'data_inicio': row[5],
                    'data_fim': row[6],
                    'dias_calculados': row[7],
                    'tipo_de_beneficio': row[8],
                    'valor_pago': row[9],
                    'data_de_pagamento': row[10],
                }
            )
    
    # Remove the file after processing
    os.remove(filepath)
