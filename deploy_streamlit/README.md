# Drug-Target Interaction Prediction (Streamlit)

Streamlit web app that predicts the binding affinity between a drug and a target
protein using a pretrained DeepPurpose model (`Transformer` drug encoder + `CNN`
target encoder, DBTA architecture).

This folder is self-contained and can be deployed to free hosting such as
[Streamlit Community Cloud](https://streamlit.io/cloud) directly from a GitHub
repository.

## Files

- `streamlit_app.py` - the Streamlit app (main entry point).
- `requirements.txt` - Python dependencies.
- `DTI_Model/` - pretrained model files (`config.pkl` + `model.pt`).
- `data/Modified Data.csv` - drug/target lookup table.

## Deploy on Streamlit Community Cloud (free)

1. Push this repository to GitHub (the whole repo, or just this folder).
2. Go to <https://streamlit.io/cloud> and sign in with GitHub.
3. Click **New app** -> choose the repository, branch `master`, and set the main
   file path to `deploy_streamlit/streamlit_app.py`.
4. Click **Deploy**.

Notes:

- The app installs `DeepPurpose==0.1.5` at runtime with `--no-deps` (to avoid
  its heavy/uninstallable dependencies such as `descriptastorus`, `dgl`, and
  `ax-platform`), then patches `DeepPurpose/utils.py` to remove the
  `descriptastorus` import before importing the package.
- `torch` is installed from the official CPU wheel index via the
  `--extra-index-url` line in `requirements.txt`.
- Model loading takes a while on the first request; subsequent requests use a
  cached instance.

## Important caveat

The dataset targets are **UniProt identifiers** (e.g. `Q9GZT9`), not amino-acid
sequences. The original Flask app feeds these identifiers directly into the CNN
target encoder (non-amino-acid characters are mapped to `?`). The Streamlit app
replicates that behavior in the "Select from dataset" tab. For a scientifically
meaningful prediction, use the **Custom input** tab with a real SMILES string and
a real amino-acid sequence.
