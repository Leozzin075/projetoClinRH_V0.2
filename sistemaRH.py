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
    def listarFuncionarios(self):
        if not self.funcionarios:
            print("Nenhum funcionario cadastrado")
            return
        else:
            for funcionario in self.funcionarios:
                if funcionario.estaAtivo:
                    funcionario.exibirDados()
    def gerarFolhaDePagamento(self, mapaDeHoras):
        for funcionario in self.funcionarios:
            if funcionario.estaAtivo and not funcionario.estaDeFerias:
                horasExtras = mapaDeHoras.get(funcionario.matricula, 0)
                salarioDoMes = funcionario.calcularSalario(horasExtras)
                print(f"Pagamento do funcionario {funcionario.nome}: RS{salarioDoMes:.2f}")       
    def editarFuncionario(self, matricula, dadosParaAtualizar):
            funcionario = self.buscarPorMatricula(matricula)
            if not funcionario:
                print(f"Erro: Matrícula {matricula} não encontrada.")
                return
            for chave, valor in dadosParaAtualizar.items():
                setattr(funcionario, chave, valor)                
                print(f"LOG: {chave} do funcionário {matricula} atualizado para {valor}.") # Um log é bom
            print(f"Dados do funcionário {funcionario.nome} atualizados com sucesso.")    
    def demitirFuncionario(self, matricula):
        funcionario = self.buscarPorMatricula(matricula)
        if funcionario:
            if funcionario.estaAtivo:
                funcionario.estaAtivo = False
                print("Funcionario Demitido")
            else:
                print("Funcionario ja esta Inativo")
        else:
            print(f"Erro: Matrícula {matricula} não encontrada.")
    def iniciarFerias(self, matricula):
        funcionario = self.buscarPorMatricula(matricula)
        if funcionario:
            if funcionario.estaAtivo:
                funcionario.estaDeFerias=True
                print("Funcionario esta de Ferias")
            else:
                print("Funcionario nao esta na equipe")
        else:
            print(f"Erro: Matrícula {matricula} não encontrada.")
    def encerrarFerias(self, matricula):
        funcionario = self.buscarPorMatricula(matricula)
        if funcionario:
            if funcionario.estaAtivo:
                funcionario.estaDeFerias=False
                print("Funcionario voltou de Ferias")
            else:
                print("Funcionario nao esta na equipe")
        else:
            print(f"Erro: Matrícula {matricula} não encontrada.")