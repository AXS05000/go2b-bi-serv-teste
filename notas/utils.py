import openpyxl

from .models import BaseCNPJ


def update_basecnpj_from_excel(file_path):
    # Abre a planilha desejada
    workbook = openpyxl.load_workbook(file_path)
    worksheet = workbook['Planilha1']

    # Armazena os dados da planilha em uma lista de dicionários
    rows = list(worksheet.values)
    headers = rows[0]
    basecnpj_data = [dict(zip(headers, row)) for row in rows[1:]]

    # Atualiza os objetos do modelo BaseCNPJ com base nos dados da planilha
    for data in basecnpj_data:
        basecnpj = BaseCNPJ.objects.get(id=data['ID'])
        basecnpj.tx_adm = data['taxa Adm']
        basecnpj.save()

def import_basecnpj_from_excel(file_path):
    # Abre a planilha desejada
    workbook = openpyxl.load_workbook(file_path)
    worksheet = workbook['Planilha1']

    # Armazena os dados da planilha em uma lista de dicionários
    rows = list(worksheet.values)
    headers = rows[0]
    basecnpj_data = [dict(zip(headers, row)) for row in rows[1:]]

    # Cria objetos BaseCNPJ com base nos dados da planilha
    for data in basecnpj_data:
        BaseCNPJ.objects.create(
            cnpj=data['CNPJ'],
            razao=data['Razão Social'],
            avenida_rua=data['Avenida/Rua'],
            endereco=data['Endereço'],
            numero=data['Número'],
            complemento=data['Complemento'],
            bairro=data['Bairro'],
            municipio=data['Municipio'],
            uf=data['UF'],
            cep=data['Cep'],
            nome_cliente=data['Nome Cliente'],
            tipo_de_servico=data['Tipo de Serviço'],
            iss=data['ISS'],
            unidade=data['Unidade'],
            mcu=data['MCU'],
            tipo_de_cliente=data['Tipo de Cliente'],
            tx_adm=data['taxa Adm']
        )


