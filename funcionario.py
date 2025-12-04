import datetime
from database import db

class Funcionario(db.Model):
    __tablename__ = 'funcionarios' # Nome da tabela

    # --- COLUNAS DO BANCO ---
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    salario_base = db.Column(db.Float, nullable=False)
    
    # Status (agora salvos no banco)
    esta_ativo = db.Column(db.Boolean, default=True)
    em_ferias = db.Column(db.Boolean, default=False)

    # Coluna mágica para o Polimorfismo (diz se é medico, enfermeiro...)
    tipo_func = db.Column(db.String(50))

    # Configuração do SQLAlchemy para Herança
    __mapper_args__ = {
        'polymorphic_identity': 'funcionario',
        'polymorphic_on': tipo_func
    }

    # --- SEU CONSTRUTOR ORIGINAL (ADAPTADO) ---
    def __init__(self, matricula, nome, cpf, salario_base):
        self.matricula = matricula
        self.nome = nome
        self.cpf = cpf
        self.salario_base = salario_base
        self.esta_ativo = True
        self.em_ferias = False
        # self.registroDePonto não é mais uma lista, será uma relação com outra tabela

    # --- SEUS MÉTODOS ORIGINAIS ---
    def _pegarTimeAtual_(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # (Nota: registrarEntrada/Saida vão mudar um pouco no futuro para salvar na tabela de Ponto, 
    # mas por enquanto deixamos a lógica visual aqui)
    def registrarEntrada(self):
        timestamp_atual = self._pegarTimeAtual_()
        print(f"Sua entrada foi registrada: {self.nome} no horario:{timestamp_atual}")

    def registrarSaida(self):
        timestamp_atual = self._pegarTimeAtual_()
        print(f"Sua saida foi registrada: {self.nome} no horario:{timestamp_atual}")

    def exibirDados(self):
        print (f"Matricula: {self.matricula}")
        print(f"Nome: {self.nome}")
        print(f"CPF: {self.cpf}")
        print(f"Salario base: {self.salario_base:.2f}") # Ajustado para snake_case do banco
        
        if not self.esta_ativo:
            print("Status = Inativo")
        elif self.em_ferias:
            print("Status: Em Ferias")
        else:
            print("Status: Ativo")
    
    # Método base para o cálculo
    def calcularSalario(self, horas_extras=0):
        return self.salario_base