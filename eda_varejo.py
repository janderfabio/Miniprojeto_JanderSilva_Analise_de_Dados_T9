"""
================================================================================
MINIPROJETO - ANALISE EXPLORATORIA DE DADOS (EDA) - BASE VAREJO
================================================================================

Aluno: Jander Silva
Turma: Analise_de_Dados_T9

Sprints:
  Sprint 1 (concluido): Importacao dos dados
  Sprint 2 (concluido): Transformacao de tipos (string, int, float, datetime)
  Sprint 3 (concluido): Limpeza de nulos e duplicatas
  Sprint 4 (concluido): Estatistica descritiva (CL_FHL)
  Sprint 5 (atual): Relatorio e documentacao
================================================================================
"""

import os
import sys
import re
import pandas as pd
import numpy as np


CAMINHO_CSV = "Base_varejo.csv"
SEPARADOR = ";"
ENCODING = "utf-8"


def separador(titulo: str) -> None:
    """Imprime um separador visual para organizar a saida no console."""
    print("\n" + "=" * 80)
    print(titulo)
    print("=" * 80)


# ===========================================================================
# SPRINT 1 - IMPORTACAO DOS DADOS
# ===========================================================================
def carregar_base(caminho: str) -> pd.DataFrame:
    """
    SPRINT 1 - Importacao dos dados.

    Carrega o arquivo Base_varejo.csv no pandas.

    Detalhes:
    - sep=';' porque o arquivo e separado por ponto-e-virgula.
    - dtype=str para ler tudo como texto inicialmente.
    - Remove colunas totalmente vazias (sobrantes do cabecalho ;;;;).
    - Remove espacos nos nomes das colunas.
    """
    if not os.path.exists(caminho):
        print(f"ERRO: arquivo '{caminho}' nao encontrado.")
        sys.exit(1)

    df = pd.read_csv(
        caminho,
        sep=SEPARADOR,
        encoding=ENCODING,
        dtype=str,
    )

    df = df.dropna(axis=1, how="all")
    df.columns = df.columns.str.strip()

    return df


def mostrar_carga(df: pd.DataFrame) -> None:
    """Exibe numero de registros, colunas, tipos e amostra (Sprint 1)."""
    separador("SPRINT 1 - IMPORTACAO DOS DADOS")

    print(f"Arquivo carregado: {CAMINHO_CSV}")
    print(f"\nNumero de registros (linhas): {df.shape[0]}")
    print(f"Numero de colunas: {df.shape[1]}")

    print("\nColunas e tipos de dados (apos importacao, tudo como string):")
    print(df.dtypes.to_string())

    print("\nPrimeiras 5 linhas (amostra):")
    print(df.head().to_string())


# ===========================================================================
# SPRINT 2 - TRANSFORMACAO DE TIPOS (STRING, INT, FLOAT, DATETIME)
# ===========================================================================
def limpar_texto(valor):
    """
    SPRINT 2 - Limpeza de texto.

    Aplica expressoes regulares para padronizar strings:
    - Remove espacos em branco nas extremidades.
    - Converte para maiusculas.
    - Substitui espacos multiples por um unico espaco.
    """
    if pd.isna(valor):
        return valor
    texto = str(valor).strip()
    texto = re.sub(r"\s+", " ", texto)
    texto = texto.upper()
    return texto


def converter_para_numerico(serie: pd.Series) -> pd.Series:
    """
    SPRINT 2 - Transformacao para inteiro/float.

    Converte uma serie de texto para numerico usando pd.to_numeric.
    Valores invalidos viram NaN.
    """
    return pd.to_numeric(serie, errors="coerce")


def converter_para_datetime(serie: pd.Series, coluna: str) -> pd.Series:
    """
    SPRINT 2 - Transformacao para datetime.

    Converte uma serie de texto (formato DD/MM/YYYY) para datetime64[ns].
    Usa dayfirst=True para interpretar o formato brasileiro.
    Valores invalidos viram NaT.
    """
    return pd.to_datetime(serie, dayfirst=True, errors="coerce")


def aplicar_transformacoes_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """
    SPRINT 2 - Aplica todas as transformacoes de tipo no DataFrame.
    """
    separador("SPRINT 2 - TRANSFORMACAO DE TIPOS (STRING, INT, FLOAT, DATETIME)")

    print("\n[2a] Limpeza de texto (expressoes regulares):")
    colunas_texto = ["CL_GENERO", "CL_SEG", "PR_CAT", "PR_NOME"]
    for col in colunas_texto:
        if col in df.columns:
            antes = df[col].astype(str).str.strip().tolist()
            df[col] = df[col].apply(limpar_texto)
            depois = df[col].astype(str).tolist()
            alteradas = sum(1 for a, b in zip(antes, depois) if a != b)
            print(f"  - {col}: {alteradas} valor(es) padronizado(s) via regex.")

    print("\n[2b] Conversao de colunas numericas (int/float):")
    colunas_numericas = ["CO_ID", "CL_ID", "CL_EC", "CL_FHL", "PR_ID"]
    for col in colunas_numericas:
        if col in df.columns:
            df[col] = converter_para_numerico(df[col])
            nans = int(df[col].isna().sum())
            print(f"  - {col}: convertido para numerico ({nans} valor(es) invalido(es) viraram NaN).")

    print("\n[2c] Conversao de coluna DATA para datetime:")
    if "DATA" in df.columns:
        df["DATA"] = converter_para_datetime(df["DATA"], "DATA")
        invalidos = int(df["DATA"].isna().sum())
        print(f"  - DATA: convertido para datetime64[ns] ({invalidos} valor(es) invalido(es) viraram NaT).")

    print("\nTipos apos transformacoes do Sprint 2:")
    print(df.dtypes.to_string())

    return df


# ===========================================================================
# SPRINT 3 - LIMPEZA DE NULOS E DUPLICATAS
# ===========================================================================
def tratar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """
    SPRINT 3 - Limpeza de nulos.

    Estrategia:
    - Colunas criticas (DATA, PR_ID, CO_ID, CL_ID): remove linhas com nulos.
    - PR_CAT e PR_NOME: preenche com 'DESCONHECIDO'.
    - Atributos do cliente (CL_GENERO, CL_SEG, CL_EC, CL_FHL): imputa com
      a moda do proprio cliente (CL_ID); se nao houver, usa a moda global.
    """
    print("\n[3a] Tratamento de valores nulos / ausentes:")

    df = df.replace(r"^\s*$", np.nan, regex=True)
    df = df.replace(["#N/D", "ND", "N/D", "nan", "NaN"], np.nan)

    colunas_criticas = ["DATA", "PR_ID", "CO_ID", "CL_ID"]
    colunas_existentes_criticas = [c for c in colunas_criticas if c in df.columns]

    if colunas_existentes_criticas:
        antes = len(df)
        df = df.dropna(subset=colunas_existentes_criticas)
        depois = len(df)
        print(
            f"  - Linhas removidas por nulos em colunas criticas "
            f"({colunas_existentes_criticas}): {antes - depois}"
        )

    for col in ["PR_CAT", "PR_NOME"]:
        if col in df.columns:
            qtd_nan = int(df[col].isna().sum())
            if qtd_nan > 0:
                df[col] = df[col].fillna("DESCONHECIDO")
                print(f"  - {col}: {qtd_nan} nulos imputados como 'DESCONHECIDO'.")

    for col in ["CL_GENERO", "CL_SEG", "CL_EC", "CL_FHL"]:
        if col in df.columns:
            qtd_nan = int(df[col].isna().sum())
            if qtd_nan > 0:
                moda_por_cliente = df.groupby("CL_ID")[col].transform(
                    lambda s: s.mode().iloc[0] if not s.mode().empty else np.nan
                )
                df[col] = df[col].fillna(moda_por_cliente)
                moda_global = df[col].mode()
                if not moda_global.empty:
                    df[col] = df[col].fillna(moda_global.iloc[0])
                print(
                    f"  - {col}: {qtd_nan} nulos imputados (moda do cliente / moda global)."
                )

    return df


def remover_duplicatas(df: pd.DataFrame) -> pd.DataFrame:
    """
    SPRINT 3 - Remocao de duplicatas.

    - Remove linhas duplicadas completas.
    - Remove duplicatas por identificacao da transacao
      (CO_ID, CL_ID, DATA, PR_ID), mantendo a primeira ocorrencia.
    """
    print("\n[3b] Remocao de duplicatas:")

    antes = len(df)
    df = df.drop_duplicates()
    depois_todas = len(df)
    print(f"  - Linhas duplicadas completas removidas: {antes - depois_todas}")

    colunas_id = [c for c in ["CO_ID", "CL_ID", "DATA", "PR_ID"] if c in df.columns]
    if colunas_id:
        antes2 = len(df)
        df = df.drop_duplicates(subset=colunas_id, keep="first")
        print(
            f"  - Linhas duplicadas por transacao ({colunas_id}) removidas: "
            f"{antes2 - len(df)}"
        )

    print(f"  - Registros apos limpeza de duplicatas: {len(df)} (eram {antes})")
    return df


def aplicar_limpeza_nulos_duplicatas(df: pd.DataFrame) -> pd.DataFrame:
    """SPRINT 3 - Orquestra a limpeza de nulos e duplicatas."""
    separador("SPRINT 3 - LIMPEZA DE NULOS E DUPLICATAS")
    df = tratar_nulos(df)
    df = remover_duplicatas(df)
    return df


# ===========================================================================
# SPRINT 4 - ESTATISTICA DESCRITIVA (NUMERO DE FILHOS)
# ===========================================================================
def estatisticas_filhos(df: pd.DataFrame) -> None:
    """
    SPRINT 4 - Estatistica descritiva.

    Calcula e exibe para a coluna CL_FHL (numero de filhos do cliente):
    - Contagem
    - Media
    - Mediana
    - Desvio padrao
    - Moda
    - Minimo
    - Maximo
    - Quartis (25%, 50%, 75%)
    - Distribuicao de frequencia
    """
    separador("SPRINT 4 - ESTATISTICA DESCRITIVA: NUMERO DE FILHOS (CL_FHL)")

    col = "CL_FHL"
    if col not in df.columns:
        print(f"Coluna '{col}' nao encontrada na base.")
        return

    serie = df[col].dropna()

    print(f"\nColuna analisada: {col} (numero de filhos do cliente)")
    print(f"Contagem de registros validos: {serie.count()}")
    print(f"Media: {serie.mean():.2f}")
    print(f"Mediana: {serie.mediana():.2f}")
    print(f"Desvio padrao: {serie.std():.2f}")
    print(f"Moda: {serie.mode().iloc[0] if not serie.mode().empty else 'N/A'}")
    print(f"Minimo: {serie.min()}")
    print(f"Maximo: {serie.max()}")

    print("\nQuartis (describe):")
    print(serie.describe().to_string())

    print("\nDistribuicao de frequencia por numero de filhos:")
    print(serie.value_counts().sort_index().to_string())


# ===========================================================================
# SPRINT 5 - RELATORIO E DOCUMENTACAO
# ===========================================================================
def agrupamentos(df: pd.DataFrame) -> None:
    """
    SPRINT 5 - Relatorio: padroes de agrupamento.

    Exibe:
    - Vendas por genero (groupby)
    - Top 10 categorias por itens vendidos
    - Pivot_table: segmento x genero
    - Media de filhos por segmento e genero
    """
    print("\n[5a] Vendas por genero do cliente:")
    if "CL_GENERO" in df.columns:
        vendas_genero = (
            df.groupby("CL_GENERO")
            .agg(
                qtd_vendas=("PR_ID", "count"),
                qtd_clientes=("CL_ID", "nunique"),
            )
            .sort_values("qtd_vendas", ascending=False)
        )
        print(vendas_genero.to_string())

        total = vendas_genero["qtd_vendas"].sum()
        vendas_genero["participacao_%"] = (vendas_genero["qtd_vendas"] / total * 100).round(2)
        print("\nParticipacao percentual de vendas por genero:")
        print(vendas_genero[["participacao_%"]].to_string())

    print("\n[5b] Top 10 categorias por quantidade de itens vendidos:")
    if "PR_CAT" in df.columns:
        cat_vendas = (
            df.groupby("PR_CAT")
            .size()
            .reset_index(name="qtd_itens")
            .sort_values("qtd_itens", ascending=False)
            .head(10)
        )
        print(cat_vendas.to_string(index=False))

    print("\n[5c] Pivot_table: Segmento (CL_SEG) x Genero (CL_GENERO) - qtd de compras:")
    if {"CL_SEG", "CL_GENERO"}.issubset(df.columns):
        pivot = pd.pivot_table(
            df,
            index="CL_SEG",
            columns="CL_GENERO",
            values="PR_ID",
            aggfunc="count",
            fill_value=0,
        )
        print(pivot.to_string())

    print("\n[5d] Media de numero de filhos (CL_FHL) por segmento e genero:")
    if {"CL_SEG", "CL_GENERO", "CL_FHL"}.issubset(df.columns):
        media_filhos = (
            df.groupby(["CL_SEG", "CL_GENERO"])["CL_FHL"]
            .mean()
            .round(2)
            .unstack(fill_value=0)
        )
        print(media_filhos.to_string())


def gerar_contadores_relatorio(df: pd.DataFrame, relatorio: dict) -> None:
    """
    SPRINT 5 - Contadores do relatorio final.

    Exibe resumo quantitativo das principais metricas da base limpa.
    """
    separador("SPRINT 5 - RELATORIO E DOCUMENTACAO: CONTADORES FINAIS")

    print("\nResumo quantitativo da base apos limpeza:")
    print(f"  - Total de registros: {len(df)}")
    print(f"  - Total de colunas: {df.shape[1]}")
    print(f"  - Clientes unicos (CL_ID): {df['CL_ID'].nunique() if 'CL_ID' in df.columns else 'N/A'}")
    print(f"  - Pedidos unicos (CO_ID): {df['CO_ID'].nunique() if 'CO_ID' in df.columns else 'N/A'}")
    print(f"  - Produtos unicos (PR_ID): {df['PR_ID'].nunique() if 'PR_ID' in df.columns else 'N/A'}")
    print(f"  - Categorias unicas: {df['PR_CAT'].nunique() if 'PR_CAT' in df.columns else 'N/A'}")

    if "CL_GENERO" in df.columns:
        generos = df["CL_GENERO"].value_counts()
        print(f"  - Distribuicao por genero: {generos.to_dict()}")

    if "DATA" in df.columns:
        print(f"  - Periodo: {df['DATA'].min()} ate {df['DATA'].max()}")
        print(f"  - Datas unicas: {df['DATA'].nunique()}")


def conclusoes(df: pd.DataFrame, relatorio: dict) -> None:
    """
    SPRINT 5 - Bloco de conclusoes (3-6 topicos).

    Apresenta os principais insights obtidos e problemas remanescentes.
    """
    print("\nPrincipais insights obtidos:")

    insights = []

    if "CL_GENERO" in df.columns:
        vendas_genero = df.groupby("CL_GENERO").size().sort_values(ascending=False)
        genero_top = vendas_genero.idxmax()
        pct_top = round(vendas_genero.iloc[0] / vendas_genero.sum() * 100, 2)
        insights.append(
            f"1. Genero com mais vendas: {genero_top} responde por {pct_top}% "
            f"dos itens vendidos ({vendas_genero.iloc[0]} de {vendas_genero.sum()})."
        )

    if "PR_CAT" in df.columns:
        cat_series = df.groupby("PR_CAT").size().sort_values(ascending=False)
        cat_nome = cat_series.index[0]
        cat_top = int(cat_series.iloc[0])
        insights.append(
            f"2. Categoria de produto com mais itens vendidos: '{cat_nome}' "
            f"({cat_top} itens)."
        )

    if "CL_FHL" in df.columns:
        media_filhos = df["CL_FHL"].mean()
        moda_filhos = df["CL_FHL"].mode().iloc[0]
        insights.append(
            f"3. O cliente da base tem, em media, {media_filhos:.2f} filho(s); "
            f"a moda e {moda_filhos} filho(s)."
        )

    if "CL_SEG" in df.columns:
        seg_series = df.groupby("CL_SEG").size().sort_values(ascending=False)
        seg_top = seg_series.index[0]
        insights.append(
            f"4. O segmento de cliente com maior volume de compras e '{seg_top}'."
        )

    if relatorio.get("datas_unicas", 1) == 1:
        insights.append(
            "5. A base contem apenas uma data, limitando analises de tendencia temporal."
        )

    for i in insights:
        print(i)

    print("\nProblemas remanescentes / pontos de atencao:")

    problemas = []

    if relatorio.get("categorias_invalidas", 0) > 0:
        problemas.append(
            f"- Ainda existem {relatorio['categorias_invalidas']} registros com categoria/produto "
            "marcados como '#N/D' ou ausentes (preenchidos com 'DESCONHECIDO', mas devem ser revisados)."
        )

    problemas.append(
        "- Nao existe coluna de preco/quantidade/valor unitario; analise baseada em contagem de itens."
    )

    problemas.append(
        "- Baixa variacao temporal na coluna DATA, limitando RFM e sazonalidade."
    )

    for p in problemas:
        print(p)

    print("\nRecomendacao: coletar mais historico de datas e incluir colunas de preco e quantidade.")


def aplicar_relatorio_documentacao(df: pd.DataFrame, relatorio: dict) -> None:
    """SPRINT 5 - Orquestra geracao de contadores e conclusoes."""
    separador("SPRINT 5 - RELATORIO E DOCUMENTACAO")
    gerar_contadores_relatorio(df, relatorio)
    agrupamentos(df)
    conclusoes(df, relatorio)


# ===========================================================================
# SPRINT 6 - VERSIONAMENTO
# ===========================================================================
# Este sprint nao contem codigo no script, pois se refere ao envio dos arquivos
# via Git para o repositorio no GitHub. Os arquivos a serem enviados sao:
#   - eda_varejo.py
#   - README.md
#   - README_JanderSilva_Analise_de_Dados_T9.md
#   - Base_varejo.csv (opcional, dependendo do tamanho / LFS)


# ===========================================================================
# MAIN (Sprints 1 a 5)
# ===========================================================================
def main() -> None:
    print("Iniciando Analise Exploratoria de Dados - Base Varejo")
    print("Sprints 1 a 5 executados no script; Sprint 6 via Git/GitHub")

    df = carregar_base(CAMINHO_CSV)
    mostrar_carga(df)
    df = aplicar_transformacoes_tipos(df)
    df = aplicar_limpeza_nulos_duplicatas(df)

    # Ajuste final de tipos apos limpeza (categoricos)
    colunas_categoricas = ["CL_GENERO", "CL_SEG", "PR_CAT", "PR_NOME"]
    for col in colunas_categoricas:
        if col in df.columns:
            df[col] = df[col].astype("category")

    # Relatorio de problemas (para uso no Sprint 5)
    relatorio = {
        "categorias_invalidas": 0,
        "datas_unicas": int(df["DATA"].nunique()) if "DATA" in df.columns else 0,
    }

    print("\n" + "=" * 80)
    print(f"Registros apos todas as limpezas: {len(df)}")
    print("=" * 80 + "\n")

    estatisticas_filhos(df)
    aplicar_relatorio_documentacao(df, relatorio)

    print("\n" + "=" * 80)
    print("Fim do script. Analise concluida com sucesso (Sprints 1 a 5 executados).")
    print("Sprint 6 (versionamento) deve ser realizado via Git no repositorio GitHub.")
    print("=" * 80)


if __name__ == "__main__":
    main()
