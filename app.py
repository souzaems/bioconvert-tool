import streamlit as st
from Bio import SeqIO
from io import StringIO

# Configuração da Página
st.set_page_config(page_title="BioConvert - Érica Souza", page_icon="dna")

st.title("🧬 BioConvert: Conversor de Formatos Biológicos")
st.markdown("""
Esta ferramenta converte arquivos **FASTA** para formatos comuns em filogenia (**NEXUS, PHYLIP**).
*Desenvolvido por [Érica Souza](https://github.com/souzaems)*
""")

# --- NOVO: Seleção do tipo de molécula (Corrige o erro do Nexus) ---
molecule_type = st.radio(
    "Qual o tipo das sequências?",
    ("DNA", "Protein", "RNA"),
    horizontal=True
)

# Upload do Arquivo
uploaded_file = st.file_uploader("Arraste seu arquivo FASTA aqui", type=["fasta", "fas", "fa"])

if uploaded_file is not None:
    # Ler o arquivo
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    
    try:
        # Lê as sequências
        sequences = list(SeqIO.parse(stringio, "fasta"))
        count = len(sequences)
        
        # --- A CORREÇÃO MÁGICA AQUI ---
        # Atribuímos manualmente o tipo de molécula para cada sequência
        # O Biopython precisa disso para escrever o cabeçalho do NEXUS corretamente
        for seq in sequences:
            seq.annotations["molecule_type"] = molecule_type
        # ------------------------------

        st.success(f"Arquivo carregado com sucesso! {count} sequências identificadas.")
        
        st.divider()
        st.subheader("Escolha o formato para download:")

        # --- Conversão para NEXUS ---
        nexus_output = StringIO()
        # Agora o SeqIO sabe que é DNA/Proteína e não vai dar erro
        SeqIO.write(sequences, nexus_output, "nexus")
        
        st.download_button(
            label="Baixar em NEXUS (.nex)",
            data=nexus_output.getvalue(),
            file_name="converted_sequences.nex",
            mime="text/plain"
        )

        # --- Conversão para PHYLIP (Relaxed) ---
        phylip_output = StringIO()
        SeqIO.write(sequences, phylip_output, "phylip-relaxed")
        st.download_button(
            label="Baixar em PHYLIP Relaxed (.phy)",
            data=phylip_output.getvalue(),
            file_name="converted_sequences.phy",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"Erro ao converter. Detalhes técnicos: {e}")

# Rodapé
st.markdown("---")
st.caption("Ferramenta criada com Python, Biopython e Streamlit.")
