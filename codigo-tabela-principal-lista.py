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

        padrao_itens_principais = re.compile(
            r'\\item(.*?)(?=\s*\\item(?!\[)|$)',
            re.DOTALL
        )

        todos_itens = padrao_itens_principais.findall(conteudo_questoes_limpo)
        print(todos_itens)

        itemize_pattern = re.compile(r'\\begin\{itemize\}(.*?)\\end\{itemize\}', re.DOTALL)

        # corresponde exatamente aos \item[...] cujo conteúdo dos colchetes começa por uma letra
        # (ex: \item[a)] , \item[ a ) ] etc.). Em seguida captura até o próximo \item, \item[ ou \end{itemize}.
        labeled_subitem_pattern = re.compile(
            r'\\item\[\s*(?:\([a-z]\)|[a-z]\))\s*\].*?(?=(?:\\item\[|\\item\b|\\end\{itemize\}|$))',
            re.DOTALL
        )

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return []

    for i, texto_item in enumerate(todos_itens):
        id_quest = f'l{numero_lista}q{i + 1}'

        # função de callback para limpar cada bloco itemize separadamente
        def _clean_itemize_block(match):
            inner = match.group(1)  # conteúdo entre \begin{itemize} e \end{itemize}
            # remove apenas os subitens que começam com uma letra dentro dos colchetes
            cleaned_inner = labeled_subitem_pattern.sub('', inner)

            # se, depois de remover, não sobrar nenhum \item, removemos todo o bloco itemize
            if not re.search(r'\\item\b', cleaned_inner):
                return ''
            # caso contrário, reconstruímos o ambiente itemize com o conteúdo limpo
            return r'\begin{itemize}' + cleaned_inner + r'\end{itemize}'

        # aplica a limpeza em TODOS os blocos itemize do texto_item
        pergunta_sem_subitens = itemize_pattern.sub(_clean_itemize_block, texto_item)
        pergunta_final = pergunta_sem_subitens.strip()

        # debug: mostra o texto processado (remova/ comente esse print quando não precisar)


        dados_perguntas.append({
            'id_quest': id_quest,
            'numero_lista': numero_lista,
            'numero_questao': i + 1,
            'pergunta_principal': pergunta_final
        })

    return dados_perguntas


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


