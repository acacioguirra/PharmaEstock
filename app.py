import streamlit as st
import pandas as pd
from datetime import datetime
import database as db

# Configuração da Página
st.set_page_config(page_title="PharmaStock", page_icon="💊", layout="wide")

# Inicializar Banco de Dados
db.init_db()

# --- GERENCIAMENTO DE SESSÃO ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'username' not in st.session_state:
    st.session_state.username = None

def login():
    st.title("🔐 Login PharmaStock")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        
        if st.button("Entrar", type="primary"):
            role = db.verificar_login(username, password)
            if role:
                st.session_state.logged_in = True
                st.session_state.user_role = role
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.rerun()

# --- TELAS DO SISTEMA ---

def main_system():
    # Sidebar
    st.sidebar.title(f"Olá, {st.session_state.username}")
    st.sidebar.text(f"Perfil: {st.session_state.user_role.upper()}")
    
    menu_options = ["Visão Geral", "Cadastrar Medicamento", "Gerenciar Estoque"]
    
    # Opção extra apenas para ADMIN
    if st.session_state.user_role == 'admin':
        menu_options.append("Gerenciar Usuários")
        
    choice = st.sidebar.radio("Menu", menu_options)
    
    if st.sidebar.button("Sair"):
        logout()

    # --- TELA: VISÃO GERAL ---
    # --- TELA: VISÃO GERAL (ATUALIZADA) ---
    if choice == "Visão Geral":
        st.title("📊 Visão Geral do Estoque")
        
        # 1. Carregar dados
        dados = db.listar_medicamentos()
        
        if dados:
            df = pd.DataFrame(dados)
            
            # 2. Criar campo de busca/filtro
            st.markdown("### 🔍 Consultar Medicamento")
            termo_busca = st.text_input("Digite o nome do medicamento para buscar:", placeholder="Ex: Dipirona")
            
            # 3. Lógica de Filtragem
            if termo_busca:
                # Filtra onde o 'nome' contém o texto digitado (ignora maiúsculas/minúsculas)
                df_filtrado = df[df['nome'].str.contains(termo_busca, case=False, na=False)]
            else:
                df_filtrado = df # Se não digitar nada, mostra tudo

            # 4. Exibição Inteligente
            if df_filtrado.empty:
                st.warning(f"Nenhum medicamento encontrado com o nome '{termo_busca}'.")
            
            else:
                # Se encontrou exatamente 1 medicamento (ou se a lista for pequena), mostra destaque
                if len(df_filtrado) == 1:
                    item = df_filtrado.iloc[0]
                    
                    st.divider()
                    st.subheader(f"📦 Detalhes de: {item['nome']}")
                    
                    # Cartões de destaque (Métricas)
                    col1, col2, col3 = st.columns(3)
                    
                    # Coloração visual para validade
                    hoje = datetime.now().date()
                    data_val = datetime.strptime(item['validade'], '%d/%m/%Y').date()
                    dias_vencimento = (data_val - hoje).days
                    
                    cor_delta = "normal"
                    if dias_vencimento < 0:
                        cor_delta = "inverse" # Vencido (Vermelho)
                    elif dias_vencimento < 30:
                        cor_delta = "off" # Perto de vencer (Cinza/Amarelo dependendo do tema)

                    col1.metric("Quantidade em Estoque", f"{item['quantidade']} un")
                    col2.metric("Data de Validade", item['validade'], delta=f"{dias_vencimento} dias", delta_color=cor_delta)
                    col3.metric("Lote", item['lote'])
                    st.divider()

                # Tabela Geral (Sempre visível)
                st.write(f"Resultados encontrados: {len(df_filtrado)}")
                
                # Destaca as colunas que você pediu
                st.dataframe(
                    df_filtrado[['nome', 'quantidade', 'validade', 'lote', 'fabricante']], 
                    use_container_width=True,
                    hide_index=True
                )
                
        else:
            st.info("Nenhum medicamento cadastrado no sistema ainda.")

    # --- TELA: CADASTRAR ---
    elif choice == "Cadastrar Medicamento":
        st.title("💊 Novo Medicamento")
        
        with st.form("form_cadastro"):
            col1, col2 = st.columns(2)
            nome = col1.text_input("Nome do Medicamento")
            fabricante = col2.text_input("Fabricante")
            
            col3, col4, col5 = st.columns(3)
            lote = col3.text_input("Lote")
            validade = col4.text_input("Validade (DD/MM/AAAA)")
            qtd = col5.number_input("Quantidade Inicial", min_value=0, step=1)
            
            submit = st.form_submit_button("Salvar Medicamento")
            
            if submit:
                if nome and lote and validade:
                    try:
                        # Validação simples de data
                        datetime.strptime(validade, '%d/%m/%Y')
                        
                        dados = {
                            "nome": nome, "lote": lote, 
                            "validade": validade, "fabricante": fabricante, 
                            "quantidade": qtd
                        }
                        db.cadastrar_medicamento(dados)
                        st.success(f"Medicamento '{nome}' cadastrado com sucesso!")
                    except ValueError:
                        st.error("Formato de data inválido. Use DD/MM/AAAA")
                else:
                    st.warning("Preencha os campos obrigatórios.")

    # --- TELA: GERENCIAR ---
    elif choice == "Gerenciar Estoque":
        st.title("📦 Gerenciamento de Estoque")
        dados = db.listar_medicamentos()
        
        if dados:
            df = pd.DataFrame(dados)
            med_selecionado = st.selectbox("Selecione um medicamento para editar/remover:", 
                                         options=df['id'], 
                                         format_func=lambda x: f"{x} - {df[df['id']==x]['nome'].values[0]}")
            
            item = df[df['id'] == med_selecionado].iloc[0]
            
            st.write(f"**Item Selecionado:** {item['nome']} | **Lote:** {item['lote']}")
            
            c1, c2 = st.columns(2)
            
            # Atualizar Quantidade
            with c1:
                st.subheader("Atualizar Quantidade")
                nova_qtd = st.number_input("Nova Quantidade", value=int(item['quantidade']), step=1)
                if st.button("Atualizar"):
                    db.atualizar_quantidade(int(item['id']), nova_qtd)
                    st.success("Estoque atualizado!")
                    st.rerun()
            
            # Excluir
            with c2:
                st.subheader("Zona de Perigo")
                if st.button("🗑️ Excluir Medicamento", type="primary"):
                    db.excluir_medicamento(int(item['id']))
                    st.warning("Medicamento removido.")
                    st.rerun()
        else:
            st.info("Nada para gerenciar.")

    # --- TELA: ADMIN (CRIAR USUÁRIOS) ---
    elif choice == "Gerenciar Usuários":
        st.title("👥 Gerenciamento de Usuários")
        st.info("Área restrita a Administradores")
        
        with st.form("novo_usuario"):
            new_user = st.text_input("Novo Nome de Usuário")
            new_pass = st.text_input("Nova Senha", type="password")
            new_role = st.selectbox("Perfil", ["user", "admin"])
            
            if st.form_submit_button("Criar Usuário"):
                if len(new_pass) < 4:
                    st.error("A senha deve ter pelo menos 4 caracteres.")
                else:
                    sucesso = db.criar_usuario(new_user, new_pass, new_role)
                    if sucesso:
                        st.success(f"Usuário {new_user} criado com sucesso!")
                    else:
                        st.error("Usuário já existe.")

# --- LÓGICA PRINCIPAL ---
if __name__ == "__main__":
    if st.session_state.logged_in:
        main_system()
    else:
        login()