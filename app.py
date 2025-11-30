from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import db

# IMPORTAMOS OS SEUS ARQUIVOS ORIGINAIS
from funcionario import Funcionario
from medico import Medico
from enfermeiro import Enfermeiro
from funcionarioAdmin import FuncionarioAdmin
from usuario import Usuario
from registro_ponto import RegistroPonto
# Se quiser o log no banco depois: from log import RegistroLog 

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
app.config['SECRET_KEY'] = 'chave_secreta_do_souzza' # Necessário para mensagens de erro/sucesso
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinica.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco com este app
db.init_app(app)

# --- ROTAS ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/funcionarios')
def funcionarios():
    # FILTRO: Ver ativos ou demitidos
    status_filtro = request.args.get('ver')
    
    if status_filtro == 'demitidos':
        # Graças ao polimorfismo, isso busca Médicos, Enfermeiros e Admins inativos
        lista = Funcionario.query.filter_by(esta_ativo=False).all()
        titulo = "Funcionários Demitidos"
    else:
        lista = Funcionario.query.filter_by(esta_ativo=True).all()
        titulo = "Lista de Funcionários"

    return render_template('funcionarios.html', funcionarios=lista, filtro_atual=status_filtro, titulo_pagina=titulo)

@app.route('/cadastro', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar_banco():
    dados = request.form
    tipo = dados.get('tipo')
    
    novo_func = None

    try:
        # AQUI USAMOS AS SUAS CLASSES ORIGINAIS
        if tipo == 'medico':
            novo_func = Medico(
                matricula=dados.get('matricula'),
                nome=dados.get('nome'),
                cpf=dados.get('cpf'),
                salario_base=float(dados.get('salario') or 0),
                crm=dados.get('crm'),
                especialidade=dados.get('especialidade'),
                valor_hora_extra=float(dados.get('hora_extra') or 0)
            )
            
        elif tipo == 'enfermeiro':
            novo_func = Enfermeiro(
                matricula=dados.get('matricula'),
                nome=dados.get('nome'),
                cpf=dados.get('cpf'),
                salario_base=float(dados.get('salario') or 0),
                coren=dados.get('coren'),
                turno=dados.get('turno'),
                adicional_noturno=float(dados.get('adicional') or 0.2)
            )
            
        elif tipo == 'admin':
            novo_func = FuncionarioAdmin(
                matricula=dados.get('matricula'),
                nome=dados.get('nome'),
                cpf=dados.get('cpf'),
                salario_base=float(dados.get('salario') or 0),
                cargo=dados.get('cargo')
            )

        if novo_func:
            db.session.add(novo_func)
            db.session.commit()
            flash(f"Sucesso! {dados.get('nome')} cadastrado.", "success")
            return redirect('/funcionarios')

    except Exception as e:
        db.session.rollback()
        msg = str(e)
        if "UNIQUE constraint" in msg:
            flash("Erro: Já existe um funcionário com esta Matrícula ou CPF.", "danger")
        else:
            flash(f"Erro ao cadastrar: {msg}", "danger")
        return redirect('/cadastro')
    
    return redirect('/funcionarios')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    funcionario = Funcionario.query.get(id)
    
    if request.method == 'POST':
        dados = request.form
        
        # Atualiza dados comuns
        funcionario.nome = dados.get('nome')
        funcionario.cpf = dados.get('cpf')
        funcionario.salario_base = float(dados.get('salario') or 0)
        
        # Atualiza dados específicos checando o tipo (Polimorfismo)
        if funcionario.tipo_func == 'medico':
            funcionario.crm = dados.get('crm')
            funcionario.especialidade = dados.get('especialidade')
            funcionario.valor_hora_extra = float(dados.get('hora_extra') or 0)
        elif funcionario.tipo_func == 'enfermeiro':
            funcionario.coren = dados.get('coren')
            funcionario.turno = dados.get('turno')
        elif funcionario.tipo_func == 'admin':
            funcionario.cargo = dados.get('cargo')

        db.session.commit()
        flash("Dados atualizados com sucesso!", "success")
        return redirect('/funcionarios')

    return render_template('cadastro.html', func_edit=funcionario)

@app.route('/demitir/<int:id>', methods=['POST'])
def demitir(id):
    funcionario = Funcionario.query.get(id)
    if funcionario:
        funcionario.esta_ativo = False
        db.session.commit()
        flash(f"{funcionario.nome} foi demitido.", "warning")
    return redirect('/funcionarios')

@app.route('/ferias/<int:id>', methods=['POST'])
def ferias(id):
    funcionario = Funcionario.query.get(id)
    if funcionario and funcionario.esta_ativo:
        funcionario.em_ferias = not funcionario.em_ferias
        db.session.commit()
        estado = "entrou em" if funcionario.em_ferias else "voltou das"
        flash(f"{funcionario.nome} {estado} férias.", "info")
    return redirect('/funcionarios')

# ROTA DA FOLHA (USANDO SEU MÉTODO CALCULAR SALARIO!)
@app.route('/folha', methods=['GET', 'POST'])
def folha():
    # Só médicos ativos para o formulário de horas
    # Precisamos filtrar pelo tipo_func pq Medico.query.all() pode dar erro se não configurado
    medicos = Funcionario.query.filter_by(esta_ativo=True, tipo_func='medico').all()
    folha_calculada = None

    if request.method == 'POST':
        folha_calculada = []
        todos = Funcionario.query.filter_by(esta_ativo=True).all()
        
        for func in todos:
            # Se estiver de férias, pula
            if func.em_ferias:
                continue

            horas = 0
            if func.tipo_func == 'medico':
                horas = float(request.form.get(f"horas_{func.id}") or 0)
            
            # AQUI ESTÁ A SUA LÓGICA DE POO RODANDO:
            salario_final = func.calcularSalario(horas)
            
            folha_calculada.append({
                'nome': func.nome,
                'cargo': func.tipo_func.capitalize(),
                'salario_base': func.salario_base,
                'salario_liquido': salario_final,
                'horas_extras': horas if func.tipo_func == 'medico' else '-'
            })
            
    return render_template('folha.html', medicos=medicos, resultado=folha_calculada)

# Rota de Login
# Rota de Login (Híbrida: Admin ou Funcionário)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_form = request.form.get('login')
        senha_form = request.form.get('senha')
        
        # 1. TENTATIVA ADMIN: Busca na tabela de Usuários
        usuario_admin = Usuario.query.filter_by(login=login_form).first()
        
        if usuario_admin and usuario_admin.senha == senha_form:
            # Login de Admin
            session['usuario_logado'] = usuario_admin.login
            session['permissao'] = 'admin'
            flash(f"Bem-vindo, Admin {usuario_admin.login}!", "success")
            return redirect('/') # Vai para o Dashboard

        # 2. TENTATIVA FUNCIONÁRIO: Busca na tabela de Funcionários
        # Login = Matrícula | Senha = CPF
        funcionario = Funcionario.query.filter_by(matricula=login_form).first()
        
        if funcionario and funcionario.cpf == senha_form:
            
            # Verifica se ele está ativo antes de deixar entrar
            if not funcionario.esta_ativo:
                flash("Acesso negado. Funcionário inativo.", "danger")
                return redirect('/login')

            # Login de Funcionário
            session['usuario_logado'] = funcionario.nome
            session['permissao'] = 'comum'
            session['id_funcionario'] = funcionario.id # Guardamos o ID para saber de quem é o ponto
            
            flash(f"Olá, {funcionario.nome}!", "success")
            # Redireciona direto para a área dele
            return redirect(f'/area_colaborador/{funcionario.id}')

        # Se falhou nas duas tentativas
        flash("Login ou senha incorretos.", "danger")

    return render_template('login.html')

# Rota de Logout
@app.route('/logout')
def logout():
    session.clear() # Limpa a sessão
    flash("Você saiu do sistema.", "info")
    return redirect('/login')

from datetime import datetime

# 1. Rota da Tela do Colaborador
@app.route('/area_colaborador/<int:id>')
def area_colaborador(id):
    # SEGURANÇA: Verifica se quem está logado é o dono dessa página
    if session.get('id_funcionario') != id:
        flash("Acesso não autorizado!", "danger")
        return redirect('/login')

    funcionario = Funcionario.query.get(id)
    
    # Busca os últimos 5 pontos (do mais recente para o antigo)
    # Como definimos o relacionamento no models.py, podemos usar RegistroPonto direto
    ultimos_pontos = RegistroPonto.query.filter_by(funcionario_id=id).order_by(RegistroPonto.data.desc()).limit(10).all()
    
    return render_template('colaborador.html', func=funcionario, pontos=ultimos_pontos)

# 2. Rota de Ação (Bater Ponto)
@app.route('/bater_ponto/<int:id>/<tipo>', methods=['POST'])
def bater_ponto(id, tipo):
    agora = datetime.now()
    hoje = agora.strftime('%Y-%m-%d')
    hora_atual = agora.strftime('%H:%M')
    
    if tipo == 'entrada':
        # Cria novo registro
        novo_ponto = RegistroPonto(
            funcionario_id=id,
            data=hoje,
            hora_entrada=hora_atual
        )
        db.session.add(novo_ponto)
        flash(f"Entrada registrada às {hora_atual}!", "success")
    
    elif tipo == 'saida':
        # Busca o último ponto de hoje que ainda não tem saída
        ponto_aberto = RegistroPonto.query.filter_by(funcionario_id=id, data=hoje, hora_saida=None).first()
        
        if ponto_aberto:
            ponto_aberto.hora_saida = hora_atual
            flash(f"Saída registrada às {hora_atual}!", "info")
        else:
            flash("Erro: Você não registrou entrada hoje ou já fechou o ponto.", "danger")

    db.session.commit()
    return redirect(f'/area_colaborador/{id}')

# --- INICIALIZAÇÃO ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # --- CRIAÇÃO AUTOMÁTICA DO ADMIN (SÓ PARA TESTE) ---
        if not Usuario.query.filter_by(login='admin').first():
            admin = Usuario('admin', '1234', 'admin')
            db.session.add(admin)
            db.session.commit()
            print("--- Usuário ADMIN criado: login='admin', senha='1234' ---")
            
    app.run(debug=True)