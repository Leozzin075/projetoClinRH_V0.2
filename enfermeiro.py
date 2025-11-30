from database import db
from funcionario import Funcionario

class Enfermeiro(Funcionario):
    __tablename__ = 'enfermeiros'

    id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), primary_key=True)
    
    coren = db.Column(db.String(20))
    turno = db.Column(db.String(20))
    adicional_noturno = db.Column(db.Float)

    __mapper_args__ = {
        'polymorphic_identity': 'enfermeiro',
    }

    def __init__(self, matricula, nome, cpf, salario_base, coren, adicional_noturno, turno):
        super().__init__(matricula, nome, cpf, salario_base)
        self.coren = coren
        self.adicional_noturno = adicional_noturno
        self.turno = turno.lower()

    def exibirDados(self):
        super().exibirDados()
        print(f"COREN: {self.coren}")
        print(f"Turno: {self.turno}")
        if self.turno == "noturno":
            print(f"Adicional Noturno: {(self.adicional_noturno or 0) * 100:.0f}%")
        
    def calcularSalario(self, horas_extras=0):
        if self.turno == "noturno":
            acrescimo = self.salario_base * (self.adicional_noturno or 0)
            return self.salario_base + acrescimo
        else:
            return self.salario_base