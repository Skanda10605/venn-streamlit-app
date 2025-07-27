import re
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from venn import venn  

st.title("🧬 Venn Diagram Generator")

# Upload file
table = st.file_uploader("Upload a CSV file", type="csv")

if table is not None:
    df = pd.read_csv(table)

    # Check if required column exists
    if 'High glucose' in df.columns:
        df['normal glucose'] = (df['High glucose'] != 1).astype(int)
    else:
        st.error("The file must contain a 'High glucose' column.")
    
    # Let user pick features for the Venn diagram
    binary_features = df.columns[df.isin([0, 1]).all()]  # auto-detect binary columns
    selected = st.multiselect("Select exactly 4 binary features for Venn diagram:", binary_features)

    if len(selected) == 4:
        data_dict = {feat: set(df.index[df[feat] == 1]) for feat in selected}

        fig, ax = plt.subplots(figsize=(8, 6))
        venn(data_dict, ax=ax)
        ax.set_title("Venn Diagram for Selected Features")
        st.pyplot(fig)

    elif len(selected) > 0:
        st.warning("Please select exactly 4 binary (0/1) features.")
