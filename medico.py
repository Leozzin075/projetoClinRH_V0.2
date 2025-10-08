from funcionario import Funcionario

class Medico(Funcionario):
    def __init__(self, matricula, nome, cpf, salarioBase, crm, especialidade, valorHoraExtra):
        super().__init__(matricula, nome, cpf, salarioBase)
        self.crm = crm
        self.especialidade = especialidade
        self.valorHoraExtra = valorHoraExtra


    def exibirDados(self):
        super().exibirDados()
        print(f"CRM: {self.crm}")
        print(f"Especialidade: {self.especialidade}")
        print(f"Valor da hora extra: {self.valorHoraExtra}")

    def calcularSalario(self, horasExtras):
        salarioReal = self.salarioBase + (horasExtras * self.valorHoraExtra)
        return salarioReal

    
