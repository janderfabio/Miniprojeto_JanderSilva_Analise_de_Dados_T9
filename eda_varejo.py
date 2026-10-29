"""
================================================================================
MINIPROJETO - ANALISE EXPLORATORIA DE DADOS (EDA) - BASE VAREJO
================================================================================

Aluno: Jander Silva
Turma: Analise_de_Dados_T9

Sprint 1 (atual): Importacao dos dados
================================================================================
"""

import os
import sys
import pandas as pd


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
# MAIN (Sprint 1 apenas)
# ===========================================================================
def main() -> None:
    print("Iniciando Analise Exploratoria de Dados - Base Varejo")
    print("Sprint 1 - Importacao dos dados")

    df = carregar_base(CAMINHO_CSV)
    mostrar_carga(df)

    print("\nFim do Sprint 1.")


if __name__ == "__main__":
    main()
