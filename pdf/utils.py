import io

import openpyxl
from django.http import FileResponse
from reportlab.lib import colors, utils
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from .models import Funcionario


def importar_excel(arquivo):
    workbook = openpyxl.load_workbook(arquivo)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        id = row[0] if row[0] else None
        funcionario, created = Funcionario.objects.get_or_create(id=id)
        if created:
            defaults = {
                'comp': row[1],
                'cod_cliente': row[2],
                'cliente': row[3],
                'codigo': row[4],
                'codigo_fc': row[5],
                'cto': row[6],
                'cpf': row[7],
                'nome': row[8],
                'cargo': row[9],
                'adm': row[10],
                'dem_compt': row[11],
                'valid_desl': row[12],
                'tipo': row[13],
                'qtde_hs_normais': row[14],
                'horas_normais': row[15],
                'dissidio_retroativo': row[16],
                'dsr_s_horas_normal': row[17],
                'qtde_hs_not': row[18],
                'adicional_noturno': row[19],
                'dsr_s_adicional': row[20],
                'qtde_he_50': row[21],
                'hora_extra_50': row[22],
                'qtde_he_50_not': row[23],
                'hora_extra_50_noturno': row[24],
                'dsr_s_hora_extra_50': row[25],
                'qtde_he_100': row[26],
                'hora_extra_100': row[27],
                'qtde_he_100_not': row[28],
                'hora_extra_100_noturno': row[29],
                'dsr_s_hora_extra_100': row[30],
                'adic_periculosidade': row[31],
                'adicional_de_funcao_25': row[32],
                'adicional_de_atividade_30': row[33],
                'adicional_final_de_semana_15': row[34],
                'salario_familia': row[35],
                'falta_abonada_ponto_eletr': row[36],
                'qtde_atestado_horistas': row[37],
                'atestado_horistas': row[38],
                'licenca_remunerada_gestante': row[39],
                'salario_maternidade': row[40],
                'aux_doenca_15_dias': row[41],
                'acidente_de_trabalho_15_dias': row[42],
                'acidente_de_trabalho_fgts': row[43],
                'fgts_pago_rct': row[44],
                'fgts_multa_40': row[45],
                'fgts_s_13_salario': row[46],
                'fgts_s_aviso_previo': row[47],
                'verbas_rescisorias': row[48],
                'saldo_negativo_verba_nao_repassada': row[49],
                'ferias': row[50],
                'um_terco_ferias': row[51],
                'decimo_terceiro_salario_indenizado_e_adicionais_considerar': row[52],
                'decimo_terceiro_salario_indenizado_e_adicionais': row[53],
                'antecip_13_a_vencer': row[54],
                'ferias_adiantadas': row[55],
                'inss_s_13_salario': row[56],
                'inss_s_ferias': row[57],
                'inss_s_hora_extra': row[58],
                'inss_s_aviso_previo': row[59],
                'irrf_s_13_salario': row[60],
                'irrf_s_ferias': row[61],
                'irrf_s_aviso_previo': row[62],
                'inss_s_13_salario_adicional': row[63],
                'inss_s_13_salario_abono': row[64],
                'inss_s_ferias_vendidas': row[65],
                'inss_s_ferias_vendidas_adiantadas': row[66],
                'inss_s_ferias_adiantadas': row[67],
                'inss_s_13_salario_complementar': row[68],
                'irrf_s_ferias_vendidas': row[69],
                'irrf_s_ferias_vendidas_adiantadas': row[70],
                'irrf_s_ferias_adiantadas': row[71],
                'irrf_s_13_salario_complementar': row[72],
                'contrib_sindical': row[73],
                'contrib_assistencial': row[74],
                'contrib_confederativa': row[75],
                'contrib_outra': row[76],
                'plano_saude': row[77],
                'vr': row[78],
                'vt': row[79],
                'uniforme': row[80],
                'seguro_vida': row[81],
                'vale_gasolina': row[82],
                'vale_cultura': row[83],
                'liquido_1': row[84],
                'aut_1': row[85],
                'liquido_2': row[86],
                'aut_2': row[87],
                'liquido_3': row[88],
                'aut_3': row[89],
                'liquido_4': row[90],
                'aut_4': row[91],
                'liquido_5': row[92],
                'aut_5': row[93],
                'data_1': row[94],
                'data_2': row[95],
                'data_3': row[96],
                'data_4': row[97],
                'data_5': row[98],
                'qtde_dsr_feriado': row[99],
                'dsr_feriado': row[100],
            }
        else:
            defaults = {}
            if row[1] is not None:
                defaults['comp'] = row[1]
            if row[2] is not None:
                defaults['cod_cliente'] = row[2]
            if row[3] is not None:
                defaults['cliente'] = row[3]
            if row[4] is not None:
                defaults['codigo'] = row[4]
            if row[5] is not None:
                defaults['codigo_fc'] = row[5]
            if row[6] is not None:
                defaults['cto'] = row[6]
            if row[7] is not None:
                defaults['cpf'] = row[7]
            if row[8] is not None:
                defaults['nome'] = row[8]
            if row[9] is not None:
                defaults['cargo'] = row[9]
            if row[10] is not None:
                defaults['adm'] = row[10]
            if row[11] is not None:
                defaults['dem_compt'] = row[11]
            if row[12] is not None:
                defaults['valid_desl'] = row[12]
            if row[13] is not None:
                defaults['tipo'] = row[13]
            if row[14] is not None:
                defaults['qtde_hs_normais'] = row[14]
            if row[15] is not None:
                defaults['horas_normais'] = row[15]
            if row[16] is not None:
                defaults['dissidio_retroativo'] = row[16]
            if row[17] is not None:
                defaults['dsr_s_horas_normal'] = row[17]
            if row[18] is not None:
                defaults['qtde_hs_not'] = row[18]
            if row[19] is not None:
                defaults['adicional_noturno'] = row[19]
            if row[20] is not None:
                defaults['dsr_s_adicional'] = row[20]
            if row[21] is not None:
                defaults['qtde_he_50'] = row[21]
            if row[22] is not None:
                defaults['hora_extra_50'] = row[22]
            if row[23] is not None:
                defaults['qtde_he_50_not'] = row[23]
            if row[24] is not None:
                defaults['hora_extra_50_noturno'] = row[24]
            if row[25] is not None:
                defaults['dsr_s_hora_extra_50'] = row[25]
            if row[26] is not None:
                defaults['qtde_he_100'] = row[26]
            if row[27] is not None:
                defaults['hora_extra_100'] = row[27]
            if row[28] is not None:
                defaults['qtde_he_100_not'] = row[28]
            if row[29] is not None:
                defaults['hora_extra_100_noturno'] = row[29]
            if row[30] is not None:
                defaults['dsr_s_hora_extra_100'] = row[30]
            if row[31] is not None:
                defaults['adic_periculosidade'] = row[31]
            if row[32] is not None:
                defaults['adicional_de_funcao_25'] = row[32]
            if row[33] is not None:
                defaults['adicional_de_atividade_30'] = row[33]
            if row[34] is not None:
                defaults['adicional_final_de_semana_15'] = row[34]
            if row[35] is not None:
                defaults['salario_familia'] = row[35]
            if row[36] is not None:
                defaults['falta_abonada_ponto_eletr'] = row[36]
            if row[37] is not None:
                defaults['qtde_atestado_horistas'] = row[37]
            if row[38] is not None:
                defaults['atestado_horistas'] = row[38]
            if row[39] is not None:
                defaults['licenca_remunerada_gestante'] = row[39]
            if row[40] is not None:
                defaults['salario_maternidade'] = row[40]
            if row[41] is not None:
                defaults['aux_doenca_15_dias'] = row[41]
            if row[42] is not None:
                defaults['acidente_de_trabalho_15_dias'] = row[42]
            if row[43] is not None:
                defaults['acidente_de_trabalho_fgts'] = row[43]
            if row[44] is not None:
                defaults['fgts_pago_rct'] = row[44]
            if row[45] is not None:
                defaults['fgts_multa_40'] = row[45]
            if row[46] is not None:
                defaults['fgts_s_13_salario'] = row[46]
            if row[47] is not None:
                defaults['fgts_s_aviso_previo'] = row[47]
            if row[48] is not None:
                defaults['verbas_rescisorias'] = row[48]
            if row[49] is not None:
                defaults['saldo_negativo_verba_nao_repassada'] = row[49]
            if row[50] is not None:
                defaults['ferias'] = row[50]
            if row[51] is not None:
                defaults['um_terco_ferias'] = row[51]
            if row[52] is not None:
                defaults['decimo_terceiro_salario_indenizado_e_adicionais_considerar'] = row[52]
            if row[53] is not None:
                defaults['decimo_terceiro_salario_indenizado_e_adicionais'] = row[53]
            if row[54] is not None:
                defaults['antecip_13'] = row[54]
            if row[55] is not None:
                defaults['dev_desc_exame_medico_epi_unif'] = row[55]
            if row[56] is not None:
                defaults['arredondamento'] = row[56]
            if row[57] is not None:
                defaults['dif_vale_transporte'] = row[57]
            if row[58] is not None:
                defaults['dif_vale_refeicao'] = row[58]
            if row[59] is not None:
                defaults['vencimentos'] = row[59]
            if row[60] is not None:
                defaults['qtde_dias_e_hs_desconto'] = row[60]
            if row[61] is not None:
                defaults['desc_faltas_dias_atrasos_e_horas_indevidas'] = row[61]
            if row[62] is not None:
                defaults['desc_dsr_s_faltas_dias'] = row[62]
            if row[63] is not None:
                defaults['falta_abonada_efeito_visualizacao'] = row[63]
            if row[64] is not None:
                defaults['desc_saldo_negativo'] = row[64]
            if row[65] is not None:
                defaults['desc_arredondamento'] = row[65]
            if row[66] is not None:
                defaults['desc_aviso'] = row[66]
            if row[67] is not None:
                defaults['desc_antecipacao_13_salario'] = row[67]
            if row[68] is not None:
                defaults['desc_inss_desc_irrf'] = row[68]
            if row[69] is not None:
                defaults['desc_inss_s_13_salario'] = row[69]
            if row[70] is not None:
                defaults['desc_inss_ferias'] = row[70]
            if row[71] is not None:
                defaults['desc_acidente_de_trabalho_fgts'] = row[71]
            if row[72] is not None:
                defaults['aux_doenca_15_dias_aus_legais'] = row[72]
            if row[73] is not None:
                defaults['desc_fgts_deposito_rescisao_grfc'] = row[73]
            if row[74] is not None:
                defaults['desc_pensao_alimenticia'] = row[74]
            if row[75] is not None:
                defaults['desc_uniforme_epi_div_sind_judic_adiant_mater'] = row[75]
            if row[76] is not None:
                defaults['seguro_vida'] = row[76]
            if row[77] is not None:
                defaults['desc_assist_odontologica'] = row[77]
            if row[78] is not None:
                defaults['desc_vale_transporte_nao_utilizado'] = row[78]
            if row[79] is not None:
                defaults['desc_vale_transporte'] = row[79]
            if row[80] is not None:
                defaults['desc_vr_va'] = row[80]
            if row[81] is not None:
                defaults['desc_vale_refeicao_nao_utilizado'] = row[81]
            if row[82] is not None:
                defaults['descontos'] = row[82]
            if row[83] is not None:
                defaults['liquido'] = row[83]
            if row[84] is not None:
                defaults['liquido_1'] = row[84]
            if row[85] is not None:
                defaults['aut_1'] = row[85]
            if row[86] is not None:
                defaults['liquido_2'] = row[86]
            if row[87] is not None:
                defaults['aut_2'] = row[87]
            if row[88] is not None:
                defaults['liquido_3'] = row[88]
            if row[89] is not None:
                defaults['aut_3'] = row[89]
            if row[90] is not None:
                defaults['liquido_4'] = row[90]
            if row[91] is not None:
                defaults['aut_4'] = row[91]
            if row[92] is not None:
                defaults['liquido_5'] = row[92]
            if row[93] is not None:
                defaults['aut_5'] = row[93]
            if row[94] is not None:
                defaults['data_1'] = row[94]
            if row[95] is not None:
                defaults['data_2'] = row[95]
            if row[96] is not None:
                defaults['data_3'] = row[96]
            if row[97] is not None:
                defaults['data_4'] = row[97]
            if row[98] is not None:
                defaults['data_5'] = row[98]
            if row[99] is not None:
                defaults['qtde_dsr_feriado'] = row[99]
            if row[100] is not None:
                defaults['dsr_feriado'] = row[100]


            for field, value in defaults.items():
                setattr(funcionario, field, value)

            funcionario.save()


        


def get_image(path, width):
    image = utils.ImageReader(path)
    aspect_ratio = float(image.getSize()[1]) / float(image.getSize()[0])
    height = aspect_ratio * width
    return path, width, height


def draw_centered_text(p, y, text, fontsize=11, fontname="Helvetica", fontstyle="normal"):
    if fontstyle == "bold":
        fontname = f"{fontname}-Bold"

    p.setFont(fontname, fontsize)
    text_width = p.stringWidth(text, fontname, fontsize)
    x = (letter[0] - text_width) / 2.2
    p.drawString(x, y, text)

def draw_info_rect(p, x, y, width, height, text, fontsize=11, fontname="Helvetica", fontstyle="normal"):
    p.rect(x, y, width, height)
    if fontstyle == "bold":
        fontname = f"{fontname}-Bold"
    p.setFont(fontname, fontsize)
    text_width = p.stringWidth(text, fontname, fontsize)
    text_x = x + (width - text_width) / 2
    text_y = y + height / 2 - fontsize / 2
    p.drawString(text_x, text_y, text)


def gerar_pdf(funcionario):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)


    # Configurar o título do arquivo PDF
    p.setTitle(f"{funcionario.comp} - {funcionario.codigo_fc} - {funcionario.nome}.pdf")


    logo_path, logo_width, logo_height = get_image('static/images/go2b3.jpg', 138)
    p.drawImage(logo_path, 210, 780, width=logo_width, height=logo_height)
    # Desenhe as informações do funcionário no PDF
    draw_centered_text(p, 750, f"EXTRATO SIMPLES - POR COLABORADOR – FATO GERADOR", fontsize=10, fontstyle="bold")
    draw_centered_text(p, 700, f"COMPETÊNCIA: {funcionario.comp}", fontsize=10, fontstyle="bold")
    draw_centered_text(p, 675, f"Contrato: {funcionario.cto}")
    draw_centered_text(p, 650, f"Matrícula: {funcionario.codigo_fc}")
    draw_centered_text(p, 625, f"Nome: {funcionario.nome}")
    draw_centered_text(p, 600, f"Cargo: {funcionario.cargo}")
    draw_centered_text(p, 575, f"Admissão: {funcionario.adm}")
    draw_centered_text(p, 550, f"Demissão: {funcionario.dem_compt}")
    draw_centered_text(p, 525, f"CPF: {funcionario.cpf}")
    draw_centered_text(p, 500, f"Cliente: {funcionario.cliente}")


    draw_centered_text(p, 425, f"IDENTIFICAÇÃO COMPROVANTE/EVIDÊNCIAS:", fontsize=10, fontstyle="bold")
    draw_centered_text(p, 400, f"• AUSÊNCIAS LEGAIS/FÉRIAS/DECIMO TERC./VERBAS RESCISÓRIAS/SAL.MATERN: VIDE AUTENTICAÇÕES E RECIBO.", fontsize=10, fontstyle="bold")
    draw_centered_text(p, 375, f"• FGTS RESCISÓRIO E FGTS SOBRE ACIDENTE TRABALHO: VIDE SEFIP E GRRF.", fontsize=10, fontstyle="bold")





    table_widthxx = 550

    rect_xx = (letter[0] - table_widthxx) / 2

    p.setFont("Helvetica", 10)
    p.drawString(rect_xx, 273, f"_________________________________________________________________________________________________")
    p.drawString(rect_xx, 181, f"_________________________________________________________________________________________________")
    
    
    p.setFont("Helvetica", 7)
    p.drawString(rect_xx + 275, 150, f"-------")
    p.drawString(rect_xx + 325, 150, f"-------")
    p.drawString(rect_xx + 400, 150, f"-------")
    p.drawString(rect_xx + 275, 135, f"-------")
    p.drawString(rect_xx + 325, 135, f"-------")
    p.drawString(rect_xx + 400, 135, f"-------")
    p.drawString(rect_xx + 275, 120, f"-------")
    p.drawString(rect_xx + 325, 120, f"-------")
    p.drawString(rect_xx + 400, 120, f"-------")
    p.drawString(rect_xx + 275, 105, f"-------")
    p.drawString(rect_xx + 325, 105, f"-------")
    p.drawString(rect_xx + 400, 105, f"-------")
    p.drawString(rect_xx + 275, 90, f"-------")
    p.drawString(rect_xx + 325, 90, f"-------")
    p.drawString(rect_xx + 400, 90, f"-------")

    draw_centered_text(p, 325, f"COMPROVANTE PAGAMENTO - COMPETÊNCIA: {funcionario.comp}", fontsize=12, fontstyle="bold")
    draw_centered_text(p, 300, f"FOLHA/RCT", fontsize=12, fontstyle="bold")

    p.setFont("Helvetica-Bold", 10)
    p.drawString(rect_xx + 10, 275, f"Dados Consultados")
    p.drawString(rect_xx + 10, 166, f"Autenticação")
    p.drawString(rect_xx + 200, 166, f"Data")
    p.drawString(rect_xx + 275, 166, f"Banco")
    p.drawString(rect_xx + 325, 166, f"Agência")
    p.drawString(rect_xx + 400, 166, f"Conta")
    p.drawString(rect_xx + 475, 166, f"Valor R$")


    p.setFont("Helvetica", 8)
    p.drawString(rect_xx + 10, 250, f"Agência:")
    p.drawString(rect_xx + 10, 235, f"Conta:")
    p.drawString(rect_xx + 10, 220, f"Descrição Lote:")
    p.drawString(rect_xx + 10, 205, f"Situação Lote:")
    p.drawString(rect_xx + 10, 190, f"Favorecidos:")
    p.drawString(rect_xx + 10 + 80, 250, f"1195-9 (BANCO DO BRASIL) OU 3380-4 (BRADESCO)")
    p.drawString(rect_xx + 10 + 80, 235, f"106742-7 (BANCO DO BRASIL) OU 15801-1 (BRADESCO)")
    p.drawString(rect_xx + 10 + 80, 220, f"PAG DIVERS DOC – CREDITO CONTA SALÁRIO")
    p.drawString(rect_xx + 10 + 80, 205, f"PROCESSADO - EFETUADO")


    p.setFont("Helvetica", 7)
    p.drawString(rect_xx + 10 + 80, 190, f"{funcionario.codigo_fc} - {funcionario.nome}")
    p.drawString(rect_xx + 10, 150, f"{funcionario.aut_1}")
    p.drawString(rect_xx + 200, 150, f"{funcionario.data_1}")
    p.drawString(rect_xx + 475, 150, f"{funcionario.liquido_1}")
    p.drawString(rect_xx + 10, 135, f"{funcionario.aut_2}")
    p.drawString(rect_xx + 200, 135, f"{funcionario.data_2}")
    p.drawString(rect_xx + 475, 135, f"{funcionario.liquido_2}")
    p.drawString(rect_xx + 10, 120, f"{funcionario.aut_3}")
    p.drawString(rect_xx + 200, 120, f"{funcionario.data_3}")
    p.drawString(rect_xx + 475, 120, f"{funcionario.liquido_3}")
    p.drawString(rect_xx + 10, 105, f"{funcionario.aut_4}")
    p.drawString(rect_xx + 200, 105, f"{funcionario.data_4}")
    p.drawString(rect_xx + 475, 105, f"{funcionario.liquido_4}")
    p.drawString(rect_xx + 10, 90, f"{funcionario.aut_5}")
    p.drawString(rect_xx + 200, 90, f"{funcionario.data_5}")
    p.drawString(rect_xx + 475, 90, f"{funcionario.liquido_5}")













    # Finalizar a primeira página e iniciar a segunda página
    p.showPage()



    # Desenhar as informações na segunda página
    draw_centered_text(p, 805, f"Recibo de Pagamento", fontsize=16, fontstyle="bold")
    p.setFont("Helvetica", 6) # Altere o segundo argumento para o tamanho desejado
    p.drawString(465, 787, f"Sofware Responsável http://www.gi.com.br") 
    
    # Defina a largura da tabela
    table_width = 550
    # Desenhar um retângulo com informações do funcionário acima da tabela
    rect_x = (letter[0] - table_width) / 2
    # Aqui mexe na altura de onde fica na pagina.
    rect_y = -24
    # Altura do retangulo
    rect_height = 60
    p.roundRect(rect_x, rect_y + 750, table_width, rect_height, 1, stroke=1, fill=0)
    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 10, rect_y + 750 + 48, f"Código:")
    p.drawString(rect_x + 10, rect_y + 750 + 35, f"{funcionario.codigo_fc}")
    p.drawString(rect_x + 50, rect_y + 750 + 48, f"Nome do Funcionário:")
    p.drawString(rect_x + 50, rect_y + 750 + 35, f"{funcionario.nome}")
    p.drawString(rect_x + 210, rect_y + 750 + 48, f"Função:")
    p.drawString(rect_x + 210, rect_y + 750 + 35, f"{funcionario.cargo}")
    p.drawString(rect_x + 345, rect_y + 750 + 48, f"Admissão:")
    p.drawString(rect_x + 345, rect_y + 750 + 35, f"{funcionario.adm}")
    p.drawString(rect_x + 400, rect_y + 750 + 48, f"Demissão:")
    p.drawString(rect_x + 400, rect_y + 750 + 35, f"{funcionario.dem_compt}")
    p.drawString(rect_x + 480, rect_y + 750 + 48, f"Competência:")
    p.drawString(rect_x + 480, rect_y + 750 + 35, f"{funcionario.comp}")


    data = [
        ['Cód. Descrição', 'Referência', 'Vencimentos', 'Descontos'],
        ['HORAS NORMAIS', f"{funcionario.qtde_hs_normais}", f"{funcionario.horas_normais}", ' '],
        ['D.S.R. S/HORAS NORMAL', ' ', f"{funcionario.dsr_s_horas_normal}", ' '],
        ['D.S.R. FERIADO', f"{funcionario.qtde_dsr_feriado}", f"{funcionario.dsr_feriado}", ' '],
        ['HORA EXTRA 100% / HORA EXTRA 100% NOT', f"{funcionario.qtde_he_100} / {funcionario.qtde_he_100_not}", f"{funcionario.hora_extra_100} / {funcionario.hora_extra_100_noturno}", ' '],
        ['D.S.R. S/HORA EXTRA 100%', ' ', f"{funcionario.dsr_s_hora_extra_100}", ' '],
        ['HORA EXTRA 50% / HORA EXTRA 50% NOT', f"{funcionario.qtde_he_50} / {funcionario.qtde_he_50_not}", f"{funcionario.hora_extra_50} / {funcionario.hora_extra_50_noturno}", ' '],
        ['D.S.R. S/HORA EXTRA 50%', f" ", f"{funcionario.dsr_s_hora_extra_50}", ' '],
        ['ADIC. PERICULOSIDADE', ' ', f"{funcionario.adic_periculosidade}", ' '],
        ['ADICIONAL NOTURNO', ' ', f"{funcionario.adicional_noturno}", ' '],
        ['D.S.R. S/ADICIONAL', ' ', f"{funcionario.dsr_s_adicional}", ' '],
        ['ADICIONAL DE FUNÇÃO 25%', ' ', f"{funcionario.adicional_de_funcao_25}", ' '],
        ['SALARIO FAMILIA', ' ', f"{funcionario.salario_familia}", ' '],
        ['FALTA ABONADA-PONTO ELETR.', ' ', f"{funcionario.falta_abonada_efeito_visualizacao}", ' '],
        ['LICENÇA GESTANTE (LEI 14.151)', ' ', f"{funcionario.licenca_remunerada_gestante}", ' '],
        ['ATESTADO HORISTAS', ' ', f"{funcionario.atestado_horistas}", ' '],
        ['SAL. MATERNIDADE', ' ', f"{funcionario.salario_maternidade}", ' '],
        ['AUX. DOENÇA / ACID. TRABALHO (15 DIAS)', ' ', f"{funcionario.aux_doenca_15_dias} / {funcionario.acidente_de_trabalho_15_dias}", ' '],
        ['VERBAS RESCISÓRIAS (Art 7º CF)', ' ', f"{funcionario.verbas_rescisorias}", ' '],
        ['FERIAS', ' ', f"{funcionario.ferias}", ' '],
        ['1/3 FERIAS', ' ', f"{funcionario.um_terco_ferias}", ' '],
        ['13º SALARIO INDENIZADO E ADICIONAIS', ' ', f"{funcionario.decimo_terceiro_salario_indenizado_e_adicionais_considerar}", ' '],
        ['ARREDONDAMENTO', ' ', f"{funcionario.arredondamento}", ' '],
        ['REEMBOLSO EXAME MEDICO/EPI/UNIF', ' ', f"{funcionario.dev_desc_exame_medico_epi_unif}", ' '],
        ['DIF. VR / VA  - DIF. VALE TRANSPORTE', ' ', f"{funcionario.dif_vale_transporte}", ' '],
        ['SALDO NEGATIVO', ' ', f"{funcionario.saldo_negativo_verba_nao_repassada}", ' '],
        ['DESC. FALTAS (DIAS+ATRASOS) E HORAS IND.', f"{funcionario.qtde_dias_e_hs_desconto}", ' ', f"{funcionario.desc_faltas_dias_atrasos_e_horas_indevidas}"],
        ['DESC. D.S.R. S/FALTAS (DIAS)', ' ', ' ', f"{funcionario.desc_dsr_s_faltas_dias}"],
        ['FALTAS ABONADAS', ' ', ' ', f"{funcionario.falta_abonada_efeito_visualizacao}"],
        ['DESC. ARREDONDAMENTO', ' ', ' ', f"{funcionario.desc_arredondamento}"],
        ['DESC. AVISO', ' ', ' ', f"{funcionario.desc_aviso}"],
        ['DESC. I.N.S.S./DESC. I.R.R.F', ' ', ' ', f"{funcionario.desc_inss_desc_irrf}"],
        ['DESC. I.N.S.S. S/13º SALARIO – INSS (Férias)', ' ', ' ', f"{funcionario.desc_inss_s_13_salario}"],
        ['SEGURO VIDA', ' ', f" ", f"{funcionario.seguro_vida}"],
        ['DESC. ASSIST. ODONTOLOGICA', ' ', ' ', f"{funcionario.desc_assist_odontologica}"],
        ['DESC. VALE REFEICAO NAO UTILIZADO', ' ', ' ', f"{funcionario.desc_vale_refeicao_nao_utilizado}"],
        ['DESC. VR/VA', ' ', ' ', f"{funcionario.desc_vr_va}"],
        ['DESC UNIFORME / EPI', ' ', ' ', f"{funcionario.desc_uniforme_epi_div_sind_judic_adiant_mater}"],
        ['DESC. VALE-TRANSPORTE NAO UTILIZADO', ' ', ' ', f"{funcionario.desc_vale_transporte_nao_utilizado}"],
        ['DESC. VALE-TRANSPORTE', ' ', ' ', f"{funcionario.desc_vale_transporte}"],
        ['DESC. SALDO NEGATIVO', ' ', ' ', f"{funcionario.desc_saldo_negativo}"],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' '],



    ]



    table = Table(data)

    # Definir a largura das colunas
    table._argW[0], table._argW[1], table._argW[2], table._argW[3] = 265, 95, 95, 95

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),  #Espaçemnto da primeira linha.
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LINEABOVE', (0, 1), (-1, 1), 1, colors.black),  # Adicionado
    ]))


    table.wrapOn(p, letter[0], letter[1])
    table_x = (letter[0] - table_width) / 2
    table_y = rect_y - rect_height + 120  # Subtrair 2 para diminuir ainda mais o espaço entre a tabela e o retângulo

    table.drawOn(p, table_x, table_y)  #


########################################################################################################
#  QUADRO FINAL DO CONTRA CHEQUE.
########################################################################################################

#################################
# QUADRADO GRANDE
#################################

    # Defina a largura da tabela
    table_width = 550
    # Desenhar um retângulo com informações do funcionário acima da tabela
    rect_x = (letter[0] - table_width) / 2
    # Aqui mexe na altura de onde fica na pagina.
    rect_y = -714
    # Altura do retangulo
    rect_height = 76
    p.roundRect(rect_x, rect_y + 750, table_width, rect_height, 1, stroke=1, fill=0)

#################################
# QUADRADO DE BAIXO PARA ASSINATURA
#################################

    table_width2 = 550
    # Desenhar um retângulo com informações do funcionário acima da tabela
    rect_x2 = (letter[0] - table_width) / 2
    # Aqui mexe na altura de onde fica na pagina.
    rect_y2 = -714
    # Altura do retangulo
    rect_height2 = 40
    p.roundRect(rect_x2, rect_y2 + 750, table_width2, rect_height2, 1, stroke=1, fill=0)

#################################
# QUADRADO GRANDE PARA A DIREITA
#################################

    table_width3 = 275
    # Mexe onde ele fica visando lado
    rect_x3 = 306
    # Aqui mexe na altura de onde fica na pagina.
    rect_y3 = -714
    # Altura do retangulo
    rect_height3 = 76
    p.roundRect(rect_x3, rect_y3 + 750, table_width3, rect_height3, 0, stroke=1, fill=0)

#################################
# LINHA NA DIREITA GRANDE PARA A DIREITA
#################################


#################################
# LINHA NA DIREITA GRANDE PARA A DIREITA
#################################

    table_width3 = 137.5
    # Mexe onde ele fica visando lado
    rect_x3 = 306
    # Aqui mexe na altura de onde fica na pagina.
    rect_y3 = -674
    # Altura do retangulo
    rect_height3 = 36
    p.roundRect(rect_x3, rect_y3 + 750, table_width3, rect_height3, 0, stroke=1, fill=0)

########################################################################################################
    p.drawString(rect_x + 300 + 10, rect_y + 750 + 65, f"Total Vencimentos:")
    p.drawString(rect_x + 300 + 20, rect_y + 750 + 50, f"R$ {funcionario.vencimentos}")
    p.drawString(rect_x + 445 + 10, rect_y + 750 + 65, f"Total Descontos:")
    p.drawString(rect_x + 445 + 20, rect_y + 750 + 50, f"R$ {funcionario.descontos}")
    p.drawString(rect_x + 350, rect_y + 750 + 20, f"Valor Líquido ==== R$ {funcionario.liquido}")
    p.drawString(rect_x + 25, rect_y + 750 + 22, f"__________________________________")
    p.drawString(rect_x + 25, rect_y + 750 + 10, f"Declaro ter recebido a importância líquida discriminada neste recibo")

    p.setFont("Helvetica", 10)
    p.drawString(rect_x + 25, rect_y + 750 + 25, f"{funcionario.nome}")

    # Finalizar a segunda página e começa a 3°.
    p.showPage()












    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'{funcionario.comp} - {funcionario.codigo_fc} - {funcionario.nome}.pdf')

