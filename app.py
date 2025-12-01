from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import db
from datetime import datetime

# --- IMPORTANDO SEUS MODELOS ---
from funcionario import Funcionario
from medico import Medico
from enfermeiro import Enfermeiro
from funcionarioAdmin import FuncionarioAdmin
from usuario import Usuario
from log import RegistroLog 
from registro_ponto import RegistroPonto 

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
app.config['SECRET_KEY'] = 'chave_secreta_do_souzza'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinica.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco com este app
db.init_app(app)

# ==============================================================================
# ROTAS DE ACESSO (LOGIN / LOGOUT / HOME)
# ==============================================================================

@app.route('/')
def index():
    # Verifica se tem alguém logado
    if 'usuario_logado' not in session:
        return redirect('/login')
    
    # Se for funcionário comum, manda para a área dele
    if session.get('permissao') != 'admin':
        id_func = session.get('id_funcionario')
        return redirect(f'/area_colaborador/{id_func}')
    
    total_ativos = Funcionario.query.filter_by(esta_ativo=True).count()

    total_ferias = Funcionario.query.filter_by(esta_ativo=True, em_ferias=True).count()
    
    hoje_str = datetime.now().strftime('%Y-%m-%d')
    pontos_hoje = RegistroPonto.query.filter_by(data=hoje_str).count()

    return render_template('index.html', 
                           total_ativos=total_ativos, 
                           total_ferias=total_ferias,
                           pontos_hoje=pontos_hoje)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_form = request.form.get('login')
        senha_form = request.form.get('senha')
        
        # 1. TENTATIVA ADMIN
        usuario_admin = Usuario.query.filter_by(login=login_form).first()
        
        if usuario_admin and usuario_admin.senha == senha_form:
            session['usuario_logado'] = usuario_admin.login
            session['permissao'] = 'admin'
            flash(f"Bem-vindo, Admin {usuario_admin.login}!", "success")
            return redirect('/') 

        # 2. TENTATIVA FUNCIONÁRIO
        funcionario = Funcionario.query.filter_by(matricula=login_form).first()
        
        if funcionario and funcionario.cpf == senha_form:
            if not funcionario.esta_ativo:
                flash("Acesso negado. Funcionário inativo.", "danger")
                return redirect('/login')

            session['usuario_logado'] = funcionario.nome
            session['permissao'] = 'comum'
            session['id_funcionario'] = funcionario.id
            
            flash(f"Olá, {funcionario.nome}!", "success")
            return redirect(f'/area_colaborador/{funcionario.id}')

        flash("Login ou senha incorretos.", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Saiu com sucesso.", "info")
    return redirect('/login')

# ==============================================================================
# ROTAS DE GESTÃO DE FUNCIONÁRIOS (APENAS ADMIN)
# ==============================================================================

@app.route('/funcionarios')
def funcionarios():
    if session.get('permissao') != 'admin':
        return redirect('/')

    status_filtro = request.args.get('ver')
    
    if status_filtro == 'demitidos':
        lista = Funcionario.query.filter_by(esta_ativo=False).all()
        titulo = "Funcionários Demitidos"
    else:
        lista = Funcionario.query.filter_by(esta_ativo=True).all()
        titulo = "Lista de Funcionários"

    return render_template('funcionarios.html', funcionarios=lista, filtro_atual=status_filtro, titulo_pagina=titulo)

@app.route('/cadastro', methods=['GET'])
def cadastro():
    if session.get('permissao') != 'admin':
        return redirect('/')
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar_banco():
    if session.get('permissao') != 'admin':
        return redirect('/')

    dados = request.form
    tipo = dados.get('tipo')
    
    novo_func = None
    acao_log = "Adicionar"

    try:
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
            
            # --- REGISTRAR LOG ---
            log = RegistroLog(session['usuario_logado'], acao_log, f"Novo {tipo}: {novo_func.nome}")
            db.session.add(log)
            
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
    if session.get('permissao') != 'admin':
        return redirect('/')

    funcionario = Funcionario.query.get(id)
    
    if request.method == 'POST':
        dados = request.form
        
        funcionario.nome = dados.get('nome')
        funcionario.cpf = dados.get('cpf')
        funcionario.salario_base = float(dados.get('salario') or 0)
        
        if funcionario.tipo_func == 'medico':
            funcionario.crm = dados.get('crm')
            funcionario.especialidade = dados.get('especialidade')
            funcionario.valor_hora_extra = float(dados.get('hora_extra') or 0)
        elif funcionario.tipo_func == 'enfermeiro':
            funcionario.coren = dados.get('coren')
            funcionario.turno = dados.get('turno')
        elif funcionario.tipo_func == 'admin':
            funcionario.cargo = dados.get('cargo')

        # Log
        log = RegistroLog(session['usuario_logado'], "Editar", f"Atualizou {funcionario.nome}")
        db.session.add(log)

        db.session.commit()
        flash("Dados atualizados com sucesso!", "success")
        return redirect('/funcionarios')

    return render_template('cadastro.html', func_edit=funcionario)

@app.route('/demitir/<int:id>', methods=['POST'])
def demitir(id):
    if session.get('permissao') != 'admin':
        return redirect('/')

    funcionario = Funcionario.query.get(id)
    if funcionario:
        funcionario.esta_ativo = False
        
        # Log
        log = RegistroLog(session['usuario_logado'], "Demitir", f"Demitiu {funcionario.nome}")
        db.session.add(log)
        
        db.session.commit()
        flash(f"{funcionario.nome} foi demitido.", "warning")
    return redirect('/funcionarios')

@app.route('/ferias/<int:id>', methods=['POST'])
def ferias(id):
    if session.get('permissao') != 'admin':
        return redirect('/')

    funcionario = Funcionario.query.get(id)
    if funcionario and funcionario.esta_ativo:
        funcionario.em_ferias = not funcionario.em_ferias
        estado = "entrou em" if funcionario.em_ferias else "voltou das"
        
        # Log
        log = RegistroLog(session['usuario_logado'], "Ferias", f"{funcionario.nome} {estado} férias")
        db.session.add(log)
        
        db.session.commit()
        flash(f"{funcionario.nome} {estado} férias.", "info")
    return redirect('/funcionarios')

# ==============================================================================
# ROTA FINANCEIRA (FOLHA DE PAGAMENTO)
# ==============================================================================

@app.route('/folha', methods=['GET', 'POST'])
def folha():
    if session.get('permissao') != 'admin':
        return redirect('/')

    # Busca apenas médicos ativos para o formulário de horas
    medicos = Funcionario.query.filter_by(esta_ativo=True, tipo_func='medico').all()
    folha_calculada = None

    if request.method == 'POST':
        folha_calculada = []
        todos = Funcionario.query.filter_by(esta_ativo=True).all()
        
        for func in todos:
            if func.em_ferias:
                continue

            horas = 0
            # Se for médico, pega as horas do formulário
            if func.tipo_func == 'medico':
                horas = float(request.form.get(f"horas_{func.id}") or 0)
            
            # Calcula o salário usando o método da classe
            salario_final = func.calcularSalario(horas)
            
            folha_calculada.append({
                'nome': func.nome,
                'cargo': func.tipo_func.capitalize(),
                'salario_base': func.salario_base,
                'salario_liquido': salario_final,
                'horas_extras': horas if func.tipo_func == 'medico' else '-'
            })
        
        # --- AQUI ESTAVA FALTANDO O LOG ---
        if folha_calculada:
            qtd = len(folha_calculada)
            # Soma o total pago para ficar bonito no log
            total_valor = sum(item['salario_liquido'] for item in folha_calculada)
            
            log = RegistroLog(
                session['usuario_logado'], 
                "Folha", 
                f"Gerada p/ {qtd} funcs. Total: R$ {total_valor:.2f}"
            )
            db.session.add(log)
            db.session.commit()
            
            flash("Cálculo realizado e registrado no log!", "success")
            
    return render_template('folha.html', medicos=medicos, resultado=folha_calculada)

# ==============================================================================
# ROTAS DE PONTO
# ==============================================================================

@app.route('/ponto', methods=['GET', 'POST'])
def ponto():
    if session.get('permissao') != 'admin':
        return redirect('/')

    if request.method == 'POST':
        dados = request.form
        
        novo_ponto = RegistroPonto(
            funcionario_id=int(dados.get('funcionario_id')),
            data=dados.get('data'),
            hora_entrada=dados.get('entrada'),
            hora_saida=dados.get('saida')
        )
        
        db.session.add(novo_ponto)
        # Log
        log = RegistroLog(session['usuario_logado'], "Ponto Manual", f"Ponto p/ ID {dados.get('funcionario_id')}")
        db.session.add(log)
        
        db.session.commit()
        flash("Ponto registrado manualmente com sucesso!", "success")
        return redirect('/ponto')

    filtro_id = request.args.get('filtro_id')
    
    if filtro_id and filtro_id != 'todos':
        pontos = RegistroPonto.query.filter_by(funcionario_id=filtro_id).order_by(RegistroPonto.data.desc()).all()
    else:
        pontos = RegistroPonto.query.order_by(RegistroPonto.data.desc()).all()

    funcionarios = Funcionario.query.filter_by(esta_ativo=True).all()
    
    return render_template('ponto.html', pontos=pontos, funcionarios=funcionarios, filtro_atual=filtro_id)

# ==============================================================================
# ROTA DE LOGS (CORRIGIDA)
# ==============================================================================

@app.route('/logs')
def logs():
    if session.get('permissao') != 'admin':
        flash("Acesso restrito.", "danger")
        return redirect('/')

    # AQUI ESTAVA O ERRO: Usamos RegistroLog, e não Log
    lista_logs = RegistroLog.query.order_by(RegistroLog.timestamp.desc()).all()
    
    return render_template('logs.html', logs=lista_logs)

# ==============================================================================
# ROTAS DO COLABORADOR
# ==============================================================================

@app.route('/area_colaborador/<int:id>')
def area_colaborador(id):
    if session.get('permissao') != 'admin' and session.get('id_funcionario') != id:
        flash("Acesso não autorizado.", "danger")
        return redirect('/login')

    funcionario = Funcionario.query.get(id)
    if not funcionario:
        flash("Funcionário não encontrado.", "danger")
        return redirect('/login')

    ultimos_pontos = RegistroPonto.query.filter_by(funcionario_id=id).order_by(RegistroPonto.data.desc()).limit(10).all()
    return render_template('colaborador.html', func=funcionario, pontos=ultimos_pontos)

@app.route('/bater_ponto/<int:id>/<tipo>', methods=['POST'])
def bater_ponto_acao(id, tipo):
    if session.get('id_funcionario') != id:
        return redirect('/login')

    agora = datetime.now()
    hoje_str = agora.strftime('%Y-%m-%d')
    hora_str = agora.strftime('%H:%M')

    if tipo == 'entrada':
        novo_ponto = RegistroPonto(
            funcionario_id=id,
            data=hoje_str,
            hora_entrada=hora_str,
            hora_saida=None
        )
        db.session.add(novo_ponto)
        flash(f"Entrada registrada às {hora_str}.", "success")

    elif tipo == 'saida':
        ponto_aberto = RegistroPonto.query.filter_by(
            funcionario_id=id, 
            data=hoje_str, 
            hora_saida=None
        ).first()

        if ponto_aberto:
            ponto_aberto.hora_saida = hora_str
            flash(f"Saída registrada às {hora_str}.", "info")
        else:
            flash("Erro: Você não registrou entrada hoje ou já fechou o ponto!", "danger")

    db.session.commit()
    return redirect(f'/area_colaborador/{id}')

# ==============================================================================
# INICIALIZAÇÃO
# ==============================================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Cria admin padrão se não existir
        if not Usuario.query.filter_by(login='admin').first():
            admin = Usuario('admin', '1234', 'admin')
            db.session.add(admin)
            db.session.commit()
            print("--- ADMIN PADRÃO CRIADO: login='admin', senha='1234' ---")
            
    app.run(debug=True)