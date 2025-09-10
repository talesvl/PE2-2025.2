import re
import pandas as pd


def extrair_perguntas_corretamente(caminho_arquivo, numero_lista):

    dados_perguntas = []

    try:
        with open(caminho_arquivo, 'r', encoding='latin-1') as f:
            conteudo_completo = f.read()

        bloco_questoes = re.search(r'\\begin{enumerate}(.*?)\\end{enumerate}', conteudo_completo, re.DOTALL)

        if not bloco_questoes:
            print("Erro: Bloco de 'enumerate' não encontrado.")
            return []

        conteudo_questoes_limpo = bloco_questoes.group(1)

        partes = re.split(r'\\gabilinda', conteudo_questoes_limpo, maxsplit=1)


        blocos = re.split(r'(\\item)', partes[0])


        blocos = blocos[1:]

        itens_agrupados = []
        bloco_atual = ""
        nivel_aninhamento = 0

        for i in range(0, len(blocos), 2):
            delimitador = blocos[i]
            texto_bloco = blocos[i + 1]


            bloco_atual += delimitador + texto_bloco


            nivel_aninhamento += len(re.findall(r'\\begin\{itemize\}', texto_bloco))
            nivel_aninhamento -= len(re.findall(r'\\end\{itemize\}', texto_bloco))


            if nivel_aninhamento == 0 and i + 2 < len(blocos):
                itens_agrupados.append(bloco_atual.strip())
                bloco_atual = ""
            elif i + 2 >= len(blocos):

                itens_agrupados.append(bloco_atual.strip())

    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return []


    for i, texto_item in enumerate(itens_agrupados):
        dados_perguntas.append({
            'numero_lista': numero_lista,
            'numero_questao': i + 1,
            'texto_pergunta': texto_item  # Usamos o texto_item que está correto
        })

    return dados_perguntas


dados = extrair_perguntas_corretamente("/home/gabi/dados/unb/dados-gabi/unb_Semestre_8/james/arquivostxt/lista1.tex", 1)

df = pd.DataFrame(dados)


