from database import db
# Importamos Funcionario para fazer o relacionamento
from funcionario import Funcionario 

class RegistroPonto(db.Model):
    __tablename__ = 'pontos'
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10), nullable=False)
    hora_entrada = db.Column(db.String(5), nullable=True)
    hora_saida = db.Column(db.String(5), nullable=True)
    
    # Chave Estrangeira: Liga o ponto ao funcionário
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'), nullable=False)
    
    # Cria a "ponte": Ponto sabe quem é seu Funcionário, e Funcionário tem uma lista de 'pontos'
    funcionario = db.relationship('Funcionario', backref='pontos')

    def __init__(self, funcionario_id, data, hora_entrada, hora_saida=None):
        self.funcionario_id = funcionario_id
        self.data = data
        self.hora_entrada = hora_entrada
        self.hora_saida = hora_saida