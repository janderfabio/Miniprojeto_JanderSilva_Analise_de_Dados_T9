"""
================================================================================
MINIPROJETO - ANALISE EXPLORATORIA DE DADOS (EDA) - BASE VAREJO
================================================================================

Aluno: Jander Silva
Turma: Analise_de_Dados_T9

Sprints:
  Sprint 1 (concluido): Importacao dos dados
  Sprint 2 (concluido): Transformacao de tipos (string, int, float, datetime)
  Sprint 3 (atual): Limpeza de nulos e duplicatas
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
# MAIN (Sprints 1, 2 e 3)
# ===========================================================================
def main() -> None:
    print("Iniciando Analise Exploratoria de Dados - Base Varejo")
    print("Sprints 1, 2 e 3")

    df = carregar_base(CAMINHO_CSV)
    mostrar_carga(df)
    df = aplicar_transformacoes_tipos(df)
    df = aplicar_limpeza_nulos_duplicatas(df)

    print("\nFim dos Sprints 1, 2 e 3.")


if __name__ == "__main__":
    main()
