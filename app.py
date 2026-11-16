import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configuração da Página
st.set_page_config(
    page_title="ED Industrial Intelligence | 2027+ Interactive",
    page_icon="🚀",
    layout="wide"
)

# Design System Premium Dark Mode
st.markdown("""
    <style>
    .main { background-color: #0B0F19; color: #F3F4F6; }
    [data-testid="stSidebar"] { background-color: #111827; border-right: 1px solid #1F2937; }
    .stMetric { background-color: #111827; padding: 20px; border-radius: 12px; border: 1px solid #1F2937; }
    .stMetric label { color: #9CA3AF !important; font-size: 0.8rem; text-transform: uppercase; }
    .stMetric [data-testid="stMetricValue"] { color: #38BDF8 !important; font-size: 1.8rem; font-weight: 700; }
    h1, h2, h3 { color: #FFFFFF; font-family: 'Inter', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# BASES DE DADOS EXPANDIDAS PARA 2027+
# ----------------------------------------------------
if 'estoque' not in st.session_state:
    st.session_state['estoque'] = pd.DataFrame([
        {"SKU": "SKU-2027-01", "Produto": "Chapa de Aço Especial 12mm", "Categoria": "Matéria-Prima", "Estoque_Min": 60, "Custo_Unit": 145.00, "Qtd_Atual": 180},
        {"SKU": "SKU-2027-02", "Produto": "Composto de Borracha High-Tech", "Categoria": "Componentes", "Estoque_Min": 120, "Custo_Unit": 52.00, "Qtd_Atual": 95},
        {"SKU": "SKU-2027-03", "Produto": "Kit Fixação Estrutural M14", "Categoria": "Fixadores", "Estoque_Min": 400, "Custo_Unit": 2.50, "Qtd_Atual": 850},
        {"SKU": "SKU-2027-04", "Produto": "Fluido Hidráulico Sintético 68", "Categoria": "Lubrificantes", "Estoque_Min": 70, "Custo_Unit": 48.00, "Qtd_Atual": 55}
    ])

if 'entregas_geo' not in st.session_state:
    # Dados geográficos simulados para o mapa interativo (Cachoeirinha, Porto Alegre, Gravataí, Caxias do Sul)
    st.session_state['entregas_geo'] = pd.DataFrame([
        {"Cliente": "Montadora Delta", "Cidade": "Cachoeirinha", "Lat": -29.9542, "Lon": -50.9936, "Status": "No Prazo", "Frete": 680.00, "Volume": 45},
        {"Cliente": "Industrial Sul", "Cidade": "Gravataí", "Lat": -29.9461, "Lon": -50.9939, "Status": "Atrasado", "Frete": 950.00, "Volume": 80},
        {"Cliente": "AutoPças Serra", "Cidade": "Caxias do Sul", "Lat": -29.1678, "Lon": -51.1794, "Status": "No Prazo", "Frete": 1420.00, "Volume": 120},
        {"Cliente": "Global Rubber", "Cidade": "Porto Alegre", "Lat": -30.0346, "Lon": -51.2177, "Status": "Em Trânsito", "Frete": 520.00, "Volume": 30}
    ])

# Menu Lateral
st.sidebar.markdown("## ⚡ ED INDUSTRIAL 2027")
st.sidebar.markdown("<p style='color: #9CA3AF; font-size: 0.75rem;'>Front-End Interativo & Analytics</p>", unsafe_allow_html=True)
st.sidebar.divider()

menu = st.sidebar.radio("Navegação Imersiva", [
    "🚀 Dashboard Executivo & Hover Interativo", 
    "🗺️ Mapa Geográfico de Entregas & Rotas", 
    "📈 Projeções Preditivas (2027-2030)", 
    "🔄 Gestão Operacional de Estoque"
])

df_est = st.session_state['estoque']
df_geo = st.session_state['entregas_geo']

# ----------------------------------------------------
# TELA 1: DASHBOARD EXECUTIVO COM HOVER INTERATIVO
# ----------------------------------------------------
if menu == "🚀 Dashboard Executivo & Hover Interativo":
    st.title("🚀 Painel Executivo Interativo (2027+)")
    st.markdown("Passe o mouse sobre os gráficos para inspecionar métricas detalhadas em tempo real.")

    # KPIs Principais
    df_est['Valor_Total'] = df_est['Qtd_Atual'] * df_est['Custo_Unit']
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Patrimônio em Estoque", f"R$ {df_est['Valor_Total'].sum():,.2f}")
    with c2:
        rupturas = len(df_est[df_est['Qtd_Atual'] <= df_est['Estoque_Min']])
        st.metric("Rupturas Críticas", rupturas, delta="Atenção" if rupturas > 0 else "Estável", delta_color="inverse")
    with c3:
        st.metric("Total SKUs Ativos", len(df_est))
    with c4:
        st.metric("Índice OTD Global", "92.4%", delta="+1.8% vs 2026")

    st.divider()

    # Gráfico de Barras Interativo (Hover detalhado)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 📊 Valor Imobilizado por SKU (Hover Interativo)")
        fig_bar = px.bar(
            df_est, 
            x='SKU', 
            y='Valor_Total', 
            text='Valor_Total',
            color='Categoria',
            hover_data=['Produto', 'Qtd_Atual', 'Custo_Unit'],
            template='plotly_dark'
        )
        fig_bar.update_traces(texttemplate='R$ %{text:,.2f}', textposition='outside')
        fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_b:
        st.markdown("### 🍩 Composição de Estoque por Categoria")
        fig_pie = px.pie(
            df_est, 
            names='Categoria', 
            values='Valor_Total', 
            hole=0.4,
            template='plotly_dark'
        )
        fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie, use_container_width=True)

# ----------------------------------------------------
# TELA 2: MAPA GEOGRÁFICO DE ENTREGAS
# ----------------------------------------------------
elif menu == "🗺️ Mapa Geográfico de Entregas & Rotas":
    st.title("🗺️ Mapa Geográfico de Entregas & Logística")
    st.markdown("Visualização interativa das entregas destino, status de pontualidade e custos de frete.")

    # Mapa Interativo com Plotly Scattermapbox / Scattergeo
    fig_map = px.scatter_geo(
        df_geo,
        lat='Lat',
        lon='Lon',
        color='Status',
        size='Volume',
        hover_name='Cliente',
        hover_data=['Cidade', 'Frete', 'Status'],
        projection='natural earth',
        template='plotly_dark',
        title="<b>Rede de Distribuição Logística (Passar o mouse para detalhes)</b>"
    )
    
    # Ajustando o zoom para a região sul do Brasil como base
    fig_map.update_geos(
        center=dict(lat=-29.8, lon=-51.1),
        zoom=6,
        showland=True,
        landcolor="#1F2937",
        subunitcolor="#374151"
    )
    fig_map.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=50, b=0))
    
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("### 📋 Tabela Analítica de Fretes e Destinos")
    st.dataframe(df_geo, use_container_width=True, hide_index=True)

# ----------------------------------------------------
# TELA 3: PROJEÇÕES PREDITIVAS (2027-2030)
# ----------------------------------------------------
elif menu == "📈 Projeções Preditivas (2027-2030)":
    st.title("📈 Projeções Preditivas de Consumo & Demanda")
    st.markdown("Simulação algorítmica de tendência de consumo de matérias-primas para os próximos anos.")

    # Gerando dados de projeção futurista
    anos = ['2026 (Real)', '2027 (Proj)', '2028 (Proj)', '2029 (Proj)', '2030 (Proj)']
    consumo_aco = [1200, 1450, 1700, 1950, 2300]
    consumo_borracha = [800, 920, 1050, 1200, 1400]

    df_proj = pd.DataFrame({
        'Ano': anos,
        'Chapa de Aço (Ton)': consumo_aco,
        'Composto de Borracha (Ton)': consumo_borracha
    })

    fig_line = px.line(
        df_proj, 
        x='Ano', 
        y=['Chapa de Aço (Ton)', 'Composto de Borracha (Ton)'],
        markers=True,
        template='plotly_dark',
        title="<b>Tendência de Crescimento e Demanda Industrial (2026 - 2030)</b>"
    )
    fig_line.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title="Horizonte Temporal", yaxis_title="Volume Projetado")
    st.plotly_chart(fig_line, use_container_width=True)

    st.info("💡 **Análise de IA 2027:** O modelo preditivo indica alta de 20.8% na demanda por chapas de aço para o ciclo de 2027, exigindo renegociação antecipada com fornecedores.")

# ----------------------------------------------------
# TELA 4: GESTÃO OPERACIONAL DE ESTOQUE
# ----------------------------------------------------
elif menu == "🔄 Gestão Operacional de Estoque":
    st.title("🔄 Controle Operacional de Saldos")
    st.markdown("Gerenciamento rápido de entradas e saídas nas mini-fábricas.")

    with st.form("form_op"):
        c1, c2, c3 = st.columns(3)
        with c1:
            sku_sel = st.selectbox("SKU", df_est['SKU'].tolist())
            op = st.selectbox("Operação", ["Entrada", "Saída"])
        with c2:
            qtd = st.number_input("Quantidade", min_value=1, value=50)
            nf = st.text_input("Nota Fiscal", "NF-2027-")
        with c3:
            parceiro = st.text_input("Parceiro", "Cliente / Fornecedor")
            data_op = st.date_input("Data", datetime.today())

        btn = st.form_submit_button("⚡ Processar Operação")
        if btn:
            idx = df_est[df_est['SKU'] == sku_sel].index[0]
            if op == "Entrada":
                df_est.loc[idx, 'Qtd_Atual'] += qtd
            else:
                df_est.loc[idx, 'Qtd_Atual'] -= qtd
            st.success("Operação executada e sincronizada com sucesso!")

    st.markdown("### 📦 Inventário Atualizado em Tempo Real")
    st.dataframe(df_est[['SKU', 'Produto', 'Categoria', 'Estoque_Min', 'Qtd_Atual', 'Custo_Unit', 'Valor_Total']], use_container_width=True, hide_index=True)
