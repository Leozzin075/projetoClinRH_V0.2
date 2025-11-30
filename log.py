from database import db
from datetime import datetime

class RegistroLog(db.Model):
    __tablename__ = 'logs'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    usuario = db.Column(db.String(50))
    acao = db.Column(db.String(50))
    alvo = db.Column(db.String(50))

    def __init__(self, usuario, acao, alvo):
        self.usuario = usuario
        self.acao = acao
        self.alvo = alvo
        self.timestamp = datetime.now()