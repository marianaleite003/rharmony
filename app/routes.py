from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from .models import Gestor, Veiculo, Documento
from .forms import CadastroForm, LoginForm, EditarGestorForm, VeiculoForm, DocumentoForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

# --- ROTAS DE SESSÃO E PÁGINAS PÚBLICAS ---
@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        gestor = Gestor.query.filter_by(email=form.email.data).first()
        if gestor and gestor.verificar_senha(form.senha.data):
            login_user(gestor)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Email ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = CadastroForm()
    if form.validate_on_submit():
        novo_gestor = Gestor(nome=form.nome.data, email=form.email.data)
        novo_gestor.set_senha(form.senha.data)
        db.session.add(novo_gestor)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça o login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('cadastro.html', form=form)

# --- ROTAS DA ÁREA LOGADA ---
@main.route('/dashboard')
@login_required
def dashboard():
    hoje = datetime.utcnow().date()
    limite_alerta = hoje + timedelta(days=30)
    documentos_perto_vencer = Documento.query.filter(Documento.data_vencimento.between(hoje, limite_alerta)).count()
    documentos_vencidos = Documento.query.filter(Documento.data_vencimento < hoje).count()
    alertas_docs = Documento.query.filter(Documento.data_vencimento < limite_alerta).order_by(Documento.data_vencimento.asc()).all()
    return render_template('dashboard.html', documentos_perto_vencer=documentos_perto_vencer, documentos_vencidos=documentos_vencidos, alertas=alertas_docs, hoje=hoje)

@main.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    form = EditarGestorForm(obj=current_user)
    if form.validate_on_submit():
        current_user.nome = form.nome.data
        current_user.email = form.email.data
        if form.foto.data:
            filename = secure_filename(form.foto.data.filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads')
            form.foto.data.save(os.path.join(upload_path, filename))
            current_user.foto = filename
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('main.perfil'))
    foto_perfil = url_for('static', filename=f'uploads/{current_user.foto}') if current_user.foto else None
    return render_template('perfil.html', form=form, foto_perfil=foto_perfil)

@main.route('/perfil/deletar', methods=['POST'])
@login_required
def deletar_perfil():
    user_to_delete = Gestor.query.get_or_404(current_user.id)
    logout_user()
    db.session.delete(user_to_delete)
    db.session.commit()
    flash('Sua conta foi excluída.', 'info')
    return redirect(url_for('main.index'))

# --- ROTAS DE VEÍCULOS ---
@main.route('/veiculos')
@login_required
def listar_veiculos():
    veiculos = Veiculo.query.order_by(Veiculo.placa).all()
    return render_template('listar_veiculos.html', veiculos=veiculos)

@main.route('/veiculos/novo', methods=['GET', 'POST'])
@login_required
def adicionar_veiculo():
    form = VeiculoForm()
    if form.validate_on_submit():
        novo_veiculo = Veiculo(placa=form.placa.data.upper(), modelo=form.modelo.data, ano=form.ano.data, gestor_id=current_user.id)
        db.session.add(novo_veiculo)
        db.session.commit()
        flash('Veículo adicionado! Agora adicione os documentos dele.', 'success')
        return redirect(url_for('main.listar_documentos', veiculo_id=novo_veiculo.id))
    return render_template('adicionar_veiculo.html', form=form, title="Adicionar Veículo")

@main.route('/veiculos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)
    form = VeiculoForm(obj=veiculo)
    if form.validate_on_submit():
        veiculo.placa = form.placa.data.upper()
        veiculo.modelo = form.modelo.data
        veiculo.ano = form.ano.data
        db.session.commit()
        flash('Veículo atualizado!', 'success')
        return redirect(url_for('main.listar_veiculos'))
    return render_template('adicionar_veiculo.html', form=form, title="Editar Veículo")

@main.route('/veiculos/deletar/<int:id>', methods=['POST'])
@login_required
def deletar_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)
    db.session.delete(veiculo)
    db.session.commit()
    flash('Veículo deletado.', 'success')
    return redirect(url_for('main.listar_veiculos'))

# --- ROTAS DE DOCUMENTOS ---
@main.route('/veiculo/<int:veiculo_id>/documentos')
@login_required
def listar_documentos(veiculo_id):
    veiculo = Veiculo.query.get_or_404(veiculo_id)
    return render_template('listar_documentos.html', veiculo=veiculo)

@main.route('/veiculo/<int:veiculo_id>/documentos/novo', methods=['GET', 'POST'])
@login_required
def adicionar_documento(veiculo_id):
    veiculo = Veiculo.query.get_or_404(veiculo_id)
    form = DocumentoForm()
    if form.validate_on_submit():
        novo_documento = Documento(tipo=form.tipo.data, numero=form.numero.data, data_vencimento=form.data_vencimento.data, veiculo_id=veiculo.id)
        db.session.add(novo_documento)
        db.session.commit()
        flash(f'Documento "{novo_documento.tipo}" adicionado!', 'success')
        return redirect(url_for('main.listar_documentos', veiculo_id=veiculo.id))
    return render_template('adicionar_documento.html', form=form, veiculo=veiculo)

@main.route('/documento/deletar/<int:documento_id>', methods=['POST'])
@login_required
def deletar_documento(documento_id):
    documento = Documento.query.get_or_404(documento_id)
    veiculo_id = documento.veiculo.id
    db.session.delete(documento)
    db.session.commit()
    flash('Documento deletado.', 'success')
    return redirect(url_for('main.listar_documentos', veiculo_id=veiculo_id))