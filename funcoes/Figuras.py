import plotly.graph_objects as go
import pandas as pd
import numpy as np


def calculate_avg_move_with_date(df, value_column, date_column=None, 
                                method='absolute', periods=1, 
                                time_unit='days', sort_by_date=True):
    """
    Calculate average movement in a pandas DataFrame with date handling
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame
    value_column : str
        Column name to calculate movement for
    date_column : str, optional
        Date column name. If None, assumes index is datetime
    method : str
        'absolute' - average of absolute differences
        'net' - average of net differences
        'percent' - average percentage change
        'percent_abs' - average absolute percentage change
        'per_day' - average movement per day (requires date column)
    periods : int
        Number of periods for difference calculation
    time_unit : str
        Time unit for per-day calculations ('days', 'hours', 'minutes')
    sort_by_date : bool
        Whether to sort by date before calculating
    
    Returns:
    --------
    float : Average movement value
    """
    
    # Create working copy
    df_work = df.copy()
    
    # Handle date column
    if date_column:
        df_work[date_column] = pd.to_datetime(df_work[date_column])
        if sort_by_date:
            df_work = df_work.sort_values(date_column)
    elif sort_by_date and isinstance(df_work.index, pd.DatetimeIndex):
        df_work = df_work.sort_index()
    
    # Calculate basic movements
    if method == 'absolute':
        return df_work[value_column].diff(periods).abs().mean()
    
    elif method == 'net':
        return df_work[value_column].diff(periods).mean()
    
    elif method == 'percent':
        return df_work[value_column].pct_change(periods).mean()
    
    elif method == 'percent_abs':
        return df_work[value_column].pct_change(periods).abs().mean()
    
    elif method == 'per_day':
        if date_column is None and not isinstance(df_work.index, pd.DatetimeIndex):
            raise ValueError("Date column required for 'per_day' method")
        
        # Calculate value differences
        value_diff = df_work[value_column].diff(periods).abs()
        
        # Calculate time differences
        if date_column:
            time_diff = df_work[date_column].diff(periods)
        else:
            time_diff = pd.Series(df_work.index).diff(periods)
        
        # Convert to specified time unit
        if time_unit == 'days':
            time_diff_numeric = time_diff.dt.total_seconds() / 86400
        elif time_unit == 'hours':
            time_diff_numeric = time_diff.dt.total_seconds() / 3600
        elif time_unit == 'minutes':
            time_diff_numeric = time_diff.dt.total_seconds() / 60
        else:
            raise ValueError("time_unit must be 'days', 'hours', or 'minutes'")
        
        # Calculate movement per time unit
        movement_per_unit = value_diff / time_diff_numeric
        return movement_per_unit.mean()
    
    else:
        raise ValueError("Method must be 'absolute', 'net', 'percent', 'percent_abs', or 'per_day'")


def create_horizontal_bar_chart_go(data, x_col, y_col, title="Horizontal Bar Chart", 
                                   show_percentages=True, height=400, 
                                   text_position='inside', bar_color=None):
    """
    Create a horizontal bar chart using Plotly Graph Objects
    
    Parameters:
    -----------
    data : pandas.DataFrame or dict
        Data containing the values for the chart
    x_col : str
        Column name for x-axis values (bar lengths)
    y_col : str  
        Column name for y-axis labels (categories)
    title : str
        Chart title
    show_percentages : bool
        Whether to show percentages in labels
    height : int
        Chart height in pixels
    text_position : str
        Position of text labels ('inside', 'outside', 'auto')
    bar_color : str or list
        Color(s) for bars
    
    Returns:
    --------
    plotly.graph_objects.Figure
    """
    
    # Convert to DataFrame if dict
    if isinstance(data, dict):
        df = pd.DataFrame(data)
    else:
        df = data.copy()
    
    # Calculate proportions if showing percentages
    if show_percentages:
        total = df[x_col].sum()
        proportions = df[x_col] / total
    
    # Create the bar trace
    bar_trace = go.Bar(
        x=df[x_col],
        y=df[y_col],
        orientation='h',
        text=df[x_col],
        textposition=text_position,
        marker_color=bar_color
    )
    
    # Update text template based on percentage option
    if show_percentages:
        bar_trace.texttemplate = '%{text} (%{customdata:.1%})'
        bar_trace.customdata = proportions
    else:
        bar_trace.texttemplate = '%{text}'
    
    # Create figure
    fig = go.Figure(data=[bar_trace])
    
    # Update layout
    fig.update_layout(
        title=title,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=False, 
            zeroline=False,
            title=""
        ),
        yaxis=dict(
            showgrid=False, 
            zeroline=False,
            title=""
        ),
        height=height
    )
    
    return fig

def create_time_series_chart_go(data, date_col, value_col, ma_col=None, 
                                title="Time Series Chart", height=500,
                                daily_color='blue', ma_color='red',
                                show_markers=True, ma_width=3,
                                show_slider=False, extra_months=1):
    """
    Create a time series chart with moving average using Plotly Graph Objects

    Parameters:
    -----------
    data : pandas.DataFrame or dict
        Data containing the time series values
    date_col : str
        Column name for date/time axis
    value_col : str
        Column name for main values (daily/monthly counts)
    ma_col : str, optional
        Column name for moving average values
    title : str
        Chart title
    height : int
        Chart height in pixels
    daily_color : str
        Color for daily/monthly values line
    ma_color : str
        Color for moving average line
    show_markers : bool
        Whether to show markers on daily values
    ma_width : int
        Width of moving average line
    show_slider : bool
        Whether to show a range slider and range selector on the x-axis
    extra_months : int
        Number of extra months to add at the end of x-axis (default: 1)

    Returns:
    --------
    plotly.graph_objects.Figure
    """

    # Convert to DataFrame if dict
    if isinstance(data, dict):
        df = pd.DataFrame(data)
    else:
        df = data.copy()

    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col])

    # Create figure
    fig = go.Figure()

    # Add daily values trace
    mode = 'lines+markers' if show_markers else 'lines'
    daily_trace = go.Scatter(
        x=df[date_col],
        y=df[value_col],
        mode=mode,
        name='Contagem',
        line=dict(color=daily_color, width=1),
        opacity=0.7,
        hovertemplate='<b>Data:</b> %{x|%d/%m/%Y}<br><b>Contagem:</b> %{y}<extra></extra>'
    )

    if show_markers:
        daily_trace.marker = dict(size=4, color=daily_color)

    fig.add_trace(daily_trace)

    # Add moving average trace if column provided
    if ma_col and ma_col in df.columns:
        ma_trace = go.Scatter(
            x=df[date_col],
            y=df[ma_col],
            mode='lines',
            name='Média Móvel',
            line=dict(color=ma_color, width=ma_width),
            hovertemplate='<b>Data:</b> %{x|%d/%m/%Y}<br><b>Média Móvel:</b> %{y:.2f}<extra></extra>'
        )
        fig.add_trace(ma_trace)

    # Define min and max date for x-axis
    min_date = df[date_col].min()
    max_date = df[date_col].max() + pd.DateOffset(months=extra_months)

    # Define layout for x-axis (slider and range selector)
    xaxis_config = dict(
        title="",
        showgrid=False,
        gridcolor='lightgray',
        gridwidth=0.5,
        range=[min_date, max_date]
    )

    if show_slider:
        xaxis_config["rangeslider"] = dict(visible=True)
        xaxis_config["rangeselector"] = dict(
            buttons=list([
                dict(count=1, label="1 ano", step="year", stepmode="backward"),
                dict(count=10, label="10 anos", step="year", stepmode="backward"),
                dict(step="all", label="Todos")
            ]),
            bgcolor="rgba(240,240,240,0.6)",
            bordercolor="gray",
            borderwidth=1,
            activecolor="#666"
        )

    # Update layout
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            font=dict(size=16)
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=xaxis_config,
        yaxis=dict(
            title="",
            showgrid=False,
            gridcolor='lightgray',
            gridwidth=0.5
        ),
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="gray",
            borderwidth=1
        ),
        height=height
    )

    return fig


def create_line_chart_go(data, x_col, y_col, 
                         title="Line Chart", height=500,
                         line_color='blue', line_width=2):
    """
    Cria um gráfico de linha simples usando Plotly Graph Objects.
    
    Parâmetros:
    -----------
    data : pandas.DataFrame ou dict
        Dados contendo as séries para plotar.
    x_col : str
        Nome da coluna para o eixo x.
    y_col : str
        Nome da coluna para o eixo y.
    title : str
        Título do gráfico.
    height : int
        Altura do gráfico em pixels.
    line_color : str
        Cor da linha.
    line_width : int
        Espessura da linha.
    
    Retorna:
    --------
    plotly.graph_objects.Figure
    """
    
    # Converter dict para DataFrame se necessário
    if isinstance(data, dict):
        df = pd.DataFrame(data)
    else:
        df = data.copy()
   
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='lines',
        line=dict(color=line_color, width=line_width),
        name='y_col',
        hovertemplate=f'<b>{x_col}:</b> %{{x}}<br><b>{y_col}:</b> %{{y}}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=16)),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title='',
            showgrid=False,
            gridcolor='lightgray',
            gridwidth=0.5
        ),
        yaxis=dict(
            title='',
            showgrid=False,
            gridcolor='lightgray',
            gridwidth=0.5
        ),
        hovermode='x unified',
        height=height,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="gray",
            borderwidth=1
        )
    )
    
    return fig



