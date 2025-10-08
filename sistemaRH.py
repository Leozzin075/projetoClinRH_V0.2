from funcionario import Funcionario
from medico import Medico
from enfermeiro import Enfermeiro
from funcionarioAdmin import FuncionarioAdmin

class SistemaRH:
    def __init__(self):
        self.funcionarios = []

    def adicionarFuncionario(self, funcionario):
        self.funcionarios.append(funcionario)
        print(f"O funcionario {funcionario.nome} foi adicionado com sucesso!")

    def buscarPorMatricula(self, matricula):
        for funcionario in self.funcionarios:
            if funcionario.matricula == matricula:
                return funcionario
        return None