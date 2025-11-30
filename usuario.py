from database import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    # Colunas do Banco
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    permissao = db.Column(db.String(20), nullable=False) # 'admin' ou 'comum'
    
    # Se for funcionário comum, guardamos a matrícula para saber quem é
    matricula = db.Column(db.String(20), nullable=True)

    # Construtor Original
    def __init__(self, login, senha, permissao, matricula=None):
        self.login = login
        self.senha = senha
        self.permissao = permissao
        self.matricula = matricula