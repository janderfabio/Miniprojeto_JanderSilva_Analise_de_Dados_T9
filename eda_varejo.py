"""
================================================================================
MINIPROJETO - ANALISE EXPLORATORIA DE DADOS (EDA) - BASE VAREJO
================================================================================

Aluno: Jander Silva
Turma: Analise_de_Dados_T9

Sprints:
  Sprint 1 (concluido): Importacao dos dados
  Sprint 2 (atual): Transformacao de tipos (string, int, float, datetime)
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
# MAIN (Sprints 1 e 2)
# ===========================================================================
def main() -> None:
    print("Iniciando Analise Exploratoria de Dados - Base Varejo")
    print("Sprints 1 e 2")

    df = carregar_base(CAMINHO_CSV)
    mostrar_carga(df)
    df = aplicar_transformacoes_tipos(df)

    print("\nFim dos Sprints 1 e 2.")


if __name__ == "__main__":
    main()
