from src.mochila_ic236ep.models import Item, InstanciaMochila

def ler_instancia(caminho_arquivo: str) -> InstanciaMochila:
    """Lê um arquivo .txt e converte para o modelo de dados."""
    itens = []
    
    with open(caminho_arquivo, 'r') as file:
        linhas = file.readlines()
        
        # A primeira linha costuma ter: [numero_de_itens] [capacidade_da_mochila]
        cabecalho = linhas[0].strip().split()
        capacidade = float(cabecalho[1])
        
        # Lendo os itens nas linhas subsequentes: [valor] [peso]
        for id_item, linha in enumerate(linhas[1:]):
            dados = linha.strip().split()
            if len(dados) == 2:
                valor = float(dados[0])
                peso = float(dados[1])
                itens.append(Item(id=id_item, peso=peso, valor=valor))
                
    return InstanciaMochila(capacidade=capacidade, itens=itens)

# Teste rápido
if __name__ == "__main__":
    # Certifique-se de que o ficheiro 'teste.txt' está na mesma pasta
    instancia = ler_instancia("src/mochila_ic236ep/teste.txt")
    print(f"Capacidade da Mochila: {instancia.capacidade}")
    print(f"Total de Itens lidos: {instancia.num_itens}")
    
    # Vamos imprimir o primeiro item para confirmar
    print(f"Primeiro item -> Valor: {instancia.itens[0].valor}, Peso: {instancia.itens[0].peso}")