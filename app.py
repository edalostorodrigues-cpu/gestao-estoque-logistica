import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(
    page_title="Gestão de Estoque & Logística Pro",
    page_icon="📦",
    layout="wide"
)

# Inicialização de Estados (Cache local na sessão)
if 'estoque' not in st.session_state:
    st.session_state['estoque'] = pd.DataFrame([
        {"SKU": "SKU-001", "Produto": "Chapa de Aço 10mm", "Categoria": "Matéria-Prima", "Estoque_Min": 50, "Custo_Unit": 120.00, "Qtd_Atual": 140},
        {"SKU": "SKU-002", "Produto": "Borracha Industrial V", "Categoria": "Componentes", "Estoque_Min": 100, "Custo_Unit": 45.50, "Qtd_Atual": 80},
        {"SKU": "SKU-003", "Produto": "Parafuso Sextavado M12", "Categoria": "Fixadores", "Estoque_Min": 500, "Custo_Unit": 1.20, "Qtd_Atual": 620}
    ])

if 'movimentos' not in st.session_state:
    st.session_state['movimentos'] = pd.DataFrame([
        {"Data": "2026-11-01", "SKU": "SKU-001", "Tipo": "Entrada", "Quantidade": 100, "Documento": "NF-4412", "Parceiro": "Fornecedor A"},
        {"Data": "2026-11-05", "SKU": "SKU-002", "Tipo": "Saída", "Quantidade": 50, "Documento": "NF-9981", "Parceiro": "Cliente X"}
    ])

if 'entregas' not in st.session_state:
    st.session_state['entregas'] = pd.DataFrame([
        {"ID_Entrega": "ENT-101", "Documento": "NF-9981", "Cliente": "Cliente X", "Data_Saida": "2026-11-05", "Data_Prevista": "2026-11-10", "Data_Real": "2026-11-09", "Status": "No Prazo", "Transportadora": "TransLogística"},
        {"ID_Entrega": "ENT-102", "Documento": "NF-9982", "Cliente": "Cliente Y", "Data_Saida": "2026-11-10", "Data_Prevista": "2026-11-12", "Data_Real": "2026-11-15", "Status": "Atrasado", "Transportadora": "FastCargo"}
    ])

# Menu Lateral
st.sidebar.title("🚀 ED Logística & Estoque")
menu = st.sidebar.selectbox("Navegação", ["Visão Geral & KPIs", "Movimentações (Entrada/Saída)", "Gestão de Entregas", "Cadastrar Produtos"])

# ----------------------------------------------------
# TELA 1: VISÃO GERAL & KPIS
# ----------------------------------------------------
if menu == "Visão Geral & KPIs":
    st.title("📊 Painel Executivo - Estoque & Logística")
    
    df_est = st.session_state['estoque']
    df_ent = st.session_state['entregas']
    
    valor_total = (df_est['Qtd_Atual'] * df_est['Custo_Unit']).sum()
    rupturas = len(df_est[df_est['Qtd_Atual'] <= df_est['Estoque_Min']])
    
    total_entregas = len(df_ent)
    no_prazo = len(df_ent[df_ent['Status'] == 'No Prazo'])
    otd_perc = (no_prazo / total_entregas * 100) if total_entregas > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Valor Total em Estoque", f"R$ {valor_total:,.2f}")
    with col2:
        st.metric("Itens em Ruptura", f"{rupturas} SKUs")
    with col3:
        st.metric("Total de SKUs", len(df_est))
    with col4:
        st.metric("OTD (Entregas no Prazo)", f"{otd_perc:.1f}%")

    st.divider()
    st.subheader("⚠️ Alertas de Estoque Mínimo")
    df_alerta = df_est[df_est['Qtd_Atual'] <= df_est['Estoque_Min']]
    if not df_alerta.empty:
        st.dataframe(df_alerta, use_container_width=True)
    else:
        st.success("Nenhum produto abaixo do estoque mínimo!")

# ----------------------------------------------------
# TELA 2: MOVIMENTAÇÕES (ENTRADAS E SAÍDAS)
# ----------------------------------------------------
elif menu == "Movimentações (Entrada/Saída)":
    st.title("🔄 Controle de Entradas e Saídas")
    
    with st.form("form_mov", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            sku_sel = st.selectbox("Produto (SKU)", st.session_state['estoque']['SKU'].tolist())
            tipo = st.selectbox("Tipo de Movimento", ["Entrada", "Saída"])
        with col2:
            qtd = st.number_input("Quantidade", min_value=1, value=10)
            doc = st.text_input("Número do Documento / NF", "NF-")
        with col3:
            parceiro = st.text_input("Fornecedor / Cliente", "Nome")
            data_mov = st.date_input("Data", datetime.today())
            
        submitted = st.form_submit_button("Registrar Movimentação")
        if submitted:
            idx = st.session_state['estoque'][st.session_state['estoque']['SKU'] == sku_sel].index[0]
            if tipo == "Entrada":
                st.session_state['estoque'].loc[idx, 'Qtd_Atual'] += qtd
            else:
                st.session_state['estoque'].loc[idx, 'Qtd_Atual'] -= qtd
                
            nova_mov = pd.DataFrame([{"Data": str(data_mov), "SKU": sku_sel, "Tipo": tipo, "Quantidade": qtd, "Documento": doc, "Parceiro": parceiro}])
            st.session_state['movimentos'] = pd.concat([st.session_state['movimentos'], nova_mov], ignore_index=True)
            st.success("Movimentação registrada com sucesso!")

    st.subheader("Histórico Recente")
    st.dataframe(st.session_state['movimentos'], use_container_width=True)

# ----------------------------------------------------
# TELA 3: GESTÃO DE ENTREGAS
# ----------------------------------------------------
elif menu == "Gestão de Entregas":
    st.title("🚚 Monitoramento de Entregas")
    
    with st.form("form_entrega", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            id_ent = st.text_input("ID da Entrega", "ENT-103")
            doc_ref = st.text_input("NF Vinculada", "NF-")
            cliente = st.text_input("Cliente Destino", "Nome")
        with c2:
            d_saida = st.date_input("Data de Saída", datetime.today())
            d_prev = st.date_input("Data Prevista", datetime.today())
        with c3:
            transportadora = st.text_icon = st.text_input("Transportadora", "Nome")
            status_ent = st.selectbox("Status", ["No Prazo", "Atrasado", "Em Trânsito"])
            
        btn_ent = st.form_submit_button("Cadastrar Entrega")
        if btn_ent:
            nova_ent = pd.DataFrame([{
                "ID_Entrega": id_ent, "Documento": doc_ref, "Cliente": cliente, 
                "Data_Saida": str(d_saida), "Data_Prevista": str(d_prev), 
                "Data_Real": str(d_prev) if status_ent == "No Prazo" else "Pendente",
                "Status": status_ent, "Transportadora": transportadora
            }])
            st.session_state['entregas'] = pd.concat([st.session_state['entregas'], nova_ent], ignore_index=True)
            st.success("Entrega cadastrada com sucesso!")

    st.subheader("Painel de Expedição")
    st.dataframe(st.session_state['entregas'], use_container_width=True)

# ----------------------------------------------------
# TELA 4: CADASTRAR PRODUTOS
# ----------------------------------------------------
elif menu == "Cadastrar Produtos":
    st.title("📦 Cadastro de Produtos")
    
    with st.form("form_prod", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            sku = st.text_input("Código SKU", "SKU-004")
            nome = st.text_input("Nome do Produto", "Descrição")
            cat = st.text_input("Categoria", "Peças")
        with c2:
            min_est = st.number_input("Estoque Mínimo", min_value=0, value=20)
            custo = st.number_input("Custo Unitário (R$)", min_value=0.0, value=10.0)
            qtd_inicial = st.number_input("Saldo Inicial", min_value=0, value=100)
            
        btn_prod = st.form_submit_button("Salvar Produto")
        if btn_prod:
            novo_p = pd.DataFrame([{
                "SKU": sku, "Produto": nome, "Categoria": cat, 
                "Estoque_Min": min_est, "Custo_Unit": custo, "Qtd_Atual": qtd_inicial
            }])
            st.session_state['estoque'] = pd.concat([st.session_state['estoque'], novo_p], ignore_index=True)
            st.success(f"Produto {sku} salvo com sucesso!")
            
    st.subheader("Base de Produtos")
    st.dataframe(st.session_state['estoque'], use_container_width=True)
