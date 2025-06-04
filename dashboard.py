import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para estilização
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f77b4;
    }
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .insight-box {
    position: relative;
    background: linear-gradient(135deg, #f9fafc, #e6ecf3);
    padding: 1.5rem 2rem;
    border-left: 6px solid #1f77b4;
    border-radius: 12px;
    margin: 1.5rem 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 1rem;
    line-height: 1.6;
    color: #2c3e50;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .insight-box::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at center, rgba(31, 119, 180, 0.1), transparent 70%);
    transform: rotate(45deg);
    animation: pulse 6s infinite;
    }

    .insight-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    }

    @keyframes pulse {
    0% {
        transform: rotate(45deg) scale(1);
        opacity: 0.6;
    }
    50% {
        transform: rotate(45deg) scale(1.1);
        opacity: 0.8;
    }
    100% {
        transform: rotate(45deg) scale(1);
        opacity: 0.6;
    }
    }



</style>
""", unsafe_allow_html=True)

# Função para gerar dados fictícios
@st.cache_data
def generate_sales_data():
    np.random.seed(42)
    
    # Configurações dos dados
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    # Listas de dados fictícios
    produtos = [
        'Smartphone Pro', 'Laptop Gamer', 'Tablet Premium', 'Smartwatch',
        'Fones Bluetooth', 'Monitor 4K', 'Teclado Mecânico', 'Mouse Gamer',
        'Webcam HD', 'SSD 1TB', 'Carregador Wireless', 'Capa Protetora'
    ]
    
    categorias = {
        'Smartphone Pro': 'Smartphones',
        'Laptop Gamer': 'Computadores',
        'Tablet Premium': 'Tablets',
        'Smartwatch': 'Wearables',
        'Fones Bluetooth': 'Áudio',
        'Monitor 4K': 'Periféricos',
        'Teclado Mecânico': 'Periféricos',
        'Mouse Gamer': 'Periféricos',
        'Webcam HD': 'Periféricos',
        'SSD 1TB': 'Armazenamento',
        'Carregador Wireless': 'Acessórios',
        'Capa Protetora': 'Acessórios'
    }
    
    regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
    vendedores = ['Ana Silva', 'Carlos Santos', 'Maria Oliveira', 'João Pereira', 
                  'Fernanda Costa', 'Ricardo Lima', 'Patricia Souza', 'Bruno Alves']
    
    # Preços base dos produtos
    precos_base = {
        'Smartphone Pro': 2500, 'Laptop Gamer': 4500, 'Tablet Premium': 1800,
        'Smartwatch': 800, 'Fones Bluetooth': 250, 'Monitor 4K': 1200,
        'Teclado Mecânico': 300, 'Mouse Gamer': 150, 'Webcam HD': 200,
        'SSD 1TB': 400, 'Carregador Wireless': 80, 'Capa Protetora': 50
    }
    
    # Gerar dados
    dados = []
    for _ in range(5000):
        data_venda = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        produto = random.choice(produtos)
        categoria = categorias[produto]
        preco_base = precos_base[produto]
        
        # Variação de preço (desconto/promoção)
        variacao_preco = random.uniform(0.8, 1.2)
        preco_unitario = round(preco_base * variacao_preco, 2)
        
        quantidade = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 15, 7, 3])[0]
        receita = round(preco_unitario * quantidade, 2)
        
        # Custo (margem entre 30-60%)
        margem = random.uniform(0.3, 0.6)
        custo = round(receita * (1 - margem), 2)
        lucro = round(receita - custo, 2)
        
        dados.append({
            'Data': data_venda,
            'Produto': produto,
            'Categoria': categoria,
            'Quantidade': quantidade,
            'Preço_Unitário': preco_unitario,
            'Receita': receita,
            'Custo': custo,
            'Lucro': lucro,
            'Região': random.choice(regioes),
            'Vendedor': random.choice(vendedores),
            'Mês': data_venda.strftime('%Y-%m'),
            'Trimestre': f"Q{((data_venda.month-1)//3)+1} {data_venda.year}",
            'Ano': data_venda.year
        })
    
    return pd.DataFrame(dados)

# Função para calcular métricas
def calcular_metricas(df):
    total_receita = df['Receita'].sum()
    total_lucro = df['Lucro'].sum()
    total_vendas = len(df)
    ticket_medio = df['Receita'].mean()
    margem_lucro = (total_lucro / total_receita) * 100 if total_receita > 0 else 0
    
    return {
        'receita': total_receita,
        'lucro': total_lucro,
        'vendas': total_vendas,
        'ticket_medio': ticket_medio,
        'margem_lucro': margem_lucro
    }

# Função para formatar valores
def formatar_valor(valor, tipo='moeda'):
    if tipo == 'moeda':
        return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    elif tipo == 'porcentagem':
        return f"{valor:.1f}%"
    elif tipo == 'numero':
        return f"{valor:,.0f}".replace(',', '.')
    return str(valor)

# Carregar dados
df = generate_sales_data()

# Header
st.markdown('<h1 class="main-header">🎯 Dashboard de Vendas Estratégico</h1>', 
            unsafe_allow_html=True)

# Sidebar para filtros
st.sidebar.header("🔍 Filtros")

# Filtros
anos_disponiveis = sorted(df['Ano'].unique())
ano_selecionado = st.sidebar.selectbox('Ano', anos_disponiveis, index=len(anos_disponiveis)-1)

categorias_disponiveis = ['Todas'] + sorted(df['Categoria'].unique())
categoria_selecionada = st.sidebar.selectbox('Categoria', categorias_disponiveis)

regioes_disponiveis = ['Todas'] + sorted(df['Região'].unique())
regiao_selecionada = st.sidebar.selectbox('Região', regioes_disponiveis)

vendedores_disponiveis = ['Todos'] + sorted(df['Vendedor'].unique())
vendedor_selecionado = st.sidebar.selectbox('Vendedor', vendedores_disponiveis)

# Aplicar filtros
df_filtrado = df[df['Ano'] == ano_selecionado].copy()

if categoria_selecionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Categoria'] == categoria_selecionada]

if regiao_selecionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Região'] == regiao_selecionada]

if vendedor_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Vendedor'] == vendedor_selecionado]

# Calcular métricas
metricas = calcular_metricas(df_filtrado)
metricas_ano_anterior = calcular_metricas(df[df['Ano'] == ano_selecionado - 1]) if ano_selecionado > df['Ano'].min() else None

# Seção de KPIs
st.header("📈 Principais Indicadores")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    delta_receita = ((metricas['receita'] - metricas_ano_anterior['receita']) / metricas_ano_anterior['receita'] * 100) if metricas_ano_anterior else 0
    st.metric(
        "Receita Total",
        formatar_valor(metricas['receita']),
        f"{delta_receita:+.1f}%" if metricas_ano_anterior else None
    )

with col2:
    delta_lucro = ((metricas['lucro'] - metricas_ano_anterior['lucro']) / metricas_ano_anterior['lucro'] * 100) if metricas_ano_anterior else 0
    st.metric(
        "Lucro Total",
        formatar_valor(metricas['lucro']),
        f"{delta_lucro:+.1f}%" if metricas_ano_anterior else None
    )

with col3:
    delta_vendas = ((metricas['vendas'] - metricas_ano_anterior['vendas']) / metricas_ano_anterior['vendas'] * 100) if metricas_ano_anterior else 0
    st.metric(
        "Total de Vendas",
        formatar_valor(metricas['vendas'], 'numero'),
        f"{delta_vendas:+.1f}%" if metricas_ano_anterior else None
    )

with col4:
    delta_ticket = ((metricas['ticket_medio'] - metricas_ano_anterior['ticket_medio']) / metricas_ano_anterior['ticket_medio'] * 100) if metricas_ano_anterior else 0
    st.metric(
        "Ticket Médio",
        formatar_valor(metricas['ticket_medio']),
        f"{delta_ticket:+.1f}%" if metricas_ano_anterior else None
    )

with col5:
    st.metric(
        "Margem de Lucro",
        formatar_valor(metricas['margem_lucro'], 'porcentagem'),
        None
    )

# Gráficos principais
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Evolução Mensal de Vendas")
    
    vendas_mensais = df_filtrado.groupby('Mês').agg({
        'Receita': 'sum',
        'Lucro': 'sum',
        'Quantidade': 'sum'
    }).reset_index()
    
    fig_linha = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_linha.add_trace(
        go.Scatter(x=vendas_mensais['Mês'], y=vendas_mensais['Receita'],
                  name='Receita', line=dict(color='#1f77b4', width=3)),
        secondary_y=False,
    )
    
    fig_linha.add_trace(
        go.Scatter(x=vendas_mensais['Mês'], y=vendas_mensais['Lucro'],
                  name='Lucro', line=dict(color='#ff7f0e', width=3)),
        secondary_y=False,
    )
    
    fig_linha.update_layout(
        title='Tendência de Receita e Lucro',
        xaxis_title='Mês',
        height=400,
        hovermode='x unified'
    )
    
    fig_linha.update_yaxes(title_text='Valor (R$)', secondary_y=False)

    
    st.plotly_chart(fig_linha, use_container_width=True)

with col2:
    st.subheader("🥧 Participação por Categoria")
    
    vendas_categoria = df_filtrado.groupby('Categoria')['Receita'].sum().reset_index()
    
    fig_pizza = px.pie(vendas_categoria, values='Receita', names='Categoria',
                       title='Distribuição de Receita por Categoria')
    fig_pizza.update_traces(textposition='inside', textinfo='percent+label')
    fig_pizza.update_layout(height=400)
    
    st.plotly_chart(fig_pizza, use_container_width=True)

# Segunda linha de gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Produtos por Receita")
    
    top_produtos = df_filtrado.groupby('Produto')['Receita'].sum().sort_values(ascending=True).tail(10)
    
    fig_bar = px.bar(x=top_produtos.values, y=top_produtos.index,
                     orientation='h',
                     title='Produtos com Maior Receita',
                     color=top_produtos.values,
                     color_continuous_scale='Blues')
    fig_bar.update_layout(height=400, showlegend=False)
    fig_bar.update_layout(xaxis_title='Receita (R$)')
    fig_bar.update_yaxes(title_text='Produto')
    
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("🌎 Performance por Região")
    
    vendas_regiao = df_filtrado.groupby('Região').agg({
        'Receita': 'sum',
        'Lucro': 'sum',
        'Quantidade': 'sum'
    }).reset_index()
    
    fig_regiao = px.bar(vendas_regiao, x='Região', y=['Receita', 'Lucro'],
                        title='Receita e Lucro por Região',
                        barmode='group')
    fig_regiao.update_layout(height=400)
    
    st.plotly_chart(fig_regiao, use_container_width=True)

# Seção de Análise de Vendedores
st.subheader("👥 Performance dos Vendedores")

vendedores_performance = df_filtrado.groupby('Vendedor').agg({
    'Receita': 'sum',
    'Lucro': 'sum',
    'Quantidade': 'sum'
}).reset_index()

vendedores_performance['Ticket_Médio'] = vendedores_performance['Receita'] / vendedores_performance['Quantidade']
vendedores_performance['Margem_Lucro'] = (vendedores_performance['Lucro'] / vendedores_performance['Receita']) * 100

# Formatar valores para exibição
vendedores_display = vendedores_performance.copy()
vendedores_display['Receita'] = vendedores_display['Receita'].apply(lambda x: formatar_valor(x))
vendedores_display['Lucro'] = vendedores_display['Lucro'].apply(lambda x: formatar_valor(x))
vendedores_display['Ticket_Médio'] = vendedores_display['Ticket_Médio'].apply(lambda x: formatar_valor(x))
vendedores_display['Margem_Lucro'] = vendedores_display['Margem_Lucro'].apply(lambda x: formatar_valor(x, 'porcentagem'))

st.dataframe(vendedores_display, use_container_width=True)

# Insights Estratégicos
st.header("🎯 Insights Estratégicos")

# Calcular insights
produto_mais_vendido = df_filtrado.groupby('Produto')['Quantidade'].sum().idxmax()
categoria_mais_lucrativa = df_filtrado.groupby('Categoria')['Lucro'].sum().idxmax()
regiao_melhor_performance = df_filtrado.groupby('Região')['Receita'].sum().idxmax()
vendedor_top = df_filtrado.groupby('Vendedor')['Receita'].sum().idxmax()

melhor_mes = df_filtrado.groupby('Mês')['Receita'].sum().idxmax()
receita_melhor_mes = df_filtrado.groupby('Mês')['Receita'].sum().max()

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="insight-box">
        <h4>🏆 Produto Campeão</h4>
        <p><strong>{produto_mais_vendido}</strong> é o produto mais vendido em quantidade, 
        demonstrando alta aceitação no mercado.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-box">
        <h4>💰 Categoria Mais Lucrativa</h4>
        <p><strong>{categoria_mais_lucrativa}</strong> apresenta a maior margem de lucro, 
        sendo estratégica para maximizar rentabilidade.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="insight-box">
        <h4>🌟 Região Destaque</h4>
        <p><strong>{regiao_melhor_performance}</strong> lidera em receita total, 
        indicando potencial para expansão de investimentos.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-box">
        <h4>🚀 Vendedor Top</h4>
        <p><strong>{vendedor_top}</strong> é o vendedor com melhor performance, 
        podendo servir como mentor para outros vendedores.</p>
    </div>
    """, unsafe_allow_html=True)

# Análise Temporal
st.subheader("📅 Análise Temporal Detalhada")

# Gráfico de heatmap por mês e categoria
vendas_heatmap = df_filtrado.groupby(['Mês', 'Categoria'])['Receita'].sum().reset_index()
vendas_pivot = vendas_heatmap.pivot(index='Categoria', columns='Mês', values='Receita').fillna(0)

fig_heatmap = px.imshow(vendas_pivot, 
                        title='Heatmap de Vendas: Categoria vs Mês',
                        aspect='auto',
                        color_continuous_scale='Blues')
fig_heatmap.update_layout(height=400)

st.plotly_chart(fig_heatmap, use_container_width=True)

# Footer com informações adicionais
st.markdown("---")
st.markdown(f"""
**📊 Resumo Executivo do Dashboard**
- **Período analisado:** {ano_selecionado}
- **Total de registros:** {len(df_filtrado):,} vendas
- **Última atualização:** {datetime.now().strftime('%d/%m/%Y às %H:%M')}
- **Melhor mês:** {melhor_mes} com {formatar_valor(receita_melhor_mes)} em receita
""")

st.markdown("""
---
*Dashboard desenvolvido com Streamlit | Dados fictícios para demonstração*
""")