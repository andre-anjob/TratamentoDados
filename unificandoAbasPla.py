import pandas as pd


def unify_sheets(file_path):

    all_sheets = pd.read_excel(file_path, sheet_name=None)
    

    unified_df = pd.concat(all_sheets.values(), ignore_index=True)
    return unified_df


def repeat_rows_by_count(df):

    df_repeated = df.loc[df.index.repeat(df['called_count'])].reset_index(drop=True)
    return df_repeated


def relate_columns(unified_df, depara_file):

    depara_df = pd.read_excel(depara_file)
    

    related_df = pd.merge(unified_df, depara_df[['DEPARA', 'ACIONAMENTO']], 
                          left_on='status', right_on='DEPARA', how='left')
    

    related_df = related_df.rename(columns={'ACIONAMENTO': 'Acionamento'})
    return related_df


def filter_out_acordo(df):

    filtered_df = df[~df['Acionamento'].str.contains('acordo', case=False, na=False)]
    return filtered_df


def select_columns(filtered_df):

    final_df = filtered_df[['user', 'modify_date', 'Acionamento', 'last_name', 'phone_number', 'first_name']]
    

    final_df['Duração'] = '01:00:00' 
    final_df['Contratante'] = 'FORTBRASIL'
    final_df['Cpf'] = final_df['phone_number']
    

    final_df = final_df.rename(columns={'phone_number': 'Fone/Destino',
                                        'user': 'Cobrador',
                                        'modify_date': 'DataInclusão',
                                        'first_name': 'Devedor',
                                        'last_name': 'ID'})
    

    final_df = final_df[['Cobrador', 'DataInclusão', 'Duração', 'Acionamento', 
                         'Contratante', 'ID', 'Cpf', 'Devedor', 'Fone/Destino']]
    
    return final_df


def process_files(unified_file, depara_file):


    unified_df = unify_sheets(unified_file)
    

    repeated_df = repeat_rows_by_count(unified_df)
    

    related_df = relate_columns(repeated_df, depara_file)
    

    filtered_df = filter_out_acordo(related_df)
    
    final_df = select_columns(filtered_df)
    
    return final_df


unified_file = r'C:\Users\Andre Severo\OneDrive\Power BI\Sistecoll\Discador\Discador Enviado Romario\Mailing_fortbrasil_25112024.xlsx'
depara_file = r'C:\Users\Andre Severo\OneDrive\Power BI\Sistecoll\DExPARA\DExPARA_Discador.xlsx'


result_df = process_files(unified_file, depara_file)


result_df.to_excel(r'C:\Users\Andre Severo\OneDrive\Power BI\Sistecoll\Discador\tratativa base\nome_do_arquivo_atualizado_25112024.xlsx', index=False)
