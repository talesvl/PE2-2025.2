import re
import pandas as pd


def extrair_perguntas_corretamente(caminho_arquivo, numero_lista):
    dados_perguntas = []

    try:
        with open(caminho_arquivo, 'r', encoding='latin-1') as f:
            conteudo_completo = f.read()

        bloco_questoes = re.search(r'\\begin{enumerate}(.*?)\\end{enumerate}', conteudo_completo, re.DOTALL)

        if not bloco_questoes:
            print(f"Erro: Bloco de 'enumerate' não encontrado no arquivo '{caminho_arquivo}'.")
            return []

        conteudo_questoes_limpo = bloco_questoes.group(1)

        # Expressão regular para capturar a pergunta principal antes de uma lista aninhada.
        padrao = re.compile(
            r'\\item(?!\[)(.*?)(?=\s*\\begin\{itemize\}|\s*\\item(?!\[)|$)',
            re.DOTALL
        )
        questoes_texto = padrao.findall(conteudo_questoes_limpo)

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return []

    for i, texto_item in enumerate(questoes_texto):
        # Cria o ID da questão no formato 'l#_q#'
        id_quest = f'l{numero_lista}_q{i + 1}'

        dados_perguntas.append({
            'id_quest': id_quest,
            'numero_lista': numero_lista,
            'numero_questao': i + 1,
            'pergunta_principal': texto_item.strip()
        })

    return dados_perguntas



# Lista para armazenar todos os dados extraídos de todas as listas
todos_dados = []

# Loop para processar as listas de 1 a 7
for i in range(1, 8):
    caminho_arquivo = f"/home/gabi/dados/unb/dados-gabi/unb_Semestre_8/james/arquivostxt/lista{i}.tex"
    numero_lista = i

    # Chama a função para extrair os dados da lista atual
    dados_da_lista = extrair_perguntas_corretamente(caminho_arquivo, numero_lista)

    # Adiciona os dados da lista atual à lista geral
    todos_dados.extend(dados_da_lista)

# Constrói o DataFrame final com todos os dados
df = pd.DataFrame(todos_dados)

