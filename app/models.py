from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class Gestor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    foto = db.Column(db.String(200), nullable=True)
    senha_hash = db.Column(db.String(256), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    veiculos = db.relationship('Veiculo', backref='gestor', lazy=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10), unique=True, nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    gestor_id = db.Column(db.Integer, db.ForeignKey('gestor.id'), nullable=True)
    documentos = db.relationship('Documento', backref='veiculo', lazy=True, cascade="all, delete-orphan")

class Documento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    numero = db.Column(db.String(100), nullable=True)
    data_vencimento = db.Column(db.Date, nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)