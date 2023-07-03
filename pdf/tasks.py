from __future__ import absolute_import, unicode_literals

import os

import openpyxl
from celery import shared_task
from django.core.paginator import Paginator

from .models import Beneficios_Mala


def non_null_defaults(row):
    fields = [
        'comp',
        'codigo',
        'codigo_fc',
        'aut',
        'data_inicio',
        'data_fim',
        'dias_calculados',
        'tipo_de_beneficio',
        'valor_pago',
        'data_de_pagamento',
    ]

    return {field: value for field, value in zip(fields, row[1:]) if value is not None}

@shared_task
def importar_excel_beneficios(filepath):
    workbook = openpyxl.load_workbook(filepath, read_only=True)
    sheet = workbook.active

    rows = list(sheet.iter_rows(min_row=2, values_only=True))  # Converter o gerador em uma lista

    paginator = Paginator(rows, 1000)  # 1000 linhas por página

    for page_number in paginator.page_range:
        page = paginator.page(page_number)
        for row in page.object_list:
            defaults = non_null_defaults(row)
            Beneficios_Mala.objects.update_or_create(id=row[0], defaults=defaults)
    
    # Remove the file after processing
    os.remove(filepath)
