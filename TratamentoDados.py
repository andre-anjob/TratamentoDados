import pandas as pd
import os

def ler_csv(caminho):
    """Lê um arquivo CSV e retorna um DataFrame, pulando linhas problemáticas."""
    try:
        return pd.read_csv(caminho, sep=';', encoding='utf-8', on_bad_lines='skip')
    except Exception as e:
        print(f"Erro ao processar o arquivo {caminho}: {e}")
        return None

def concatenar_arquivos(pasta, extensao):
    """Concatena arquivos CSV em um DataFrame."""
    todos_os_dataframes = []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(extensao):
            caminho_completo = os.path.join(pasta, arquivo)
            df = ler_csv(caminho_completo)
            if df is not None:
                todos_os_dataframes.append(df)

    return pd.concat(todos_os_dataframes, ignore_index=True) if todos_os_dataframes else None

def encontrar_registros_nao_presentes(pasta_csv1, pasta_csv2):
    """Compara e encontra registros presentes apenas no primeiro conjunto de CSV."""
    if any(not (os.path.exists(p) and os.path.isdir(p)) for p in [pasta_csv1, pasta_csv2]):
        raise FileNotFoundError('Uma ou ambas as pastas não foram encontradas.')

    df_csv1 = concatenar_arquivos(pasta_csv1, '.csv')
    if df_csv1 is None:
        return None

    df_csv2 = concatenar_arquivos(pasta_csv2, '.csv')
    if df_csv2 is None:
        return None

    df_csv2 = df_csv2[df_csv2['identifier'].notna() & (df_csv2['identifier'] != '')]
    df_csv2.rename(columns={'identifier': 'ID', 'call_date': 'DataInclusão'}, inplace=True)

    # Conversão de datas
    for df in [df_csv1, df_csv2]:
        df['DataInclusão'] = pd.to_datetime(df['DataInclusão'], format='%d/%m/%Y', errors='coerce')

    merger_df = pd.merge(df_csv2, df_csv1, on=['ID', 'DataInclusão'], how='left', indicator=True)
    registros_nao_encontrados = merger_df[merger_df['_merge'] == 'left_only'].drop(columns='_merge')

    return registros_nao_encontrados

# Caminhos das pastas
pasta1 = r'C:\Users\Andre Severo\OneDrive\Power BI\Sistecoll\Acionamentos\2025\1.Jan'
pasta2 = r'C:\Users\Andre Severo\OneDrive\Power BI\Sistecoll\Discador\Discador3C\2025\1.Jan'

registros_faltantes = encontrar_registros_nao_presentes(pasta1, pasta2)


caminho_excel = r'C:\Users\Andre Severo\OneDrive\Power BI\Sistecoll\Bases\FORTBRASIL2.xlsx'

df_excel = pd.read_excel(caminho_excel, sheet_name='TRATADO')

if 'ID' not in df_excel.columns:
    raise ValueError('A coluna "ID" não foi encontrada no arquivo Excel.')

registos_correspondentes = registros_faltantes[registros_faltantes['ID'].isin(df_excel['ID'])]

df_registros_faltantes = pd.DataFrame(registos_correspondentes)




