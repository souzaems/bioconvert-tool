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

# Upload do Arquivo
uploaded_file = st.file_uploader("Arraste seu arquivo FASTA aqui", type=["fasta", "fas", "fa"])

if uploaded_file is not None:
    # Ler o arquivo
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    
    # Tentar ler as sequências
    try:
        sequences = list(SeqIO.parse(stringio, "fasta"))
        count = len(sequences)
        st.success(f"Arquivo carregado com sucesso! {count} sequências identificadas.")
        
        st.divider()
        st.subheader("Escolha o formato para download:")

        # --- Conversão para NEXUS ---
        nexus_output = StringIO()
        SeqIO.write(sequences, nexus_output, "nexus")
        st.download_button(
            label="Baixar em NEXUS (.nex)",
            data=nexus_output.getvalue(),
            file_name="converted_sequences.nex",
            mime="text/plain"
        )

        # --- Conversão para PHYLIP (Relaxed) ---
        # Phylip normal corta nomes com 10 caracteres. Relaxed permite nomes longos.
        phylip_output = StringIO()
        SeqIO.write(sequences, phylip_output, "phylip-relaxed")
        st.download_button(
            label="Baixar em PHYLIP Relaxed (.phy)",
            data=phylip_output.getvalue(),
            file_name="converted_sequences.phy",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"Erro ao ler o arquivo FASTA. Verifique a formatação. Detalhes: {e}")

# Rodapé
st.markdown("---")
st.caption("Ferramenta criada com Python, Biopython e Streamlit.")
