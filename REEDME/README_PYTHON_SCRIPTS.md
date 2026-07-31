# 🧬 Drug-Target Interaction Prediction - Python Scripts

Converted from Jupyter Notebooks to Python scripts for command-line execution.

## 📁 Files Overview

- **01_drug_target_models.py** - Model architectures (Transformer + CNN + MLP)
- **02_smiles_to_fingerprint.py** - SMILES parser and Morgan fingerprint generator (NO RDKit!)
- **03_training_pipeline.py** - Complete training pipeline on BindingDB
- **04_practical_applications.py** - Real-world applications (drug repurposing, virtual screening)
- **requirements.txt** - Python dependencies

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install torch numpy pandas scikit-learn scipy matplotlib seaborn tqdm
```

### Step 2: Test Model Architectures

```bash
python 01_drug_target_models.py
```

This will:
- Create all model components
- Test forward pass
- Display model parameters (~4.5M)

### Step 3: Test SMILES Converter

```bash
python 02_smiles_to_fingerprint.py
```

This will:
- Test SMILES parser on example molecules
- Generate Morgan fingerprints
- Verify batch processing

### Step 4: Train on BindingDB

```bash
python 03_training_pipeline.py --data_path F:/DTI/BindingDB.csv --sample_size 5000 --epochs 50
```

**Command-line arguments:**
- `--data_path`: Path to BindingDB CSV file (default: F:/DTI/BindingDB.csv)
- `--sample_size`: Number of samples to use (default: 5000, use None for all data)
- `--batch_size`: Batch size (default: 64)
- `--epochs`: Number of epochs (default: 50)
- `--learning_rate`: Learning rate (default: 1e-4)
- `--patience`: Early stopping patience (default: 10)
- `--num_layers`: Number of transformer layers (default: 6)
- `--save_path`: Path to save best model (default: bindingdb_best_model.pt)

**Example with full dataset:**
```bash
python 03_training_pipeline.py --data_path F:/DTI/BindingDB.csv --sample_size None --epochs 100
```

### Step 5: Run Practical Applications

```bash
python 04_practical_applications.py --model_path bindingdb_best_model.pt --app all
```

**Command-line arguments:**
- `--model_path`: Path to trained model (default: bindingdb_best_model.pt)
- `--app`: Which application to run (choices: covid, egfr, all)

**Run specific applications:**
```bash
# COVID-19 drug repurposing only
python 04_practical_applications.py --app covid

# EGFR virtual screening only
python 04_practical_applications.py --app egfr
```

## 📊 Expected Outputs

### Training (Script 3)
- **Model checkpoint**: `bindingdb_best_model.pt`
- **Training plot**: `training_history.png`
- **Predictions plot**: `test_predictions.png`
- **Console output**: Epoch-by-epoch metrics (Loss, R², C-Index)

### Applications (Script 4)
- **COVID-19 results**: `covid_drug_repurposing.png`
- **EGFR results**: `virtual_screening.png`
- **Console output**: Top drug candidates with predicted pKd values

## ⚙️ Configuration

### Model Hyperparameters
Edit the `config` dictionary in `03_training_pipeline.py`:

```python
config = {
    'drug_input_dim': 1024,
    'drug_d_model': 128,
    'drug_num_layers': 6,  # More layers = better accuracy, slower training
    'drug_num_heads': 8,
    'drug_d_ff': 512,
    'drug_hidden_dim': 256,
    'target_vocab_size': 26,
    'target_embedding_dim': 128,
    'target_num_filters': [32, 64, 96],
    'target_kernel_sizes': [4, 8, 12],
    'target_hidden_dim': 256,
    'decoder_hidden_dims': [1024, 512, 256],
    'dropout': 0.1,
}
```

## 🐛 Troubleshooting

### Import Error
**Problem**: `ImportError: cannot import name 'DrugTargetInteractionModel'`

**Solution**: Make sure all files are in the same directory. The scripts import from each other:
- Script 3 imports from Scripts 1 & 2
- Script 4 imports from Scripts 1, 2 & 3

### Memory Error
**Problem**: `RuntimeError: CUDA out of memory`

**Solution**: Reduce batch size or use CPU:
```bash
# Smaller batch size
python 03_training_pipeline.py --batch_size 32

# Use CPU (slower but won't run out of memory)
# The script automatically detects if CUDA is unavailable
```

### File Not Found
**Problem**: `FileNotFoundError: F:/DTI/BindingDB.csv`

**Solution**: Update the data path to your actual file location:
```bash
python 03_training_pipeline.py --data_path /path/to/your/BindingDB.csv
```

## 💡 Tips for Best Results

### For Quick Testing (15-30 minutes)
```bash
python 03_training_pipeline.py \
    --sample_size 1000 \
    --epochs 20 \
    --num_layers 4 \
    --batch_size 128
```

### For Best Accuracy (6-8 hours)
```bash
python 03_training_pipeline.py \
    --sample_size None \
    --epochs 100 \
    --num_layers 8 \
    --batch_size 64
```

### For Production (overnight training)
```bash
python 03_training_pipeline.py \
    --sample_size None \
    --epochs 200 \
    --num_layers 8 \
    --batch_size 64 \
    --patience 20
```

## 📈 Performance Expectations

| Dataset Size | Training Time (GPU) | Expected R² | Expected C-Index |
|--------------|---------------------|-------------|------------------|
| 1,000        | 15 min              | 0.50-0.60   | 0.65-0.75        |
| 5,000        | 1-2 hours           | 0.60-0.70   | 0.70-0.80        |
| 10,000       | 2-3 hours           | 0.65-0.75   | 0.75-0.85        |
| 38,000 (all) | 6-8 hours           | 0.70-0.80   | 0.80-0.90        |

## 🎯 Workflow Example

Complete end-to-end workflow:

```bash
# 1. Test everything works
python 01_drug_target_models.py
python 02_smiles_to_fingerprint.py

# 2. Quick training test (1000 samples)
python 03_training_pipeline.py \
    --data_path F:/DTI/BindingDB.csv \
    --sample_size 1000 \
    --epochs 10

# 3. Check if it worked
ls -l bindingdb_best_model.pt

# 4. Full training (if test worked)
python 03_training_pipeline.py \
    --data_path F:/DTI/BindingDB.csv \
    --sample_size 10000 \
    --epochs 50

# 5. Run applications
python 04_practical_applications.py \
    --model_path bindingdb_best_model.pt \
    --app all
```

## 📝 Notes

### Key Differences from Notebooks:
1. **No Google Colab mount** - Direct file paths
2. **Command-line arguments** - Flexible configuration
3. **No `display()`** - Uses `print()` instead
4. **Imports between scripts** - Modules import from each other
5. **No interactive widgets** - Pure command-line interface

### Advantages of Python Scripts:
- ✅ Faster execution (no notebook overhead)
- ✅ Better for automation and batch jobs
- ✅ Easier version control
- ✅ Can be imported as modules
- ✅ Better for production deployment

### When to Use Notebooks vs Scripts:
- **Use Notebooks**: Interactive exploration, visualization, teaching
- **Use Scripts**: Production training, batch processing, deployment

## 🎓 Learning Path

1. **Day 1**: Run scripts 1-2, understand architecture
2. **Day 2**: Small training test (1000 samples)
3. **Day 3**: Medium training (5000 samples)
4. **Day 4**: Full training (all data)
5. **Day 5**: Applications and fine-tuning

## 🚀 Next Steps

After completing training:
1. Fine-tune on specific targets
2. Add more molecular descriptors
3. Experiment with different architectures
4. Deploy as web service
5. Validate with experimental data

## 📞 Support

If you encounter issues:
1. Check Python version (3.8+)
2. Verify CUDA installation (if using GPU)
3. Check file paths are correct
4. Ensure all dependencies are installed

## ✅ Success Checklist

- [ ] Dependencies installed
- [ ] Script 1 runs successfully
- [ ] Script 2 runs successfully
- [ ] Data file accessible
- [ ] Script 3 training completes
- [ ] Model checkpoint saved
- [ ] Script 4 generates results
- [ ] Output plots created

---

**Made with ❤️ for drug discovery research**

**بُني بحب ❤️ لأبحاث اكتشاف الأدوية**
