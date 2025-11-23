import streamlit as st
from Bio import SeqIO
from io import StringIO

st.set_page_config(page_title="BioConvert Pro - Érica Souza", page_icon="🧬")

st.title("🧬 BioConvert Pro")
st.markdown("Converta **FASTA ou GenBank** para NEXUS/PHYLIP com Python.")

# 1. Sidebar para configurações (Deixa a tela principal limpa)
with st.sidebar:
    st.header("Configurações")
    input_format = st.selectbox(
        "Formato de Entrada:",
        ("fasta", "genbank")
    )
    molecule_type = st.radio(
        "Tipo da Molécula:",
        ("DNA", "Protein", "RNA")
    )

# 2. Abas: Upload de Arquivo OU Colar Texto (Melhor UX que o Bugaco)
tab1, tab2 = st.tabs(["📂 Upload de Arquivo", "📝 Colar Texto"])

sequences = []

# Lógica da Aba 1 (Arquivo)
with tab1:
    uploaded_file = st.file_uploader("Arraste seu arquivo aqui", type=["fasta", "fas", "gb", "txt"])
    if uploaded_file:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        try:
            sequences = list(SeqIO.parse(stringio, input_format))
        except Exception as e:
            st.error(f"Erro ao ler arquivo: {e}")

# Lógica da Aba 2 (Texto)
with tab2:
    text_input = st.text_area("Cole suas sequências aqui:", height=200)
    if text_input:
        stringio = StringIO(text_input)
        try:
            sequences = list(SeqIO.parse(stringio, input_format))
        except Exception as e:
            st.error(f"Erro ao ler texto colado. Verifique se o formato selecionado na barra lateral está correto.")

# 3. Processamento e Download (Só aparece se tiver sequências válidas)
if sequences:
    st.success(f"✅ Sucesso! {len(sequences)} sequências carregadas como **{input_format.upper()}**.")
    
    # Adicionar anotação de tipo (fix do Nexus)
    for seq in sequences:
        seq.annotations["molecule_type"] = molecule_type

    st.divider()
    col1, col2 = st.columns(2)

    # Botão NEXUS
    nexus_output = StringIO()
    SeqIO.write(sequences, nexus_output, "nexus")
    with col1:
        st.download_button(
            label="⬇️ Baixar NEXUS (.nex)",
            data=nexus_output.getvalue(),
            file_name="converted.nex",
            mime="text/plain",
            use_container_width=True
        )

    # Botão PHYLIP
    phylip_output = StringIO()
    SeqIO.write(sequences, phylip_output, "phylip-relaxed")
    with col2:
        st.download_button(
            label="⬇️ Baixar PHYLIP (.phy)",
            data=phylip_output.getvalue(),
            file_name="converted.phy",
            mime="text/plain",
            use_container_width=True
        )

elif (uploaded_file or text_input) and not sequences:
    st.warning("Nenhuma sequência encontrada. Verifique se escolheu o formato correto na barra lateral (Fasta vs GenBank).")
