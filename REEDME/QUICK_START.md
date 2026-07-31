# 🚀 QUICK START GUIDE - Ready to Run!

## ✅ Everything Updated for Your Data!

Your BindingDB.csv has been verified:
- **38,890 samples** ✅
- **Columns: Drug, Target, Y** ✅
- **No missing values** ✅
- **All scripts updated** ✅

---

## 📋 Choose Your Path:

### Path 1: Quick Test (15 minutes) 🏃‍♂️
**Just want to see if it works?**

```bash
python quick_comparison.py
```

Press Enter when asked for path (uses your data automatically).

**You'll see:**
- Baseline model training
- Enhanced model training
- Side-by-side comparison
- Improvement percentage

---

### Path 2: Small Training Test (2-3 hours) 🧪
**Test with 5,000 samples first:**

```bash
python 03_training_pipeline_enhanced.py \
    --sample_size 5000 \
    --epochs 50 \
    --batch_size 64 \
    --augment 1
```

**Expected result:** R² ≈ 0.72-0.75 (on this smaller sample)

---

### Path 3: Full Enhanced Training (8-12 hours) 🚀
**Train on all 38,890 samples:**

```bash
python 03_training_pipeline_enhanced.py \
    --sample_size None \
    --epochs 100 \
    --batch_size 64 \
    --learning_rate 0.0001 \
    --augment 1 \
    --patience 15 \
    --use_onecycle True
```

**Expected result:** R² ≈ 0.75-0.81

---

### Path 4: Optimize Then Train (12-16 hours total) 🎯
**Best approach - find optimal settings first:**

**Step 1: Find best hyperparameters (4-6 hours)**
```bash
python hyperparameter_optimization.py \
    --sample_size 5000 \
    --n_trials 50
```

This creates `best_config.json` with optimal settings.

**Step 2: Train with best settings (8-10 hours)**
```bash
# Check best_config.json for optimal values, then:
python 03_training_pipeline_enhanced.py \
    --sample_size None \
    --epochs 100 \
    --augment 1 \
    --d_model 128 \
    --num_layers 8 \
    --num_heads 8 \
    --d_ff 512 \
    --dropout 0.15 \
    --learning_rate 0.00015 \
    --batch_size 64
    # ^ Use values from best_config.json
```

**Expected result:** R² ≈ 0.78-0.83

---

### Path 5: Cross-Validation (20-30 hours) 🏆
**Most reliable, publication-ready:**

```bash
python 03_training_pipeline_enhanced.py \
    --use_cv True \
    --k_folds 5 \
    --sample_size 10000 \
    --epochs 100 \
    --augment 1 \
    --d_model 128 \
    --num_layers 8
```

**Expected result:** R² ≈ 0.79-0.84 with confidence intervals

---

## 🎯 Recommended Workflow:

### Week 1: Testing & Optimization

**Monday:** Quick test
```bash
python quick_comparison.py
```

**Tuesday:** Small training test
```bash
python 03_training_pipeline_enhanced.py --sample_size 5000 --epochs 50
```

**Wednesday-Thursday:** Hyperparameter optimization
```bash
python hyperparameter_optimization.py --sample_size 5000 --n_trials 50
```

**Friday:** Check results, read best_config.json

### Week 2: Full Training

**Monday-Tuesday:** Full training with best hyperparameters
```bash
python 03_training_pipeline_enhanced.py \
    --sample_size None --epochs 100 --augment 1 \
    # + best hyperparameters
```

**Wednesday-Friday:** (Optional) Cross-validation
```bash
python 03_training_pipeline_enhanced.py \
    --use_cv True --k_folds 5 --epochs 100
```

---

## 📊 Expected Timeline:

| Task | Time | Result |
|------|------|--------|
| Quick test | 15 min | See improvements |
| Small test | 2-3h | R² ≈ 0.72-0.75 |
| Hyperparameter opt | 4-6h | Get best settings |
| Full training | 8-12h | R² ≈ 0.75-0.81 |
| Cross-validation | 20-30h | R² ≈ 0.79-0.84 |

---

## 🔧 Troubleshooting:

### Problem: Out of Memory
```bash
# Solution: Reduce batch size
python 03_training_pipeline_enhanced.py --batch_size 32
```

### Problem: Too Slow
```bash
# Solution: Use smaller sample first
python 03_training_pipeline_enhanced.py --sample_size 10000
```

### Problem: Want faster test
```bash
# Solution: Fewer epochs
python 03_training_pipeline_enhanced.py --epochs 20
```

---

## 📈 Progress Tracking:

The script will show you:
```
Epoch 1/100
Train Loss: 2.4531 | Val Loss: 1.8234
MSE: 1.8234 | RMSE: 1.3503 | MAE: 0.9234
R²: 0.6234 | Pearson: 0.7891 | Spearman: 0.7654
C-Index: 0.7123 | Error Std: 1.2345
Learning Rate: 0.000100
✓ Saved best model
```

Watch the R² improve over epochs!

---

## 📁 Output Files:

After training, you'll get:
- `best_model_enhanced.pt` - Your trained model
- `test_predictions_enhanced.png` - Prediction plot
- `training_history.png` - Training curves
- Console output with all metrics

After hyperparameter optimization:
- `best_config.json` - Optimal settings
- `optuna_results.csv` - All tested configs
- `optimization_history.png` - Progress plot

---

## ✅ Pre-Flight Checklist:

Before starting:
- [ ] Dependencies installed: `pip install -r requirements_enhanced.txt`
- [ ] PyTorch installed with CUDA (for GPU)
- [ ] At least 16GB RAM available
- [ ] 8GB+ GPU memory (recommended)
- [ ] Enough disk space (~5GB)

Check with:
```bash
python test_data_compatibility.py
```

---

## 🎉 You're Ready!

Just copy-paste one of the commands above and start training!

**Simplest start:**
```bash
python quick_comparison.py
```

**Best start:**
```bash
python hyperparameter_optimization.py --n_trials 50
```

**Full training:**
```bash
python 03_training_pipeline_enhanced.py --epochs 100 --augment 1
```

---

## 📞 Need Help?

Check these files:
1. `DATA_UPDATED_SUMMARY.md` - What changed
2. `ENHANCED_TRAINING_GUIDE.md` - Detailed guide
3. `test_data_compatibility.py` - Verify setup

---

**Your data is ready. Your scripts are ready. Time to train! 🚀**
