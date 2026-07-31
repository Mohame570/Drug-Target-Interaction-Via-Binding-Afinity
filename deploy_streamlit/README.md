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
- `DeepPurpose/` - DeepPurpose 0.1.5 vendored and pre-patched so no `pip
  install` is needed at build or runtime time.
- `DTI_Model/` - pretrained model files (`config.pkl` + `model.pt`).
- `data/Modified Data.csv` - drug/target lookup table.

## Deploy on Streamlit Community Cloud (free)

1. Push this repository to GitHub (the whole repo, or just this folder).
2. Go to <https://streamlit.io/cloud> and sign in with GitHub.
3. Click **New app** -> choose the repository, branch `master`, and set the main
   file path to `deploy_streamlit/streamlit_app.py`.
4. In **Advanced settings**, select **Python 3.14** (the pinned wheels require
   it; Python 3.12/3.13 also work).
5. Click **Deploy**.

Notes:

- All dependencies are unpinned (except `torch`) so pip picks wheels that match
  the Python version the platform provides.
- `torch` is installed from the official CPU-only wheel index
  (`https://download.pytorch.org/whl/cpu`) via the `--extra-index-url` line in
  `requirements.txt`, so the small CPU build is used instead of the multi-GB
  CUDA build. A harmless `uv` warning/retry with a `403` from that index appears
  in the build logs before the pip fallback succeeds - this is expected.
- DeepPurpose 0.1.5 is **vendored** in the `DeepPurpose/` folder with two
  patches already applied, so the app never runs `pip install` at runtime (the
  Streamlit runtime has no `pip`):
  - the `descriptastorus` import is removed from `DeepPurpose/utils.py`, and
  - `weights_only=False` is forced on the `torch.load` call in
    `DeepPurpose/DTI.py` (torch >= 2.6 defaults to `weights_only=True`, which
    would reject the checkpoint's pickle format).
- Model loading takes a while on the first request; subsequent requests use a
  cached instance.

## Important caveat

The dataset targets are **UniProt identifiers** (e.g. `Q9GZT9`), not amino-acid
sequences. The original Flask app feeds these identifiers directly into the CNN
target encoder (non-amino-acid characters are mapped to `?`). The Streamlit app
replicates that behavior in the "Select from dataset" tab. For a scientifically
meaningful prediction, use the **Custom input** tab with a real SMILES string and
a real amino-acid sequence.
