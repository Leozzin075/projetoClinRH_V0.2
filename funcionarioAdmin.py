from funcionario import Funcionario

class FuncionarioAdmin(Funcionario):
    def __init__(self, matricula, nome, cpf, salarioBase, cargo):
        super().__init__(matricula, nome, cpf, salarioBase)
        self.cargo = cargo

    def exibirDados(self):
        super().exibirDados()
        print(f"Seu cargo e: {self.cargo}")

    def calcularSalario(self, horasExtras):
        return self.salarioBase