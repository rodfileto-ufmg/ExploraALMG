import pandas as pd
def formatar_numero_brl(numero, casas_decimais=2):
    """
    Formata um número com separador de milhar como ponto e decimal como vírgula.
    
    Args:
        numero (float ou int): O número a ser formatado.
        casas_decimais (int): Quantidade de casas decimais (padrão 2).
        
    Returns:
        str: Número formatado como string.
    """
    formato = f"{{:,.{casas_decimais}f}}"
    numero_formatado = formato.format(numero)
    # Troca vírgula por temporário, ponto por vírgula e temporário por ponto
    numero_formatado = numero_formatado.replace(',', 'X').replace('.', ',').replace('X', '.')
    return numero_formatado

def preprocessar_proposicao_media_movel(df, date_col='DataPublicacao', window=5):
    df_work = df.copy()
    df_work[date_col] = pd.to_datetime(df_work[date_col], format='%d/%m/%Y')
    daily_counts = df_work.groupby(df_work[date_col].dt.date).size().reset_index()
    daily_counts.columns = ['date', 'total_propositions']
    daily_counts['date'] = pd.to_datetime(daily_counts['date'])
    daily_counts = daily_counts.sort_values('date')
    daily_counts['moving_avg_5d'] = daily_counts['total_propositions'].rolling(window=window, min_periods=1).mean()
    return daily_counts