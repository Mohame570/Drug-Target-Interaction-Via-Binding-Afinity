import os
import sys

APP_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(APP_DIR)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

import numpy as np
import pandas as pd
import streamlit as st
from rdkit import Chem

# rdkit.Chem.Draw needs X11 system libraries (installed via packages.txt on
# Streamlit Cloud); degrade gracefully if they are unavailable.
try:
    from rdkit.Chem import Draw
except ImportError:
    Draw = None

# DeepPurpose 0.1.5 is vendored (pre-patched) under ./DeepPurpose so no pip
# install is needed at build or runtime time.
try:
    from DeepPurpose import utils
    from DeepPurpose import DTI as models
except ImportError as exc:
    raise RuntimeError(
        "The vendored DeepPurpose package is missing. Expected it at: "
        + os.path.join(APP_DIR, "DeepPurpose")
    ) from exc

DRUG_ENCODING = "Transformer"
TARGET_ENCODING = "CNN"

DATA_FILE = os.path.join(APP_DIR, "data", "Modified Data.csv")
MODEL_DIR = os.path.join(APP_DIR, "DTI_Model")

st.set_page_config(page_title="Drug-Target Interaction Prediction", page_icon=":dna:", layout="centered")


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    for col in ("uniqueDri", "drugName", "uniqueTa", "targetName", "organism"):
        df[col] = df[col].fillna("").astype(str).str.strip()
    drugs = df[["uniqueDri", "drugName", "organism"]].drop_duplicates()
    targets = df[["uniqueTa", "targetName", "organism"]].drop_duplicates()
    return df, drugs, targets


@st.cache_resource(show_spinner="Loading pretrained DTI model...")
def load_model():
    return models.model_pretrained(path_dir=MODEL_DIR)


def predict(model, drug_smiles, target_seq):
    X_pred = utils.data_process(
        [drug_smiles],
        [target_seq],
        [1],
        DRUG_ENCODING,
        TARGET_ENCODING,
        split_method="no_split",
    )
    return float(model.predict(X_pred)[0])


def _render_result(drug_name, drug_smiles, drug_organism, target_name, target_id, target_organism, affinity):
    mol = Chem.MolFromSmiles(drug_smiles)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Drug")
        st.write(f"**Name:** {drug_name}")
        if drug_organism:
            st.write(f"**Organism:** {drug_organism}")
        st.write(f"**SMILES:** `{drug_smiles}`")
        if mol is not None:
            if Draw is not None:
                try:
                    img = Draw.MolToImage(mol, size=(400, 400))
                    st.image(img, caption=drug_name)
                except Exception:
                    pass
            st.write(f"**Number of atoms:** {mol.GetNumAtoms()}")
        else:
            st.warning("Could not render the molecular structure.")
    with col2:
        st.subheader("Target")
        st.write(f"**Name:** {target_name}")
        if target_organism:
            st.write(f"**Organism:** {target_organism}")
        st.write(f"**Target ID / Sequence:** `{target_id}`")
    st.markdown("---")
    st.subheader("Prediction")
    st.metric("Predicted Binding Affinity", f"{affinity:.4f}")


st.title("Drug-Target Interaction Prediction")
st.markdown(
    "Predict the binding affinity between a drug and a target protein using a "
    "pretrained DeepPurpose model (Transformer drug encoder + CNN target encoder)."
)

df, drugs, targets = load_data()

tab1, tab2 = st.tabs(["Select from dataset", "Custom input"])

with tab1:
    drug_names = sorted(drugs["drugName"].unique().tolist())
    target_names = sorted(targets["targetName"].unique().tolist())
    with st.form("dataset_form"):
        drug_name = st.selectbox("Select Drug", drug_names)
        target_name = st.selectbox("Select Target Protein", target_names)
        submitted = st.form_submit_button("Predict Binding Affinity", type="primary")

    if submitted:
        drug_row = drugs[drugs["drugName"] == drug_name].iloc[0]
        target_row = targets[targets["targetName"] == target_name].iloc[0]
        with st.spinner("Predicting..."):
            model = load_model()
            affinity = predict(model, drug_row["uniqueDri"], target_row["uniqueTa"])
        _render_result(
            drug_name, drug_row["uniqueDri"], drug_row["organism"],
            target_name, target_row["uniqueTa"], target_row["organism"], affinity,
        )
        st.info(
            "Note: the dataset targets are UniProt identifiers rather than amino-acid "
            "sequences, so these predictions follow the original app behavior. For a "
            "scientifically meaningful prediction, use the Custom input tab with a real "
            "protein sequence."
        )

with tab2:
    with st.form("custom_form"):
        custom_smiles = st.text_input("Drug SMILES", value="CCO")
        custom_seq = st.text_area("Target Protein Sequence (amino acids)", height=120)
        custom_submitted = st.form_submit_button("Predict Binding Affinity", type="primary")

    if custom_submitted:
        custom_smiles = custom_smiles.strip()
        custom_seq = custom_seq.strip()
        if not custom_smiles or not custom_seq:
            st.warning("Please provide both a SMILES string and a protein sequence.")
        else:
            mol = Chem.MolFromSmiles(custom_smiles)
            if mol is None:
                st.error("Invalid SMILES string.")
            else:
                with st.spinner("Predicting..."):
                    model = load_model()
                    affinity = predict(model, custom_smiles, custom_seq)
                shown_seq = custom_seq[:40] + ("..." if len(custom_seq) > 40 else "")
                _render_result("Custom drug", custom_smiles, "-", "Custom target", shown_seq, "-", affinity)
