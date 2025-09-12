import pandas as pd
import re
import os


def criar_dataframe_de_arquivo_latex(caminho_arquivo, numero_lista):
    """
    Processa um arquivo LaTeX com questões em `enumerate` e itens aninhados.

    Args:
        caminho_arquivo (str): O caminho para o arquivo LaTeX.
        numero_lista (int): O número da lista de questões.

    Returns:
        pd.DataFrame: Um DataFrame com os dados das questões e itens.
    """
    dados_perguntas = []

    try:
        with open(caminho_arquivo, 'r', encoding='latin-1') as f:
            conteudo_completo = f.read()

        bloco_questoes = re.search(r'\\begin{enumerate}(.*?)\\end{enumerate}', conteudo_completo, re.DOTALL)
        if not bloco_questoes:
            print("Erro: Bloco de 'enumerate' não encontrado.")
            return []

        conteudo_questoes_limpo = bloco_questoes.group(1).strip()
        blocos_encontrados = re.split(r'(\\item(?!\[))', conteudo_questoes_limpo, flags=re.DOTALL)
        # Remove a primeira string vazia
        blocos_encontrados = blocos_encontrados[1:]
        for i in range(0, len(blocos_encontrados), 2):
            numero_questao = int(i / 2) + 1  # A contagem agora é precisa

            texto_bloco_completo = blocos_encontrados[i + 1].strip()

            texto_sem_itemize = texto_bloco_completo.replace(r'\begin{itemize}', '').replace(r'\end{itemize}',
                                                                                             '').strip()

            # Processa os subitens se houver a tag \item[a)]
            if r'\item[a)]' in texto_bloco_completo:
                # Usa re.findall para capturar os pares de item e texto
                sub_itens_encontrados = re.findall(r'\\item\[([a-z])\)](.*?)(?=\\item\[|\Z)', texto_sem_itemize,
                                                   re.DOTALL)

                for numero_item_letra, texto_solucao in sub_itens_encontrados:
                    id_quest = f'l{numero_lista}q{numero_questao}i{numero_item_letra}'

                    dados_perguntas.append({
                        'id_quest': id_quest,
                        'numero_lista': numero_lista,
                        'numero_questao': numero_questao,
                        'numero_item': numero_item_letra,
                        'texto_solucao': texto_solucao.strip()
                    })
            else:
                # Se não tem subitens, o bloco inteiro é a solução
                id_quest = f'l{numero_lista}q{numero_questao}'
                dados_perguntas.append({
                    'id_quest': id_quest,
                    'numero_lista': numero_lista,
                    'numero_questao': numero_questao,
                    'numero_item': None,
                    'texto_solucao': texto_sem_itemize
                })

        return dados_perguntas

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return []
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")
        return []

todos_dados = []

# Loop para processar as listas de 1 a 7
for i in range(1, 8):
    caminho_arquivo = f"/home/gabi/dados/unb/dados-gabi/unb_Semestre_8/james/solucoestxt/solucao{i}.tex"
    numero_lista = i

    # Chama a função para extrair os dados da lista atual
    dados_da_lista = criar_dataframe_de_arquivo_latex(caminho_arquivo, numero_lista)

    # Adiciona os dados da lista atual à lista geral
    todos_dados.extend(dados_da_lista)

# Constrói o DataFrame final com todos os dados
df = pd.DataFrame(todos_dados)

