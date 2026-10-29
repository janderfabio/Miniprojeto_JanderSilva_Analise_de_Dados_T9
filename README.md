# Miniprojeto_JanderSilva_Analise_de_Dados_T9

Análise Exploratória de Dados (EDA) da base de varejo `Base_varejo.csv`, desenvolvida em Python com pandas.

## Sobre o projeto

Este mini-projeto realiza uma análise exploratória documentada e reproduzível da base de vendas varejista, organizado em **6 sprints**:

| Sprint | Entrega |
|--------|---------|
| Sprint 1 | Importação dos dados (leitura do CSV com pandas) |
| Sprint 2 | Transformação de tipos (string, int, float, datetime) com regex |
| Sprint 3 | Limpeza de nulos e duplicatas |
| Sprint 4 | Estatística descritiva da coluna CL_FHL (número de filhos) |
| Sprint 5 | Relatório e documentação (contadores finais, agrupamentos, conclusões) |
| Sprint 6 | Versionamento via Git no GitHub |

## Como executar

### No VSCode (arquivo .py)
1. Abra a pasta do projeto no VSCode.
2. Certifique-se de que o arquivo `Base_varejo.csv` está na mesma pasta que `eda_varejo.py`.
3. Instale as dependências:
   ```bash
   pip install pandas numpy
   ```
4. Rode o script:
   ```bash
   python eda_varejo.py
   ```

### No Google Colab
1. Faça upload dos arquivos `eda_varejo.py` e `Base_varejo.csv` para o Colab.
2. Rode todas as células ou execute:
   ```bash
   !python eda_varejo.py
   ```

## Estrutura do repositório

```
Miniprojeto_JanderSilva_Analise_de_Dados_T9/
├── eda_varejo.py          # Script principal de EDA (organizado por sprints)
├── Base_varejo.csv        # Base de dados do varejo
├── README.md              # Este arquivo (instruções gerais)
└── README_JanderSilva_Analise_de_Dados_T9.md  # Instruções específicas do aluno/turma
```

## Tecnologias

- Python 3
- pandas (obrigatório)
- NumPy (opcional)
- re (expressões regulares, padrão do Python)

## Autor

Jander Silva – Turma: Análise de Dados T9
