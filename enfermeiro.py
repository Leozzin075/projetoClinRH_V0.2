from funcionario import Funcionario

class Enfermeiro(Funcionario):
    def __init__(self, matricula, nome, cpf, salarioBase, coren, adcionalNoturno, turno):
        super().__init__(matricula, nome, cpf, salarioBase)
        self.coren = coren
        self.adicionalNoturno = adcionalNoturno
        self.turno = turno.lower()

    def exibirDados(self):
        super().exibirDados()
        print(f"COREN: {self.coren}")
        print(f"Turno: {self.turno}")
        if self.turno == "noturno":
            print(f"Adicional Noturno: {self.adicional_noturno * 100:.0f}%")
        
    def calcularSalario(self, horasExtras):
        if self.turno == "noturno":
            acrescimo = self.salario_base * self.adicional_noturno
            salarioReal = self.salario_base + acrescimo
            return salarioReal
        else:
            return self.salarioBase