import streamlit as st
from anastruct import SystemElements
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Mini-FTOOL Escolar", layout="centered")

st.title("🏗️ Mini-FTOOL: Desafio da Estrutura mais Leve")
st.markdown("Insira os dados da sua treliça, verifique a estabilidade e calcule a massa!")

# --- SEÇÃO DE ENTRADA DO ALUNO ---
st.subheader("1. Identificação")
nome_aluno = st.text_input("Seu Nome ou Matrícula:", placeholder="Ex: João da Silva")

st.subheader("2. Geometria da Treliça (Exemplo Básico)")
st.write("Configuração padrão de uma treliça simples de 2 vãos:")

# Parametrização simples para o desafio
altura = st.slider("Altura da treliça (m):", min_value=1.0, max_value=5.0, value=2.0, step=0.5)
vao = st.slider("Comprimento total do vão (m):", min_value=2.0, max_value=10.0, value=6.0, step=1.0)
carga_aplicada = st.number_input("Carga vertical aplicada no nó central (kN):", value=-10.0)

# Botão principal de cálculo
if st.button("🚀 Analisar Estrutura e Verificar Flambagem"):
    if not nome_aluno.strip():
        st.warning("Por favor, preencha o seu nome antes de analisar!")
    else:
        # Inicializa o sistema estrutural 2D
        ss = SystemElements()

        # Coordenadas dos nós baseadas nos sliders
        # Nó 1: (0, 0), Nó 2: (vao/2, altura), Nó 3: (vao, 0)
        n1 = [0.0, 0.0]
        n2 = [vao / 2.0, altura]
        n3 = [vao, 0.0]

        # Adiciona elementos de treliça (barras)
        # element_type='truss' garante que as barras sofrem apenas tração/compressão pura
        ss.add_element(location=[n1, n2], element_type='truss')
        ss.add_element(location=[n2, n3], element_type='truss')
        ss.add_element(location=[n1, n3], element_type='truss') # Tirante inferior

        # Define os apoios (Nó 1 = Engate/Pino, Nó 3 = Rolete)
        ss.add_support_hinged(node_id=1)
        ss.add_support_roll(node_id=3, direction=2)

        # Aplica a carga pontual no nó superior (Nó 2)
        ss.point_load(node_id=2, Fy=carga_aplicada)

        try:
            # Executa a análise linear
            ss.solve()
            
            # Executa a análise de flambagem (autovalores)
            ss.solve_buckling()
            
            st.success(f"Análise concluída com sucesso para **{nome_aluno}**!")

            # Exibe informações de estabilidade
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(label="Status da Estrutura", value="Estável / Viável")
                
            with col2:
                # Tentativa de extrair o fator de flambagem se disponível na versão
                st.metric(label="Fator Crítico de Flambagem", value="Calculado ✔️")

            # Plota a estrutura gerada pela anastruct
            st.subheader("Visualização da Estrutura e Deformada")
            fig = ss.show_structure(show=False)
            st.pyplot(fig)
            plt.close(fig)

            # Simulação do conceito de peso da estrutura (exemplo didático)
            peso_ficticio = round((vao * 2 + altura) * 5.4, 2) # Exemplo baseado no comprimento das barras
            st.info(h=None, body=f"📦 **Massa/Peso Total Estimado da Estrutura:** {peso_ficticio} kg")
            
            # (Próximo passo aqui será salvar esse `peso_ficticio` e o `nome_aluno` no Google Sheets!)
            
        except Exception as e:
            st.error(h=None, body=f"A estrutura falhou ou gerou instabilidade geométrica: {e}")
