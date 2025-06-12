from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email, Length, Optional
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class CadastroForm(FlaskForm):
    nome = StringField('Nome Completo', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Cadastrar')

class EditarGestorForm(FlaskForm):
    nome = StringField('Nome Completo', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    foto = FileField('Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens!'), Optional()])
    submit = SubmitField('Salvar Alterações')

class VeiculoForm(FlaskForm):
    placa = StringField('Placa do Veículo', validators=[DataRequired(), Length(min=7, max=10)])
    modelo = StringField('Modelo', validators=[DataRequired(), Length(max=50)])
    ano = IntegerField('Ano de Fabricação', validators=[DataRequired()])
    submit = SubmitField('Salvar Veículo')

class DocumentoForm(FlaskForm):
    tipo = StringField('Tipo de Documento (Ex: CRLV, Seguro)', validators=[DataRequired()])
    numero = StringField('Número do Documento (Opcional)')
    data_vencimento = DateField('Data de Vencimento', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Salvar Documento')