# no arquivo teste.py

from sistemaRH import SistemaRH
from medico import Medico
from enfermeiro import Enfermeiro
from funcionarioAdmin import FuncionarioAdmin

def rodar_teste_completo():
    """Função principal que vai testar todo o ciclo de vida dos funcionários."""
    
    print("--- INICIANDO TESTE COMPLETO DO SISTEMA DE RH ---")

    # 1. CRIAR A INSTÂNCIA DO SISTEMA
    sistema = SistemaRH()
    print("\n[PASSO 1] Objeto SistemaRH criado com sucesso.")

    # 2. CRIAR OBJETOS PARA TESTE
    # Criamos 3 funcionários para testar os diferentes status
    medico1 = Medico(matricula=101, nome="Dr. Gregory House", cpf="111.111.111-11", salarioBase=15000.0, crm="12345-RJ", especialidade="Nefrologia", valorHoraExtra=150.0)
    enfermeira1 = Enfermeiro(matricula=202, nome="Florence Nightingale", cpf="222.222.222-22", salarioBase=4000.0, coren="67890-SP", turno="noturno", adicionalNoturno=0.2)
    admin1 = FuncionarioAdmin(matricula=303, nome="Sr. Smith (A Ser Demitido)", cpf="333.333.333-33", salarioBase=2500.0, cargo="Recepcionista")
    print("[PASSO 2] Objetos de funcionários de teste criados.")

    # 3. TESTAR O MÉTODO 'adicionarFuncionario'
    print("\n[PASSO 3] Adicionando funcionários ao sistema...")
    sistema.adicionarFuncionario(medico1)
    sistema.adicionarFuncionario(enfermeira1)
    sistema.adicionarFuncionario(admin1)

    # 4. TESTAR 'listarFuncionarios' (DEPOIS DE ADICIONAR)
    print("\n[PASSO 4] Listando funcionários (todos devem estar ATIVOS):")
    sistema.listarFuncionarios()
    # (Esperado: Ver Dr. House, Florence e Sr. Smith, todos ATIVOS)

    # 5. TESTAR 'demitirFuncionario'
    print("\n[PASSO 5] Testando demissão do funcionário 303...")
    sistema.demitirFuncionario(303) # Demitindo o Sr. Smith

    # 6. TESTAR 'listarFuncionarios' (DEPOIS DE DEMITIR)
    print("\n[PASSO 6] Listando funcionários (Sr. Smith NÃO deve aparecer):")
    sistema.listarFuncionarios()
    # (Esperado: Ver APENAS Dr. House e Florence)

    # 7. TESTAR 'iniciarFerias'
    print("\n[PASSO 7] Colocando funcionária 202 (Florence) de férias...")
    sistema.iniciarFerias(202)
    # Vamos verificar o status dela chamando exibirDados() diretamente
    func_ferias = sistema.buscarPorMatricula(202)
    if func_ferias:
        print("\n--- Verificando status da funcionária 202 ---")
        func_ferias.exibirDados()
        print("--- Fim da verificação ---")
    # (Esperado: Ver os dados da Florence com o status "Em Ferias")

    # 8. TESTAR 'editarFuncionario'
    print("\n[PASSO 8] Editando dados do Dr. House (matrícula 101)...")
    dados_para_atualizar = {
        "salarioBase": 17000.0,
        "especialidade": "Diagnóstico e Nefrologia"
    }
    sistema.editarFuncionario(101, dados_para_atualizar)
    # Vamos verificar os dados dele
    func_editado = sistema.buscarPorMatricula(101)
    if func_editado:
        print("\n--- Verificando dados ATUALIZADOS do funcionário 101 ---")
        func_editado.exibirDados()
        print("--- Fim da verificação ---")
    # (Esperado: Ver Dr. House com o novo salário base de 17000.00 e nova especialidade)

    # 9. TESTE FINAL: 'gerarFolhaDePagamento' (O TESTE DE POLIMORFISMO E FILTROS)
    print("\n[PASSO 9] Gerando a folha de pagamento...")
    mapa_horas_teste = {
        101: 10, # Dr. House (ATIVO, NÃO-FÉRIAS) -> DEVE RECEBER (com salário novo + 10h extras)
        202: 5,  # Florence (ATIVA, EM FÉRIAS)  -> NÃO DEVE RECEBER
        303: 20  # Sr. Smith (INATIVO)         -> NÃO DEVE RECEBER
    }
    sistema.gerarFolhaDePagamento(mapa_horas_teste)
    # (Esperado: Ver APENAS o pagamento do Dr. House)
    # Cálculo esperado: 17000 + (10 * 150) = 18500.00

    print("\n--- FIM DO TESTE COMPLETO ---")


# Esta linha executa a função de teste quando rodamos o arquivo Python
if __name__ == "__main__":
    rodar_teste_completo()