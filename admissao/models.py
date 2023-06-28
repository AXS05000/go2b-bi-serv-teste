from django.db import models


class ContractTemplate(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='contract_templates/')

    def __str__(self):
        return f'{self.name}'
    
class ClienteGI(models.Model):
    nome = models.CharField(max_length=250)
    cod_cliente = models.IntegerField()
    responsavel_filial = models.CharField(max_length=250)
    telefone_filial = models.CharField(max_length=60)
       
    def __str__(self):
        return f'{self.nome}'
    
    def get_field_values(self):
        return {
            '{nome_cliente}': self.nome,
            '{cod_cliente}': self.cod_cliente,
            '{responsavel_filial}': str(self.responsavel_filial),
            '{telefone_filial}': self.telefone_filial,
        }
    
    
class Departamento(models.Model):
    nome_departamento = models.CharField(max_length=250)
    endereco_local = models.CharField(max_length=250)
    id_dep_fc = models.CharField(max_length=250)
    cliente_gi_dep = models.ForeignKey(
        ClienteGI, on_delete=models.SET_NULL, null=True, blank=True
    )
    def __str__(self):
        return f'{self.cliente_gi_dep} - {self.nome_departamento}'
    
    def get_field_values(self):
        return {
            '{nome_departamento}': self.nome_departamento,
            '{endereco_local}': self.endereco_local,
            '{id_dep_fc}': self.id_dep_fc,
        }
    
class Turno(models.Model):
    nome = models.CharField(max_length=250)
    jornada_de_semana = models.CharField(max_length=250)
    periodo_semanal = models.CharField(max_length=250)
    horas_semana = models.CharField(max_length=250)
    jornada_fim_semana = models.CharField(max_length=250)
    periodo_fim_semana = models.CharField(max_length=250)
    horas_fim_semana = models.CharField(max_length=250)
    departamento = models.ForeignKey(
        Departamento, on_delete=models.SET_NULL, null=True, blank=True
    )


    def __str__(self):
        return f'{self.nome}'
    
    def get_field_values(self):
        return {
            '{nome_turno}': self.nome,
            '{jornada_de_semana}': self.jornada_de_semana,
            '{periodo_semanal}': self.periodo_semanal,
            '{horas_semana}': self.horas_semana,
            '{jornada_fim_semana}': self.jornada_fim_semana,
            '{periodo_fim_semana}': self.periodo_fim_semana,
            '{horas_fim_semana}': self.horas_fim_semana,
        }   


class Base(models.Model):
    cargo = models.CharField(max_length=250)
    cbo = models.CharField(max_length=250)
    cliente = models.ForeignKey(
        ClienteGI, on_delete=models.SET_NULL, null=True, blank=True
    )
    salario = models.DecimalField(
        'Salario Hora', max_digits=18, decimal_places=2)
    salario_mes = models.DecimalField(
        'Salario Mensal', max_digits=18, decimal_places=2)
    vt = models.DecimalField(
        'VT', max_digits=18, decimal_places=2)
    vr = models.DecimalField(
        'VR', max_digits=18, decimal_places=2)
    cesta = models.DecimalField(
        'CESTA', max_digits=18, decimal_places=2)
    sindicato = models.CharField(max_length=250)

       
    def __str__(self):
        return f'{self.cargo} - {self.cliente} - {self.salario_mes}'
    
    def get_field_values(self):
        return {
            '{nome_cargo}': self.cargo,
            '{cbo}': self.cbo,
            '{nome_cliente}': self.cliente.nome if self.cliente else '',
            '{cod_cliente}': str(self.cliente.cod_cliente) if self.cliente else '',
            '{salario}': str(self.salario),
            '{salario_mes}': str(self.salario_mes),
            '{vt}': str(self.vt),
            '{vr}': str(self.vr),
            '{cesta}': str(self.cesta),
            '{sindicato}': self.sindicato,
        }
    



ORGANIZATION_CHOICES = [
    ('SSP', 'Secretaria de Segurança Pública'),
    ('PM', 'Polícia Militar'),
    ('PC', 'Polícia Civil'),
    ('FGTS', 'Fundo de Garantia do Tempo de Serviço'),
    ('IFP', 'Instituto Félix Pacheco'),
    ('IPF', 'Instituto Pereira Faustino'),
    ('IMESP', 'Instituto de Identificação Ricardo Gumbleton Daunt'),
    ('ITI', 'Instituto de Identificação Tobias de Aguiar'),
    ('DETRAN', 'Departamento de Trânsito'),
    ('CTPS', 'Carteira de Trabalho e Previdência Social'),
    ('FIDENE', 'Fundação de Integração e Desenvolvimento do Ensino do Noroeste do Estado'),
    ('ME', 'Ministério do Exército'),
    ('MEX', 'Ministério do Exército'),
    ('MTE', 'Ministério do Trabalho e Emprego'),
    ('PF', 'Polícia Federal'),
    ('POM', 'Polícia Militar'),
    ('SD/SG', 'Serviço Discreto / Secretaria Geral'),
    ('SNJ', 'Secretaria Nacional de Justiça'),
    ('SSPDS', 'Secretaria de Segurança Pública e Defesa da Sociedade'),
    ('STF', 'Supremo Tribunal Federal'),
    ('STM', 'Superior Tribunal Militar')
]


STATE_CHOICES = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
]


class Collaborator(models.Model):
    name = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14)
    admission_date = models.DateField(null=True, blank=True)
    rg = models.CharField(max_length=20)
    orgao_emissor_rg = models.CharField(max_length=150, choices=ORGANIZATION_CHOICES)
    uf_rg = models.CharField(max_length=2, choices=STATE_CHOICES)
    data_emissao_rg = models.DateField()
    n_ctps = models.CharField(max_length=7)
    serie = models.CharField(max_length=5)
    uf_ctps = models.CharField(max_length=2, choices=STATE_CHOICES)
    data_emissao_ctps = models.DateField()
    endereco = models.CharField(max_length=250)
    cep = models.CharField(max_length=9)
    celular = models.CharField(max_length=13)
    email = models.CharField(max_length=250)
    cargo = models.ForeignKey(
        Base, on_delete=models.SET_NULL, null=True, blank=True
    )
    turno = models.ForeignKey(
        Turno, on_delete=models.SET_NULL, null=True, blank=True
    )
    departamento = models.ForeignKey(
        Departamento, on_delete=models.SET_NULL, null=True, blank=True
    )
    cliente_gi = models.ForeignKey(
        ClienteGI, on_delete=models.SET_NULL, null=True, blank=True
    )
       
    def __str__(self):
        return f'{self.name}'
    
    def get_field_values(self):
        return {
            '{nome}': self.name,
            '{cpf}': self.cpf,
            '{admissão}': self.admission_date.strftime('%d/%m/%Y') if self.admission_date else '',
            '{rg}': self.rg,
            '{orgao_emissor_rg}': self.orgao_emissor_rg,
            '{uf_rg}': self.uf_rg,
            '{data_emissao_rg}': self.data_emissao_rg.strftime('%d/%m/%Y') if self.data_emissao_rg else '',
            '{n_ctps}': self.n_ctps,
            '{serie}': self.serie,
            '{uf_ctps}': self.uf_ctps,
            '{data_emissao_ctps}': self.data_emissao_ctps.strftime('%d/%m/%Y') if self.data_emissao_ctps else '',
            '{endereco}': self.endereco,
            '{cep}': self.cep,
            '{celular}': self.celular,
            '{email}': self.email,
        }
    


""" ##################################################################################################### """
