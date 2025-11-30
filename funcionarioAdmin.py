from database import db
from funcionario import Funcionario

class FuncionarioAdmin(Funcionario):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), primary_key=True)
    cargo = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, matricula, nome, cpf, salario_base, cargo):
        super().__init__(matricula, nome, cpf, salario_base)
        self.cargo = cargo

    def exibirDados(self):
        super().exibirDados()
        print(f"Seu cargo e: {self.cargo}")

    def calcularSalario(self, horas_extras=0):
        return self.salario_base