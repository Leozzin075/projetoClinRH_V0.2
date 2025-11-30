from database import db
from funcionario import Funcionario

class Medico(Funcionario):
    __tablename__ = 'medicos' # Tabela separada

    # Conecta com o ID da tabela pai
    id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), primary_key=True)
    
    # Colunas específicas
    crm = db.Column(db.String(20))
    especialidade = db.Column(db.String(50))
    valor_hora_extra = db.Column(db.Float)

    # Identidade
    __mapper_args__ = {
        'polymorphic_identity': 'medico',
    }

    # --- CONSTRUTOR ORIGINAL ---
    def __init__(self, matricula, nome, cpf, salario_base, crm, especialidade, valor_hora_extra):
        super().__init__(matricula, nome, cpf, salario_base)
        self.crm = crm
        self.especialidade = especialidade
        self.valor_hora_extra = valor_hora_extra

    # --- MÉTODOS ORIGINAIS ---
    def exibirDados(self):
        super().exibirDados()
        print(f"CRM: {self.crm}")
        print(f"Especialidade: {self.especialidade}")
        print(f"Valor da hora extra: {self.valor_hora_extra}")

    def calcularSalario(self, horas_extras=0):
        # Lógica mantida, só ajustando nomes para snake_case do banco
        acrescimo = float(horas_extras) * (self.valor_hora_extra or 0)
        return self.salario_base + acrescimo