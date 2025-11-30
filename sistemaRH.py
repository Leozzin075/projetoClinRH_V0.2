from funcionario import Funcionario
from medico import Medico
from enfermeiro import Enfermeiro
from funcionarioAdmin import FuncionarioAdmin
from log import RegistroLog
from usuario import Usuario

class SistemaRH:
    def __init__(self):
        self.funcionarios = []
        self.logs = []
        self.usuarios = []

    def _existeMatricula(self, matricula):
        for func in self.funcionarios:
            if func.matricula == matricula:
                return True
        return False
    
    def _existeLogin(self, login):
        for usuario in self.usuarios:
            if usuario.login == login:
                return True
        return False

    def adicionarFuncionario(self, funcionario):
        if self._existeLogin(funcionario.matricula):
            print(f"Erro: Ja existe um funcionario com a matricula {funcionario.matricula}")
            return
        self.funcionarios.append(funcionario)
        print(f"O funcionario {funcionario.nome} foi adicionado com sucesso!")
        self.registrarLog("AdminTemporario", "Adicionar", funcionario.matricula)

    def buscarPorMatricula(self, matricula):
        for funcionario in self.funcionarios:
            if funcionario.matricula == matricula:
                return funcionario
        return None
    
    def listarFuncionarios(self):
        if not self.funcionarios:
            print("Nenhum funcionario cadastrado")
            return
        print("Lista de Funcionarios\n")
        encontrouFuncionario = False
        for funcionario in self.funcionarios:
            if funcionario.estaAtivo:
                funcionario.exibirDados()
                encontrouFuncionario = True
        if not encontrouFuncionario:
            print("Nenhum funcionario ativo encontrado.")

    def gerarFolhaDePagamento(self, mapaDeHoras):
        pagamentoRealizado = False
        for funcionario in self.funcionarios:
            if funcionario.estaAtivo and not funcionario.estaDeFerias:
                try:
                    horasExtras = mapaDeHoras.get(funcionario.matricula, 0)
                    salarioDoMes = funcionario.calcularSalario(horasExtras)
                    print(f"Pagamento do funcionario {funcionario.nome}: RS{salarioDoMes:.2f}")
                    pagamentoRealizado = True
                except ValueError:
                    print(f"Erro ao calcular salario de {funcionario.nome}: Horas extras invalidas")

        if not pagamentoRealizado:
            print("Ninguem para pagar este mes.")        

    def editarFuncionario(self, matricula, dadosParaAtualizar):
            funcionario = self.buscarPorMatricula(matricula)
            if not funcionario:
                print(f"Erro: Matrícula {matricula} não encontrada.")
                return
            for chave, valor in dadosParaAtualizar.items():
                if hasattr(funcionario, chave):
                    setattr(funcionario, chave, valor)                
                    print(f"LOG: {chave} do funcionário {matricula} atualizado para {valor}.") # Um log é bom
                else:
                    print(f"Aviso: Atributo '{chave}' não existe no funcionário e foi ignorado.")
            print(f"Dados do funcionário {funcionario.nome} atualizados com sucesso.")
            self.registrarLog("AdminTemporario", "Editar", matricula) 

    def demitirFuncionario(self, matricula):
        funcionario = self.buscarPorMatricula(matricula)
        if funcionario:
            if funcionario.estaAtivo:
                funcionario.estaAtivo = False
                print("Funcionario Demitido")
                self.registrarLog("AdminTemporario", "Demitir", matricula)
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
                self.registrarLog("AdminTemporario", "Inicio Ferias", matricula)
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
                self.registrarLog("AdminTemporario", "Fim Ferias", matricula)
            else:
                print("Funcionario nao esta na equipe")
        else:
            print(f"Erro: Matrícula {matricula} não encontrada.")

    def registrarLog(self, usuarioResponsavel, acao, alvo):
        novoLog = RegistroLog(usuarioResponsavel, acao, alvo)
        self.logs.append(novoLog)
        print(f"LOG REGISTRADO: {usuarioResponsavel} -> {acao} -> {alvo}")

    def cadastrarUsuarios(self, login, senha, permissao, matricula=None):
        if self._existeLogin(login):
            print(f"Erro: O login {login} ja esta em uso")
            return
        novoUsuario = Usuario(login, senha, permissao, matricula)
        self.usuarios.append(novoUsuario)
        print(f"Usuario {login} cadastrado com sucesso. (Permissao: {permissao})")

    def fazerLogin(self, login, senha):
        for usuario in self.usuarios:
            if usuario.login == login and usuario.senha == senha:
                print(f"Login realizado com sucesso! Bem-vindo, {login}.")
                return usuario
        print("Login ou senhas incorretos.")
        return None
    
    def registrarPontoFuncionario(self, matricula, tipo):
        funcionario = self.buscarPorMatricula(matricula)
        if funcionario:
            if funcionario.estaAtivo and not funcionario.estaDeFerias:
                funcionario.registrarPonto(tipo)
                self.registrarLog("FuncionarioProprio", f"Ponto-{tipo}", matricula)
                return True
            else:
                print("Erro: Funcionario inativo ou em ferias")
        else: 
            print("Erro: Matricula nao encontrada")
            return False