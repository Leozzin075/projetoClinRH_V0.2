from funcionario import Funcionario

class Enfermeiro(Funcionario):
    def __init__(self, matricula, nome, cpf, salarioBase, coren, adicionalNoturno, turno):
        super().__init__(matricula, nome, cpf, salarioBase)
        self.coren = coren
        self.adicionalNoturno = adicionalNoturno
        self.turno = turno.lower()

    def exibirDados(self):
        super().exibirDados()
        print(f"COREN: {self.coren}")
        print(f"Turno: {self.turno}")
        if self.turno == "noturno":
            print(f"Adicional Noturno: {self.adicionalNoturno * 100:.0f}%")
        
    def calcularSalario(self, horasExtras):
        if self.turno == "noturno":
            acrescimo = self.salarioBase * self.adicionalNoturno
            salarioReal = self.salarioBase + acrescimo
            return salarioReal
        else:
            return self.salarioBase