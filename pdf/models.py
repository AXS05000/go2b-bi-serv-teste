from django.db import models


class Funcionario(models.Model):
    comp = models.IntegerField('COMPET.')
    cod_cliente = models.CharField('COD CLIENTE', max_length=100)
    cliente = models.CharField('CLIENTE', max_length=100)
    codigo = models.CharField('CODIGO', max_length=100)
    codigo_fc = models.IntegerField('CODIGO FC', unique=False)
    cto = models.CharField('CONTRATO', max_length=100)
    cpf = models.CharField('CPF', max_length=100)
    nome = models.CharField('Nome', max_length=100)
    cargo = models.CharField('Cargo', max_length=100)
    adm = models.CharField('ADM', max_length=100)
    dem_compt = models.CharField('DEM (COMPT)', max_length=100)
    valid_desl = models.CharField('VALID. DESL', max_length=100)
    tipo = models.CharField('TIPO', max_length=100)
    qtde_hs_normais = models.CharField('Qtde HS NORMAIS', max_length=100)
    horas_normais = models.CharField('HORAS NORMAIS', max_length=100)
    dissidio_retroativo = models.CharField('DISSÍDIO-RETROATIVO', max_length=100)
    dsr_s_horas_normal = models.CharField('D.S.R. S/HORAS NORMAL', max_length=100)
    qtde_hs_not = models.CharField('Qtde Hs Not', max_length=100)
    adicional_noturno = models.CharField('ADICIONAL NOTURNO', max_length=100)
    dsr_s_adicional = models.CharField('D.S.R. S/ADICIONAL', max_length=100)
    qtde_he_50 = models.CharField('Qtde HE 50%', max_length=100)
    hora_extra_50 = models.CharField('HORA EXTRA 50%', max_length=100)
    qtde_he_50_not = models.CharField('Qtde HE 50 NOT', max_length=100)
    hora_extra_50_noturno = models.CharField('HORA EXTRA 50% NOTURNO', max_length=100)
    dsr_s_hora_extra_50 = models.CharField('D.S.R. S/HORA EXTRA 50%', max_length=100)
    qtde_he_100 = models.CharField('Qtde HE 100%', max_length=100)
    hora_extra_100 = models.CharField('HORA EXTRA 100%', max_length=100)
    qtde_he_100_not = models.CharField('Qtde HE 100% NOT', max_length=100)
    hora_extra_100_noturno = models.CharField('HORA EXTRA 100% NOTURNO', max_length=100)
    dsr_s_hora_extra_100 = models.CharField('D.S.R. S/HORA EXTRA 100%', max_length=100)
    adic_periculosidade = models.CharField('ADIC. PERICULOSIDADE', max_length=100)
    adicional_de_funcao_25 = models.CharField('ADICIONAL DE FUNÇÃO 25%', max_length=100)
    adicional_de_atividade_30 = models.CharField('ADICIONAL DE ATIVIDADE 30% (CARTEIRO)', max_length=100)
    adicional_final_de_semana_15 = models.CharField('ADICIONAL FINAL DE SEMANA 15%', max_length=100)
    salario_familia = models.CharField('SALARIO FAMILIA',    max_length=100)
    falta_abonada_ponto_eletr = models.CharField('FALTA ABONADA-PONTO ELETR.', max_length=100)
    qtde_atestado_horistas = models.CharField('QTDE ATESTADO HORISTAS', max_length=100)
    atestado_horistas = models.CharField('ATESTADO HORISTAS', max_length=100)
    licenca_remunerada_gestante = models.CharField('LICENÇA REMUNERADA GESTANTE (LEI 14.151) / (AJUDA COMPENSATÓRIA)', max_length=100)
    salario_maternidade = models.CharField('SALÁRIO MATERNIDADE', max_length=100)
    aux_doenca_15_dias = models.CharField('AUX. DOENÇA (15 DIAS)/AUS. LEGAIS', max_length=100)
    acidente_de_trabalho_15_dias = models.CharField('ACIDENTE DE TRABALHO (15 DIAS)', max_length=100)
    acidente_de_trabalho_fgts = models.CharField('ACIDENTE DE TRABALHO (F.G.T.S.)', max_length=100)
    fgts_pago_rct = models.CharField('F.G.T.S. PAGO RCT', max_length=100)
    fgts_multa_40 = models.CharField('F.G.T.S. MULTA 40%', max_length=100)
    fgts_s_13_salario = models.CharField('F.G.T.S. S/13º SALARIO', max_length=100)
    fgts_s_aviso_previo = models.CharField('F.G.T.S. S/AVISO PREVIO (Rescisao)', max_length=100)
    verbas_rescisorias = models.CharField('VERBAS RESCISÓRIAS (Art 7º CF) - Itens 4.4.A/4.4.D + Médias Lei 12506', max_length=100)
    saldo_negativo_verba_nao_repassada = models.CharField('SALDO NEGATIVO - VERBA NÃO REPASSADA', max_length=100)
    ferias = models.CharField('FERIAS', max_length=100)
    um_terco_ferias = models.CharField('1/3 FERIAS', max_length=100)
    decimo_terceiro_salario_indenizado_e_adicionais_considerar = models.CharField('13º SALARIO INDENIZADO E ADICIONAIS (Considerar)', max_length=100)
    decimo_terceiro_salario_indenizado_e_adicionais = models.CharField('13º SALARIO INDENIZADO E ADICIONAIS', max_length=100)
    antecip_13 = models.CharField('ANTENCIP/ 13', max_length=100)
    dev_desc_exame_medico_epi_unif = models.CharField('DEV. DESC EXAME MEDICO - EPI-UNIF', max_length=100)
    arredondamento = models.CharField('ARREDONDAMENTO', max_length=100)
    dif_vale_transporte = models.CharField('DIF. VALE-TRANSPORTE', max_length=100)
    dif_vale_refeicao = models.CharField('DIF. VALE REFEICAO', max_length=100)
    vencimentos = models.CharField('VENCIMENTOS', max_length=100)
    qtde_dias_e_hs_desconto = models.CharField('Qtde dias e HS Desconto', max_length=100)
    desc_faltas_dias_atrasos_e_horas_indevidas = models.CharField('DESC. FALTAS (DIAS+ATRASOS) E HORAS INDEVIDAS', max_length=100)
    desc_dsr_s_faltas_dias = models.CharField('DESC. D.S.R. S/FALTAS (DIAS)', max_length=100)
    falta_abonada_efeito_visualizacao = models.CharField('FALTA ABONADA - Efeito Visualização', max_length=100)
    desc_saldo_negativo = models.CharField('DESC. SALDO NEGATIVO', max_length=100)
    desc_arredondamento = models.CharField('DESC. ARREDONDAMENTO', max_length=100)
    desc_aviso = models.CharField('DESC AVISO', max_length=100)
    desc_antecipacao_13_salario = models.CharField('DESC. ANTECIPACAO 13º SALARIO', max_length=100)
    desc_inss_desc_irrf = models.CharField('DESC. I.N.S.S./DESC. I.R.R.F.', max_length=100)
    desc_inss_s_13_salario = models.CharField('DESC. I.N.S.S. S/13º SALARIO', max_length=100)
    desc_inss_ferias = models.CharField('DESC. I.N.S.S. (Ferias)', max_length=100)
    desc_acidente_de_trabalho_fgts = models.CharField('DESC. ACIDENTE DE TRABALHO (F.G.T.S.)', max_length=100)
    aux_doenca_15_dias_aus_legais = models.CharField('AUX. DOENÇA (15 DIAS)/AUS. LEGAIS', max_length=100)
    desc_fgts_deposito_rescisao_grfc = models.CharField('DESC. F.G.T.S. DEPOSITO RESCISAO - G.R.F.C.', max_length=100)
    desc_pensao_alimenticia = models.CharField('DESC. PENSAO ALIMENTICIA(não é padrão)', max_length=100)
    desc_uniforme_epi_div_sind_judic_adiant_mater = models.CharField('DESC UNIFORME / EPI (DIV: SIND./JUDIC/ADIANT/MATER', max_length=100)
    seguro_vida = models.CharField('SEGURO VIDA', max_length=100)
    desc_assist_odontologica = models.CharField('DESC. ASSIST. ODONTOLOGICA', max_length=100)
    desc_vale_transporte_nao_utilizado = models.CharField('DESC. VALE-TRANSPORTE NAO UTILIZADO', max_length=100)
    desc_vale_transporte = models.CharField('DESC. VALE-TRANSPORTE', max_length=100)
    desc_vr_va = models.CharField('DESC. VR/VA', max_length=100)
    desc_vale_refeicao_nao_utilizado = models.CharField('DESC. VALE REFEICAO NAO UTILIZADO', max_length=100)
    descontos = models.CharField('DESCONTOS', max_length=100)
    liquido = models.CharField('LIQUIDO', max_length=100)
    liquido_1 = models.CharField('LIQUIDO 1', max_length=100)
    aut_1 = models.CharField('AUT 1', max_length=100)
    liquido_2 = models.CharField('LIQUIDO 2', max_length=100)
    aut_2 = models.CharField('AUT 2', max_length=100)
    liquido_3 = models.CharField('LIQUIDO 3', max_length=100)
    aut_3 = models.CharField('AUT 3', max_length=100)
    liquido_4 = models.CharField('LIQUIDO 4', max_length=100)
    aut_4 = models.CharField('AUT 4', max_length=100)
    liquido_5 = models.CharField('LIQUIDO 5', max_length=100)
    aut_5 = models.CharField('AUT 5', max_length=100)
    data_1 = models.CharField('DATA 1', max_length=100)
    data_2 = models.CharField('DATA 2', max_length=100)
    data_3 = models.CharField('DATA 3', max_length=100)
    data_4 = models.CharField('DATA 4', max_length=100)
    data_5 = models.CharField('DATA 5', max_length=100)
    qtde_dsr_feriado = models.CharField('QTDE D.S.R FERIADO', max_length=100)
    dsr_feriado = models.CharField('D.S.R. FERIADO', max_length=100)



    class Meta:
        ordering = ['comp', 'codigo_fc']

    def __str__(self):
        return f'{self.comp} - {self.codigo_fc} - {self.nome}'
    


   


class Beneficios_Mala(models.Model):
    comp = models.IntegerField('COMPET.')
    codigo = models.CharField('CODIGO', max_length=100)
    codigo_fc = models.IntegerField('CODIGO FC', unique=False)
    aut = models.CharField('Aut', max_length=100)
    data_inicio = models.CharField('Data Inicio', max_length=100)
    data_fim = models.CharField('Data Fim', max_length=100)
    dias_calculados = models.CharField('Dias Calculados', max_length=100)
    tipo_de_beneficio = models.CharField('Tipo de Beneficio', max_length=100)
    valor_pago = models.CharField('Valor Pago', max_length=100)
    data_de_pagamento = models.CharField('Data de Pagamento', max_length=100)


    class Meta:
        ordering = ['comp', 'codigo_fc']

    def __str__(self):
        return f'{self.comp} - {self.codigo_fc}'
    


class Folha_de_Ponto(models.Model):
    comp = models.IntegerField('COMPET.')
    codigo = models.CharField('CODIGO', max_length=100)
    codigo_fc = models.IntegerField('CODIGO FC', unique=False)
    total_de_horas = models.CharField(max_length=100)
    hs_normais = models.CharField(max_length=100)
    hs_noturnas = models.CharField(max_length=100)
    he_50 = models.CharField(max_length=100)
    he_100 = models.CharField(max_length=100)
    periodo_apontamento = models.CharField(max_length=100)

    # Cria um campo para cada dia do mês (1 a 31), para cada tipo (M, H, D)
    for i in range(21, 32):
        for t in ('m', 'h', 'd'):
            vars()[f'{i}_{t}'] = models.CharField(max_length=100)

    # Cria um campo para cada dia do mês (1 a 31), para cada tipo (M, H, D) com S no final
    for i in range(1, 32):
        for t in ('m', 'h', 'd'):
            vars()[f'{i}_{t}_s'] = models.CharField(max_length=100)

    class Meta:
        ordering = ['comp', 'codigo_fc']

    def __str__(self):
        return f'{self.comp} - {self.codigo_fc}'
    

class Arquivo(models.Model):
    pdf = models.FileField(upload_to='pdfs/')
    competencia = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.pdf}'




