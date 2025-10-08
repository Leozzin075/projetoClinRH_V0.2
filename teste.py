#SCRIPT DE TESTE CRIADO PELA IA PARA TESTAR MEU SISTEMA

from sistemaRH import SistemaRH
from medico import Medico
from enfermeiro import Enfermeiro
from funcionarioAdmin import FuncionarioAdmin


def rodar_teste():
    """Função principal que vai executar nosso teste passo a passo."""
    
    print("--- INICIANDO TESTE DO SISTEMA DE RH ---")

    # 2. CRIAR A INSTÂNCIA DO SISTEMA
    # Este é o objeto "gerente" que vai conter nossa lista de funcionários.
    sistema = SistemaRH()
    print("\n[PASSO 1] Objeto SistemaRH criado com sucesso.")

    # 3. CRIAR OBJETOS PARA TESTE
    # Vamos criar um funcionário de cada tipo para testar.
    medico1 = Medico(matricula=101, nome="Dr. House", cpf="111.111.111-11", salarioBase=15000.0, crm="12345-RJ", especialidade="Nefrologia", valorHoraExtra=150.0)
    enfermeira1 = Enfermeiro(matricula=202, nome="Florence Nightingale", cpf="222.222.222-22", salarioBase=4000.0, coren="67890-SP", turno="Noturno", adcionalNoturno=0.2)
    admin1 = FuncionarioAdmin(matricula=303, nome="Sr. Smith", cpf="333.333.333-33", salarioBase=2500.0, cargo="Recepcionista")
    print("[PASSO 2] Objetos de funcionários de teste criados.")

    # 4. TESTAR O MÉTODO 'adicionar_funcionario'
    # Vamos adicionar os funcionários que criamos ao nosso sistema.
    print("\n[PASSO 3] Testando a adição de funcionários...")
    sistema.adicionarFuncionario(medico1)
    sistema.adicionarFuncionario(enfermeira1)
    sistema.adicionarFuncionario(admin1)

    # 5. TESTAR O MÉTODO 'buscar_por_matricula'
    print("\n[PASSO 4] Testando a busca por matrícula...")
    
    # Teste 1: Buscar uma matrícula que EXISTE
    matricula_para_buscar = 101
    print(f"Buscando pela matrícula: {matricula_para_buscar}")
    funcionario_encontrado = sistema.buscarPorMatricula(matricula_para_buscar)
    
    if funcionario_encontrado:
        print(f"SUCESSO! Funcionário encontrado: {funcionario_encontrado.nome}")
    else:
        print(f"FALHA! Funcionário com matrícula {matricula_para_buscar} não foi encontrado.")

    # Teste 2: Buscar uma matrícula que NÃO EXISTE
    matricula_para_buscar = 999
    print(f"\nBuscando pela matrícula: {matricula_para_buscar}")
    funcionario_encontrado = sistema.buscarPorMatricula(matricula_para_buscar)

    if funcionario_encontrado:
        print(f"FALHA! Encontrou um funcionário que não deveria existir: {funcionario_encontrado.nome}")
    else:
        print(f"SUCESSO! Funcionário com matrícula {matricula_para_buscar} corretamente não foi encontrado.")

    print("\n--- FIM DO TESTE ---")


if __name__ == "__main__":
    rodar_teste()