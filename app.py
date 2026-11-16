import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(
    page_title="Gestão Industrial & Logística Pro",
    page_icon="🏭",
    layout="wide"
)

# Estilização visual limpa e profissional
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stMetric { background-color: #FFFFFF; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# INICIALIZAÇÃO DE DADOS NA SESSÃO
# ----------------------------------------------------
if 'estoque' not in st.session_state:
    st.session_state['estoque'] = pd.DataFrame([
        {"SKU": "SKU-001", "Produto": "Chapa de Aço 10mm", "Categoria": "Matéria-Prima", "Estoque_Min": 50, "Custo_Unit": 120.00, "Qtd_Atual": 140},
        {"SKU": "SKU-002", "Produto": "Borracha Industrial V", "Categoria": "Componentes", "Estoque_Min": 100, "Custo_Unit": 45.50, "Qtd_Atual": 75},
        {"SKU": "SKU-003", "Produto": "Parafuso Sextavado M12", "Categoria": "Fixadores", "Estoque_Min": 500, "Custo_Unit": 1.20, "Qtd_Atual": 620},
        {"SKU": "SKU-004", "Produto": "Óleo Hidráulico 68", "Categoria": "Lubrificantes", "Estoque_Min": 80, "Custo_Unit": 35.00, "Qtd_Atual": 40}
    ])

if 'movimentos' not in st.session_state:
    st.session_state['movimentos'] = pd.DataFrame([
        {"Data": "2026-11-01", "SKU": "SKU-001", "Tipo": "Entrada", "Quantidade": 100, "Documento": "NF-4412", "Parceiro": "Fornecedor A"},
        {"Data": "2026-11-05", "SKU": "SKU-002", "Tipo": "Saída", "Quantidade": 50, "Documento": "NF-9981", "Parceiro": "Cliente X"},
        {"Data": "2026-11-10", "SKU": "SKU-004", "Tipo": "Saída", "Quantidade": 40, "Documento": "NF-9985", "Parceiro": "Cliente Y"}
    ])

if 'entregas' not in st.session_state:
    st.session_state['entregas'] = pd.DataFrame([
        {"ID_Entrega": "ENT-101", "Documento": "NF-9981", "Cliente": "Cliente X", "Data_Saida": "2026-11-05", "Data_Prevista": "2026-11-10", "Data_Real": "2026-11-09", "Status": "No Prazo", "Transportadora": "TransLogística", "Frete": 450.00},
        {"ID_Entrega": "ENT-102", "Documento": "NF-9985", "Cliente": "Cliente Y", "Data_Saida": "2026-11-10", "Data_Prevista": "2026-11-12", "Data_Real": "2026-11-15", "Status": "Atrasado", "Transportadora": "FastCargo", "Frete": 620.00}
    ])

# Menu Lateral Comercial
st.sidebar.title("🏭 ED Indústria & Logística")
menu = st.sidebar.selectbox("Módulos do Sistema", [
    "📊 Visão Executiva & KPIs", 
    "🔄 Entradas e Saídas", 
    "🚚 Monitor de Entregas (OTD)", 
    "📦 Cadastro & Curva ABC"
])

df_est = st.session_state['estoque']
df_mov = st.session_state['movimentos']
df_ent = st.session_state['entregas']

# ----------------------------------------------------
# 1. VISÃO EXECUTIVA & KPIS
# ----------------------------------------------------
if menu == "📊 Visão Executiva & KPIs":
    st.title("📊 Painel Executivo - Supply Chain")
    st.markdown("Indicadores consolidados de inventário, rupturas e nível de serviço logístico.")
    
    # Cálculos Avançados
    df_est['Valor_Total_Item'] = df_est['Qtd_Atual'] * df_est['Custo_Unit']
    valor_total_estoque = df_est['Valor_Total_Item'].sum()
    rupturas = len(df_est[df_est['Qtd_Atual'] <= df_est['Estoque_Min']])
    total_skus = len(df_est)
    
    total_ent = len(df_ent)
    no_prazo = len(df_ent[df_ent['Status'] == 'No Prazo'])
    otd_perc = (no_prazo / total_ent * 100) if total_ent > 0 else 0
    custo_frete_total = df_ent['Frete'].sum()

    # Cards de Métricas
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Valor em Estoque", f"R$ {valor_total_estoque:,.2f}")
    with col2:
        st.metric("SKUs em Ruptura", f"{rupturas}", delta="-Alerta" if rupturas > 0 else "Normal", delta_color="inverse")
    with col3:
        st.metric("Total de SKUs", total_skus)
    with col4:
        st.metric("OTD (No Prazo)", f"{otd_perc:.1f}%")
    with col5:
        st.metric("Custo Frete", f"R$ {custo_frete_total:,.2f}")

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("⚠️ Alertas Críticos de Ruptura")
        df_alerta = df_est[df_est['Qtd_Atual'] <= df_est['Estoque_Min']]
        if not df_alerta.empty:
            st.dataframe(df_alerta[['SKU', 'Produto', 'Categoria', 'Estoque_Min', 'Qtd_Atual']], use_container_width=True)
        else:
            st.success("Nenhum item abaixo do estoque mínimo!")

    with c2:
        st.subheader("💰 Top Itens por Valor Imobilizado")
        df_top = df_est.sort_values(by='Valor_Total_Item', ascending=False).head(5)
        st.dataframe(df_top[['SKU', 'Produto', 'Valor_Total_Item']], use_container_width=True)

# ----------------------------------------------------
# 2. ENTRADAS E SAÍDAS (MOVIMENTAÇÕES)
# ----------------------------------------------------
elif menu == "🔄 Entradas e Saídas":
    st.title("🔄 Controle de Movimentações de Estoque")
    
    with st.form("form_mov", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            sku_sel = st.selectbox("Produto (SKU)", df_est['SKU'].tolist())
            tipo = st.selectbox("Tipo de Movimentação", ["Entrada", "Saída"])
        with col2:
            qtd = st.number_input("Quantidade", min_value=1, value=10)
            doc = st.text_input("Número do Documento / NF", "NF-")
        with col3:
            parceiro = st.text_input("Fornecedor / Cliente", "Nome do Parceiro")
            data_mov = st.date_input("Data", datetime.today())
            
        submitted = st.form_submit_button("Confirmar Movimentação")
        if submitted:
            idx = df_est[df_est['SKU'] == sku_sel].index[0]
            if tipo == "Entrada":
                df_est.loc[idx, 'Qtd_Atual'] += qtd
            else:
                df_est.loc[idx, 'Qtd_Atual'] -= qtd
                
            nova_mov = pd.DataFrame([{"Data": str(data_mov), "SKU": sku_sel, "Tipo": tipo, "Quantidade": qtd, "Documento": doc, "Parceiro": parceiro}])
            st.session_state['movimentos'] = pd.concat([df_mov, nova_mov], ignore_index=True)
            st.success("Movimentação efetuada com sucesso e estoque atualizado!")

    st.subheader("Histórico de Movimentações")
    st.dataframe(st.session_state['movimentos'], use_container_width=True)
    
    # Botão de Exportação
    csv = st.session_state['movimentos'].to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar Histórico (CSV)", csv, "movimentos_estoque.csv", "text/csv")

# ----------------------------------------------------
# 3. MONITOR DE ENTREGAS E LOGÍSTICA
# ----------------------------------------------------
elif menu == "🚚 Monitor de Entregas (OTD)":
    st.title("🚚 Gestão Integrada de Entregas & Logística")
    
    with st.expander("➕ Cadastrar Nova Entrega / Expedição"):
        with st.form("form_entrega", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                id_ent = st.text_input("ID Entrega", "ENT-103")
                doc_ref = st.text_input("Nota Fiscal", "NF-")
                cliente = st.text_input("Cliente", "Nome")
            with c2:
                d_saida = st.date_input("Data de Saída", datetime.today())
                d_prev = st.date_input("Data Prevista Entrega", datetime.today())
            with c3:
                transportadora = st.text_input("Transportadora", "Nome")
                status_ent = st.selectbox("Status", ["No Prazo", "Atrasado", "Em Trânsito"])
                custo_frete = st.number_input("Custo do Frete (R$)", min_value=0.0, value=150.0)
                
            btn_ent = st.form_submit_button("Salvar Entrega")
            if btn_ent:
                nova_ent = pd.DataFrame([{
                    "ID_Entrega": id_ent, "Documento": doc_ref, "Cliente": cliente, 
                    "Data_Saida": str(d_saida), "Data_Prevista": str(d_prev), 
                    "Data_Real": str(d_prev) if status_ent == "No Prazo" else "Pendente",
                    "Status": status_ent, "Transportadora": transportadora, "Frete": custo_frete
                }])
                st.session_state['entregas'] = pd.concat([df_ent, nova_ent], ignore_index=True)
                st.success("Entrega cadastrada e interligada com sucesso!")

    st.subheader("Painel Geral de Entregas")
    st.dataframe(st.session_state['entregas'], use_container_width=True)

# ----------------------------------------------------
# 4. CADASTRO & CURVA ABC
# ----------------------------------------------------
elif menu == "📦 Cadastro & Curva ABC":
    st.title("📦 Cadastro de SK
