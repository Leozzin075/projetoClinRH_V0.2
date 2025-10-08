import datetime
from abc import ABC, abstractmethod

class Funcionario(ABC):
    def __init__(self, matricula, nome, cpf, salarioBase):
        self.matricula = matricula
        self.nome = nome
        self.cpf = cpf
        self.salarioBase = salarioBase
        self.registroDePonto = []
        
    def _pegarTimeAtual_(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def registrarEntrada(self):
        timestamp_atual = self._pegarTimeAtual_()
        self.registroDePonto.append({'tipo':'Entrada', 'horario': timestamp_atual})
        print(f"Sua entrada foi registrada: {self.nome} no horario:{timestamp_atual}")

    def registrarSaida(self):
        timestamp_atual = self._pegarTimeAtual_()
        self.registroDePonto.append({'tipo':'Saida', 'horario': timestamp_atual})
        print(f"Sua saida foi registrada: {self.nome} no horario:{timestamp_atual}")

    def exibirDados(self):
        print (f"Matricula: {self.matricula}")
        print(f"Nome: {self.nome}")
        print(f"CPF: {self.cpf}")
        print(f"Salario base: {self.salarioBase:.2f}")
        if not self.registroDePonto:
            print("Nenhum registro de ponto foi encontrado")
        else:
            for registro in self.registroDePonto:
                print(f"Tipo: {registro['tipo']}\nHorario: {registro['horario']}")
    
    @abstractmethod
    def calcularSalario(self, horasExtras):
        pass