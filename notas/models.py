from decimal import ROUND_DOWN, Decimal

from django.db import models

from .formulas import truncate_decimal

# Create your models here.

class BaseInfoContratos(models.Model):
    cod_cliente = models.CharField('Cod. Cliente', max_length=5)
    contrato = models.CharField('Contrato', max_length=65)
    cargo = models.CharField('Cargo', max_length=65)
    valor_hora = models.DecimalField(
        'Valor Hora', max_digits=18, decimal_places=2)
    data_inicio_cto = models.DateField(
        'Data Inicio do Contrato no Sistema', max_length=10)
    contrato_ativo = models.BooleanField('Contrato Ativo')

    class Meta:
        ordering = ['cod_cliente', 'contrato', 'cargo']

    def __str__(self):
        return f'{self.cod_cliente} - {self.contrato} - {self.cargo}'
    



class Competencias(models.Model):
    competencia = models.CharField('Competência', max_length=30)

    def __str__(self):
        return self.competencia






GENDER_CHOICES_2 = (
    ('LOG', 'LOG'),
    ('MOT', 'MOT'),
    ('DISTRIBUIÇÃO', 'DISTRIBUIÇÃO'),
    ('PRIVADOS', 'PRIVADOS'),
    ('OUTROS', 'OUTROS'),
)




class BaseCNPJ(models.Model):
    cnpj = models.CharField('CNPJ', max_length=18)
    razao = models.CharField('Razão Social', max_length=100)
    avenida_rua = models.CharField('Avenida/Rua', max_length=450)
    endereco = models.CharField('Endereço', max_length=450)
    numero = models.CharField('Número', max_length=20, null=True, blank=True)
    complemento = models.CharField(
        'Complemento', max_length=90, null=True, blank=True)
    bairro = models.CharField('Bairro', max_length=80)
    municipio = models.CharField('Municipio', max_length=60)
    uf = models.CharField('UF', max_length=2)
    cep = models.CharField('Cep', max_length=8)
    nome_cliente = models.CharField('Nome Cliente', max_length=50)
    tipo_de_servico = models.CharField('Tipo de Serviço', max_length=5)
    iss = models.DecimalField('ISS', max_digits=4, decimal_places=4)
    unidade = models.CharField('Unidade', max_length=55)
    mcu = models.CharField('MCU', max_length=15)
    tipo_de_cliente = models.CharField(
        'Tipo de Cliente', max_length=150, choices=GENDER_CHOICES_2)
    tx_adm = models.DecimalField(
        'taxa Adm', max_digits=4, decimal_places=4)


    class Meta:
        ordering = ['uf', 'nome_cliente', 'unidade']

    def __str__(self):
        return self.uf + ' - ' + self.cnpj + ' - ' + self.nome_cliente + ' - ' + self.unidade


GENDER_CHOICES = (
    ('FATURAMENTO HORAS', 'FATURAMENTO HORAS'),
    ('FATURAMENTO FG', 'FATURAMENTO FG'),
    ('FATURAMENTO REPACTUAÇÃO E REQUILIBRIO', 'FATURAMENTO REPACTUAÇÃO E REQUILIBRIO'),
    ('FATURAMENTO OUTROS', 'FATURAMENTO OUTROS'),
)



class Notas(models.Model):

    data_de_criacao = models.DateField('Data de Criação', auto_now_add=True)
    data_de_modificacao = models.DateField(
        'Data de Modificação', auto_now=True)
    baseinfocontratos = models.ForeignKey(
        BaseInfoContratos, on_delete=models.SET_NULL, null=True, blank=True
    )
    nota_cancelada = models.BooleanField('Nota Cancelada?', default=False)
    competencia_nota = models.ForeignKey(
        Competencias, on_delete=models.SET_NULL, null=True
    )
    tipo_de_faturamento = models.CharField(
        'Tipo de Faturamento', max_length=150, choices=GENDER_CHOICES)
    quantidade_hora = models.DecimalField(
        'Quantidade de Horas', max_digits=10, decimal_places=4, null=True, blank=True)

    baseinfocontratos2 = models.ForeignKey(
        BaseInfoContratos, on_delete=models.SET_NULL, null=True, blank=True, related_name='cargo_2'
    )
    quantidade_hora2 = models.DecimalField(
        'Quantidade de Horas 2', max_digits=10, decimal_places=4, null=True, blank=True)

    baseinfocontratos3 = models.ForeignKey(
        BaseInfoContratos, on_delete=models.SET_NULL, null=True, blank=True, related_name='cargo_3'
    )
    quantidade_hora3 = models.DecimalField(
        'Quantidade de Horas 3', max_digits=10, decimal_places=4, null=True, blank=True)

    baseinfocontratos4 = models.ForeignKey(
        BaseInfoContratos, on_delete=models.SET_NULL, null=True, blank=True, related_name='cargo_4'
    )
    quantidade_hora4 = models.DecimalField(
        'Quantidade de Horas 4', max_digits=10, decimal_places=4, null=True, blank=True)

    baseinfocontratos5 = models.ForeignKey(
        BaseInfoContratos, on_delete=models.SET_NULL, null=True, blank=True, related_name='cargo_5'
    )
    quantidade_hora5 = models.DecimalField(
        'Quantidade de Horas 5', max_digits=10, decimal_places=4, null=True, blank=True)

    baseinfocontratos6 = models.ForeignKey(
        BaseInfoContratos, on_delete=models.SET_NULL, null=True, blank=True, related_name='cargo_6'
    )
    quantidade_hora6 = models.DecimalField(
        'Quantidade de Horas 6', max_digits=10, decimal_places=4, null=True, blank=True)

    baseinfocontratos7 = models.ForeignKey(
        BaseInfoContratos, on_delete=models.SET_NULL, null=True, blank=True, related_name='cargo_7'
    )
    quantidade_hora7 = models.DecimalField(
        'Quantidade de Horas 7', max_digits=10, decimal_places=4, null=True, blank=True)

    baseinfocontratos8 = models.ForeignKey(
        BaseInfoContratos, on_delete=models.SET_NULL, null=True, blank=True, related_name='cargo_8'
    )
    quantidade_hora8 = models.DecimalField(
        'Quantidade de Horas 8', max_digits=10, decimal_places=4, null=True, blank=True)

    cnpj_da_nota = models.ForeignKey(
        BaseCNPJ, on_delete=models.SET_NULL, null=True, blank=True, related_name='cnpj_da_nota'
    )

    texto_livre = models.CharField('Texto Livre', max_length=3500, null=True, blank=True)

    contrato_texto_livre = models.CharField('Contrato Texto Livre', max_length=9, null=True, blank=True)

    total_valor_outros = models.DecimalField(
        'Total Valor Outros', max_digits=10, decimal_places=4, null=True, blank=True)
    
        
    porcentagem_ans = models.DecimalField('Porcentagem ANS', max_digits=3, decimal_places=2, null=True, blank=True, error_messages={
        'max_digits': 'Certifique-se de que tenha digitado o valor correto de porcentagem na ANS'})

    competencia_nota_ans = models.ForeignKey(
        Competencias, on_delete=models.SET_NULL, null=True, blank=True, related_name='competencia_nota_ans'
    )

    def __str__(self):
        return self.tipo_de_faturamento

    @property
    def total_quantidade_de_horas(self):
        total = 0
        # Para baseinfocontratos sem número, ou seja, a primeira instância
        if self.baseinfocontratos and self.quantidade_hora:
            total += self.baseinfocontratos.valor_hora * self.quantidade_hora
        # Para baseinfocontratos2 até baseinfocontratos8
        for i in range(2, 9):
            quantidade_hora = getattr(self, f'quantidade_hora{i}', 0)
            baseinfocontratos = getattr(self, f'baseinfocontratos{i}', None)
            if quantidade_hora and baseinfocontratos:
                total += quantidade_hora * baseinfocontratos.valor_hora
        return int(total * 100)

    @property
    def total_a_faturar(self):
        total = Decimal('0.00')
        # Para baseinfocontratos sem número, ou seja, a primeira instância
        if self.baseinfocontratos and self.quantidade_hora:
            total += Decimal(str(self.baseinfocontratos.valor_hora)) * Decimal(str(self.quantidade_hora))
        # Para baseinfocontratos2 até baseinfocontratos8
        for i in range(2, 9):
            quantidade_hora = getattr(self, f'quantidade_hora{i}', 0)
            baseinfocontratos = getattr(self, f'baseinfocontratos{i}', None)
            if quantidade_hora and baseinfocontratos:
                total += Decimal(str(quantidade_hora)) * Decimal(str(baseinfocontratos.valor_hora))
        return truncate_decimal(total, 2)









class NumeradorLote(models.Model):
    valor = models.IntegerField(default=1)

class NotaFiscal2(models.Model):
    aliquota = models.FloatField(null=True, blank=True)
    cod_atividade = models.CharField(max_length=200,null=True, blank=True)
    cod_obra = models.CharField(max_length=200,null=True, blank=True)
    codigo_autenticidade = models.CharField(max_length=200,null=True, blank=True)
    data_cancelamento = models.DateField(null=True, blank=True)
    data_emissao = models.DateField(null=True, blank=True)
    data_recibo = models.DateField(null=True, blank=True)
    doc_tomador = models.CharField(max_length=200,null=True, blank=True)
    endereco_prestacao_servico = models.CharField(max_length=500,null=True, blank=True)
    link_nfe = models.URLField(null=True, blank=True)
    motivo_cancelamento = models.CharField(max_length=500,null=True, blank=True)
    nome_tomador = models.CharField(max_length=200,null=True, blank=True)
    nosso_numero = models.CharField(max_length=200,null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    numero_recibo = models.IntegerField(null=True, blank=True)
    substituicao_tributaria = models.BooleanField(null=True, blank=True)
    valor = models.FloatField(null=True, blank=True)
    valor_iss = models.FloatField(null=True, blank=True)
    valor_nfe = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.data_emissao} - {self.valor}- {self.nome_tomador}'