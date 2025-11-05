import os
import json
from datetime import datetime

# Arquivos de dados
USUARIOS_FILE = "usuarios.txt"
ALIMENTOS_FILE = "alimentos.txt"
PEDIDOS_FILE = "pedidos.txt"
AVALIACOES_FILE = "avaliacoes.txt"

# Usuário logado (declarada globalmente no início)
usuario_logado = None

# Inicializar arquivos se não existirem
def inicializar_arquivos():
    arquivos = [USUARIOS_FILE, ALIMENTOS_FILE, PEDIDOS_FILE, AVALIACOES_FILE]
    for arquivo in arquivos:
        if not os.path.exists(arquivo):
            with open(arquivo, 'w', encoding='utf-8') as f:
                if arquivo == ALIMENTOS_FILE:
                    # Adicionar alguns alimentos de exemplo
                    alimentos_exemplo = [
                        {"id": 1, "nome": "Maçã", "categoria": "Fruta", "calorias": 52, "preco": 2.50},
                        {"id": 2, "nome": "Pão Integral", "categoria": "Padaria", "calorias": 265, "preco": 1.80},
                        {"id": 3, "nome": "Frango Grelhado", "categoria": "Proteína", "calorias": 165, "preco": 12.90},
                        {"id": 4, "nome": "Arroz Integral", "categoria": "Grão", "calorias": 112, "preco": 8.50},
                        {"id": 5, "nome": "Iogurte Natural", "categoria": "Laticínio", "calorias": 59, "preco": 4.20}
                    ]
                    for alimento in alimentos_exemplo:
                        f.write(json.dumps(alimento, ensure_ascii=False) + '\n')

# Funções para manipulação de arquivos
def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        return [json.loads(linha.strip()) for linha in linhas if linha.strip()]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def escrever_arquivo(nome_arquivo, dados):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        for item in dados:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

# Funcionalidade 1: Cadastrar Novo Usuário
def cadastrar_usuario():
    print("\n=== CADASTRO DE USUÁRIO ===")
    
    usuarios = ler_arquivo(USUARIOS_FILE)
    
    email = input("Digite o email: ").strip()
    
    # Verificar se email já existe
    for usuario in usuarios:
        if usuario['email'] == email:
            print("❌ Este email já está cadastrado!")
            return False
    
    senha = input("Digite a senha: ").strip()
    nome = input("Digite o nome completo: ").strip()
    
    novo_usuario = {
        'id': len(usuarios) + 1,
        'nome': nome,
        'email': email,
        'senha': senha,
        'data_cadastro': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    usuarios.append(novo_usuario)
    escrever_arquivo(USUARIOS_FILE, usuarios)
    
    print("✅ Usuário cadastrado com sucesso!")
    return True

# Funcionalidade 2: Login do Usuário
def login_usuario():
    global usuario_logado
    
    print("\n=== LOGIN ===")
    
    email = input("Email: ").strip()
    senha = input("Senha: ").strip()
    
    usuarios = ler_arquivo(USUARIOS_FILE)
    
    for usuario in usuarios:
        if usuario['email'] == email and usuario['senha'] == senha:
            usuario_logado = usuario
            print(f"✅ Login realizado com sucesso! Bem-vindo(a), {usuario['nome']}!")
            return True
    
    print("❌ Email ou senha incorretos!")
    return False

# Funcionalidade 3: Buscar Alimento
def buscar_alimento():
    print("\n=== BUSCAR ALIMENTO ===")
    
    termo = input("Digite o nome ou categoria do alimento: ").strip().lower()
    
    alimentos = ler_arquivo(ALIMENTOS_FILE)
    resultados = []
    
    for alimento in alimentos:
        if (termo in alimento['nome'].lower() or 
            termo in alimento['categoria'].lower()):
            resultados.append(alimento)
    
    if resultados:
        print(f"\n🔍 {len(resultados)} resultado(s) encontrado(s):")
        for alimento in resultados:
            print(f"ID: {alimento['id']} | {alimento['nome']} | "
                  f"Categoria: {alimento['categoria']} | "
                  f"Calorias: {alimento['calorias']}kcal | "
                  f"Preço: R${alimento['preco']:.2f}")
        return resultados
    else:
        print("❌ Nenhum alimento encontrado com esse termo.")
        return []

# Funcionalidade 4: Listar informações de alimentos buscados
def listar_informacoes_alimentos(alimentos=None):
    if alimentos is None:
        alimentos = ler_arquivo(ALIMENTOS_FILE)
    
    print("\n=== INFORMAÇÕES DOS ALIMENTOS ===")
    
    if not alimentos:
        print("Nenhum alimento para mostrar.")
        return
    
    for alimento in alimentos:
        print(f"\n📋 {alimento['nome'].upper()}")
        print(f"   Categoria: {alimento['categoria']}")
        print(f"   Calorias: {alimento['calorias']} kcal")
        print(f"   Preço: R${alimento['preco']:.2f}")
        print(f"   ID: {alimento['id']}")

# Funcionalidade 5: Cadastrar Pedido (Criar, editar, excluir, adicionar/remover alimentos)
def cadastrar_pedido():
    global usuario_logado
    
    if not usuario_logado:
        print("❌ Você precisa estar logado para criar um pedido!")
        return
    
    print("\n=== GERENCIAR PEDIDOS ===")
    print("1. Criar novo pedido")
    print("2. Editar pedido existente")
    print("3. Excluir pedido")
    print("4. Adicionar alimento ao pedido")
    print("5. Remover alimento do pedido")
    print("6. Ver meus pedidos")
    
    opcao = input("\nEscolha uma opção: ").strip()
    
    if opcao == "1":
        criar_pedido()
    elif opcao == "2":
        editar_pedido()
    elif opcao == "3":
        excluir_pedido()
    elif opcao == "4":
        adicionar_alimento_pedido()
    elif opcao == "5":
        remover_alimento_pedido()
    elif opcao == "6":
        listar_meus_pedidos()
    else:
        print("❌ Opção inválida!")

def criar_pedido():
    pedidos = ler_arquivo(PEDIDOS_FILE)
    
    novo_pedido = {
        'id': len(pedidos) + 1,
        'usuario_id': usuario_logado['id'],
        'usuario_nome': usuario_logado['nome'],
        'alimentos': [],
        'total': 0.0,
        'status': 'Em andamento',
        'data_criacao': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    pedidos.append(novo_pedido)
    escrever_arquivo(PEDIDOS_FILE, pedidos)
    
    print(f"✅ Pedido #{novo_pedido['id']} criado com sucesso!")
    return novo_pedido['id']

def editar_pedido():
    pedido_id = int(input("Digite o ID do pedido que deseja editar: "))
    
    pedidos = ler_arquivo(PEDIDOS_FILE)
    
    for pedido in pedidos:
        if pedido['id'] == pedido_id and pedido['usuario_id'] == usuario_logado['id']:
            print(f"\nEditando Pedido #{pedido_id}")
            print("Alimentos atuais:", [f"{a['nome']} (R${a['preco']:.2f})" for a in pedido['alimentos']])
            
            novo_status = input("Novo status (Enter para manter atual): ").strip()
            if novo_status:
                pedido['status'] = novo_status
            
            # Recalcular total
            pedido['total'] = sum(alimento['preco'] for alimento in pedido['alimentos'])
            
            escrever_arquivo(PEDIDOS_FILE, pedidos)
            print("✅ Pedido atualizado com sucesso!")
            return
    
    print("❌ Pedido não encontrado ou você não tem permissão para editá-lo!")

def excluir_pedido():
    pedido_id = int(input("Digite o ID do pedido que deseja excluir: "))
    
    pedidos = ler_arquivo(PEDIDOS_FILE)
    pedidos_restantes = []
    pedido_encontrado = False
    
    for pedido in pedidos:
        if pedido['id'] == pedido_id:
            if pedido['usuario_id'] == usuario_logado['id']:
                pedido_encontrado = True
                continue  # Não adiciona à lista (exclui)
            else:
                print("❌ Você não tem permissão para excluir este pedido!")
                return
        pedidos_restantes.append(pedido)
    
    if pedido_encontrado:
        escrever_arquivo(PEDIDOS_FILE, pedidos_restantes)
        print("✅ Pedido excluído com sucesso!")
    else:
        print("❌ Pedido não encontrado!")

def adicionar_alimento_pedido():
    pedido_id = int(input("Digite o ID do pedido: "))
    
    pedidos = ler_arquivo(PEDIDOS_FILE)
    alimentos = ler_arquivo(ALIMENTOS_FILE)
    
    for pedido in pedidos:
        if pedido['id'] == pedido_id and pedido['usuario_id'] == usuario_logado['id']:
            listar_informacoes_alimentos(alimentos)
            alimento_id = int(input("\nDigite o ID do alimento que deseja adicionar: "))
            
            alimento_encontrado = None
            for alimento in alimentos:
                if alimento['id'] == alimento_id:
                    alimento_encontrado = alimento
                    break
            
            if alimento_encontrado:
                pedido['alimentos'].append(alimento_encontrado)
                pedido['total'] = sum(alimento['preco'] for alimento in pedido['alimentos'])
                
                escrever_arquivo(PEDIDOS_FILE, pedidos)
                print(f"✅ {alimento_encontrado['nome']} adicionado ao pedido!")
                return
            else:
                print("❌ Alimento não encontrado!")
                return
    
    print("❌ Pedido não encontrado ou você não tem permissão!")

def remover_alimento_pedido():
    pedido_id = int(input("Digite o ID do pedido: "))
    
    pedidos = ler_arquivo(PEDIDOS_FILE)
    
    for pedido in pedidos:
        if pedido['id'] == pedido_id and pedido['usuario_id'] == usuario_logado['id']:
            if not pedido['alimentos']:
                print("❌ Este pedido não contém alimentos!")
                return
            
            print("Alimentos no pedido:")
            for i, alimento in enumerate(pedido['alimentos'], 1):
                print(f"{i}. {alimento['nome']} - R${alimento['preco']:.2f}")
            
            try:
                indice = int(input("Digite o número do alimento que deseja remover: ")) - 1
                if 0 <= indice < len(pedido['alimentos']):
                    alimento_removido = pedido['alimentos'].pop(indice)
                    pedido['total'] = sum(alimento['preco'] for alimento in pedido['alimentos'])
                    
                    escrever_arquivo(PEDIDOS_FILE, pedidos)
                    print(f"✅ {alimento_removido['nome']} removido do pedido!")
                else:
                    print("❌ Número inválido!")
            except ValueError:
                print("❌ Digite um número válido!")
            return
    
    print("❌ Pedido não encontrado ou você não tem permissão!")

def listar_meus_pedidos():
    pedidos = ler_arquivo(PEDIDOS_FILE)
    meus_pedidos = [p for p in pedidos if p['usuario_id'] == usuario_logado['id']]
    
    if not meus_pedidos:
        print("❌ Você não tem pedidos cadastrados!")
        return
    
    print(f"\n=== MEUS PEDIDOS ({len(meus_pedidos)}) ===")
    for pedido in meus_pedidos:
        print(f"\n📦 Pedido #{pedido['id']}")
        print(f"   Status: {pedido['status']}")
        print(f"   Data: {pedido['data_criacao']}")
        print(f"   Total: R${pedido['total']:.2f}")
        print("   Alimentos:")
        for alimento in pedido['alimentos']:
            print(f"     - {alimento['nome']} (R${alimento['preco']:.2f})")

# Funcionalidade 6: Avaliar Pedido
def avaliar_pedido():
    global usuario_logado
    
    if not usuario_logado:
        print("❌ Você precisa estar logado para avaliar um pedido!")
        return
    
    pedidos = ler_arquivo(PEDIDOS_FILE)
    meus_pedidos = [p for p in pedidos if p['usuario_id'] == usuario_logado['id'] and p['status'] == 'Entregue']
    
    if not meus_pedidos:
        print("❌ Você não tem pedidos entregues para avaliar!")
        return
    
    print("\n=== AVALIAR PEDIDO ===")
    listar_meus_pedidos()
    
    try:
        pedido_id = int(input("\nDigite o ID do pedido que deseja avaliar: "))
        
        # Verificar se o pedido existe e pertence ao usuário
        pedido_avaliar = None
        for pedido in meus_pedidos:
            if pedido['id'] == pedido_id:
                pedido_avaliar = pedido
                break
        
        if not pedido_avaliar:
            print("❌ Pedido não encontrado ou não está disponível para avaliação!")
            return
        
        # Verificar se já existe avaliação
        avaliacoes = ler_arquivo(AVALIACOES_FILE)
        for avaliacao in avaliacoes:
            if avaliacao['pedido_id'] == pedido_id:
                print("❌ Este pedido já foi avaliado!")
                return
        
        # Solicitar avaliação
        while True:
            try:
                estrelas = int(input("Digite a avaliação (0-5 estrelas): "))
                if 0 <= estrelas <= 5:
                    break
                else:
                    print("❌ Digite um número entre 0 e 5!")
            except ValueError:
                print("❌ Digite um número válido!")
        
        comentario = input("Digite um comentário (opcional): ").strip()
        
        nova_avaliacao = {
            'id': len(avaliacoes) + 1,
            'pedido_id': pedido_id,
            'usuario_id': usuario_logado['id'],
            'usuario_nome': usuario_logado['nome'],
            'estrelas': estrelas,
            'comentario': comentario,
            'data_avaliacao': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        avaliacoes.append(nova_avaliacao)
        escrever_arquivo(AVALIACOES_FILE, avaliacoes)
        
        print("✅ Avaliação registrada com sucesso!")
        
    except ValueError:
        print("❌ Digite um ID válido!")

# Função adicional para ver avaliações
def ver_minhas_avaliacoes():
    global usuario_logado
    
    if not usuario_logado:
        return
    
    avaliacoes = ler_arquivo(AVALIACOES_FILE)
    minhas_avaliacoes = [a for a in avaliacoes if a['usuario_id'] == usuario_logado['id']]
    
    if not minhas_avaliacoes:
        print("❌ Você não tem avaliações registradas!")
        return
    
    print(f"\n=== MINHAS AVALIAÇÕES ({len(minhas_avaliacoes)}) ===")
    for avaliacao in minhas_avaliacoes:
        estrelas = "⭐" * avaliacao['estrelas'] + "☆" * (5 - avaliacao['estrelas'])
        print(f"\n📝 Pedido #{avaliacao['pedido_id']}")
        print(f"   Avaliação: {estrelas} ({avaliacao['estrelas']}/5)")
        if avaliacao['comentario']:
            print(f"   Comentário: {avaliacao['comentario']}")
        print(f"   Data: {avaliacao['data_avaliacao']}")

# Menu principal
def menu_principal():
    global usuario_logado
    
    while True:
        print("\n" + "="*40)
        print("          FEIFOOD - 22.225.029-2")
        print("="*40)
        
        if usuario_logado:
            print(f"👤 Usuário: {usuario_logado['nome']}")
            print("1. Buscar Alimento")
            print("2. Listar Todos os Alimentos")
            print("3. Gerenciar Pedidos")
            print("4. Avaliar Pedido")
            print("5. Ver Minhas Avaliações")
            print("6. Logout")
            print("7. Sair")
        else:
            print("1. Cadastrar Novo Usuário")
            print("2. Login")
            print("3. Buscar Alimento")
            print("4. Listar Todos os Alimentos")
            print("5. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if usuario_logado:
            if opcao == "1":
                resultados = buscar_alimento()
                if resultados:
                    listar_informacoes_alimentos(resultados)
            elif opcao == "2":
                listar_informacoes_alimentos()
            elif opcao == "3":
                cadastrar_pedido()
            elif opcao == "4":
                avaliar_pedido()
            elif opcao == "5":
                ver_minhas_avaliacoes()
            elif opcao == "6":
                usuario_logado = None
                print("✅ Logout realizado com sucesso!")
            elif opcao == "7":
                print("👋 Obrigado por usar nosso sistema!")
                break
            else:
                print("❌ Opção inválida!")
        else:
            if opcao == "1":
                cadastrar_usuario()
            elif opcao == "2":
                login_usuario()
            elif opcao == "3":
                resultados = buscar_alimento()
                if resultados:
                    listar_informacoes_alimentos(resultados)
            elif opcao == "4":
                listar_informacoes_alimentos()
            elif opcao == "5":
                print("👋 Obrigado por usar nosso sistema!")
                break
            else:
                print("❌ Opção inválida!")

# Função principal
def main():
    inicializar_arquivos()
    print("🚀 Sistema inicializado com sucesso!")
    menu_principal()

if __name__ == "__main__":
    main()