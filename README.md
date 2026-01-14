# medrisk-features

![CI](https://github.com/rostandsurel/medrisk-features/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**medrisk-features** is a production-ready Python package for **medical, metabolic, behavioral and lifestyle feature engineering**, specifically designed for **explainable machine learning risk models** in healthcare analytics.

Built with a strong emphasis on **clinical interpretability**, **data leakage prevention**, and **production robustness**, this package bridges the gap between healthcare domain expertise and modern ML engineering practices.

---

## 🎯 Use Cases

- **Diabetes risk prediction** – glucose metabolism, insulin resistance, metabolic syndrome
- **Cardiometabolic risk modeling** – lipid profiles, blood pressure, BMI interactions
- **Preventive health analytics** – lifestyle factors, behavioral patterns, population screening
- **Insurance underwriting** – actuarial risk assessment with medical features
- **Clinical decision support** – interpretable features for healthcare AI systems

---

## ✨ Why medrisk-features?

### 🧠 **Clinically Grounded**
Every feature is based on established medical research and clinical guidelines (ADA, WHO, ESC standards).

### 🏗️ **Production-Ready Architecture**
- Modular design with clear separation of concerns
- Schema validation with actionable error messages
- Comprehensive logging via Loguru
- CI/CD integration with GitHub Actions
- Full test coverage with pytest

### 🔐 **Data Leakage Prevention**
Automatic detection and removal of target-leaking variables to ensure model generalization.

### 🧪 **Battle-Tested**
Unit-tested feature transformations with edge case handling and numerical stability checks.

### 📊 **ML Pipeline Compatible**
Seamlessly integrates with:
- scikit-learn pipelines
- XGBoost, LightGBM, CatBoost
- Kaggle notebooks
- MLflow tracking
- Production deployment environments

---

## 🧬 Feature Engineering Pipeline

The package follows a **medically coherent feature hierarchy**:

### 1. **Preprocessing Layer**
- Categorical variable harmonization
- Target leakage detection and removal
- Missing value strategies

### 2. **Demographics Features**
- `age_group` – flexible binning strategies (detailed/simple/senior)
- `socioeconomic_vulnerability` – composite risk indicator

### 3. **Medical (Clinical) Features**
- `glucose_category` – ADA-based fasting glucose classification
- `hba1c_category` – glycemic control stratification
- `bmi_category` – WHO BMI classification
- `bp_category` – blood pressure staging (JNC guidelines)
- `homa_ir` – insulin resistance index
- `metabolic_syndrome_flag` – ATP III diagnostic criteria

### 4. **Clinical Interactions**
- `lipid_ratio_hdl_ldl` – atherogenic index
- `cholesterol_hdl_ratio` – cardiovascular risk marker
- `bmi_glucose_interaction` – obesity-glycemia synergy
- `glucose_variability` – glycemic instability indicator

### 5. **Advanced Metabolic Features**
- `glycemic_load` – carbohydrate metabolism burden
- `dyslipidemia_flag` – lipid disorder indicator
- `cardiometabolic_burden` – composite risk score
- `blood_pressure_ratio` – systolic/diastolic imbalance

### 6. **Behavioral Features**
- `physical_activity_adequate` – WHO activity recommendations
- `screen_sleep_imbalance` – sedentary behavior proxy
- `sedentary_risk` – multi-factor inactivity flag

### 7. **Lifestyle Features**
- `lifestyle_score` – global health behavior index (0–10 scale)
- `sleep_efficiency` – sleep quality metric

---

## 📦 Installation

### From GitHub (recommended)

```bash
pip install git+https://github.com/Manda404/medrisk-features.git
```

### With Poetry

```bash
poetry add git+https://github.com/Manda404/medrisk-features.git
```

### Development Installation

```bash
git clone https://github.com/Manda404/medrisk-features.git
cd medrisk-features
poetry install
```

---

## 🚀 Quick Start

### Basic Usage

```python
import pandas as pd
from medrisk_features import FeatureEngineeringPipeline

# Load your health data
df = pd.read_csv("patient_data.csv")

# Initialize pipeline with validation
pipeline = FeatureEngineeringPipeline(
    age_group_strategy="detailed",  # "simple", "detailed", or "senior"
    validate_schema=True,
)

# Transform data
df_features = pipeline.transform(df)

# Features are now ready for ML models
print(df_features.columns.tolist())
```

### Integration with scikit-learn

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

model_pipeline = Pipeline([
    ('features', FeatureEngineeringPipeline()),
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier())
])

model_pipeline.fit(X_train, y_train)
```

### Kaggle Notebook Example

```python
# Works seamlessly in Kaggle environments
import pandas as pd
from medrisk_features import FeatureEngineeringPipeline

df = pd.read_csv('/kaggle/input/dataset/train.csv')
pipeline = FeatureEngineeringPipeline(validate_schema=True)
df_transformed = pipeline.transform(df)
```

---

## 🔐 Schema Validation

The pipeline enforces a **minimum required schema** to prevent silent failures:

### Required Columns
- `Age` – patient age in years
- `glucose_fasting` – fasting blood glucose (mg/dL)
- `bmi` – body mass index (kg/m²)

### Optional but Recommended
- `hba1c`, `insulin_fasting` – for advanced metabolic features
- `hdl_cholesterol`, `ldl_cholesterol`, `total_cholesterol` – for lipid features
- `systolic_bp`, `diastolic_bp` – for cardiovascular features
- `physical_activity_minutes`, `sleep_hours`, `screen_time_hours` – for lifestyle features

### Validation Example

```python
try:
    pipeline = FeatureEngineeringPipeline(validate_schema=True)
    df_features = pipeline.transform(df)
except SchemaValidationError as e:
    print(f"Schema Error: {e}")
    # Output: Missing required columns: ['glucose_fasting', 'bmi']
```

Disable validation for flexibility (not recommended in production):

```python
pipeline = FeatureEngineeringPipeline(validate_schema=False)
```

---

## 🧪 Testing

### Run Unit Tests

```bash
poetry run pytest -v
```

### With Coverage Report

```bash
poetry run pytest --cov=medrisk_features --cov-report=html
```

### Test Specific Modules

```bash
poetry run pytest tests/test_medical.py -v
poetry run pytest tests/test_pipeline.py::test_full_pipeline -v
```

---

## 🏗️ Project Structure

```
medrisk-features/
│
├── medrisk_features/           # Main package
│   ├── __init__.py
│   │
│   ├── pipeline/               # Orchestration layer
│   │   ├── __init__.py
│   │   └── feature_engineering_pipeline.py
│   │
│   ├── preprocessing/          # Data cleaning
│   │   ├── __init__.py
│   │   ├── categorical_cleaning.py
│   │   └── leakage.py
│   │
│   ├── features/               # Feature modules
│   │   ├── __init__.py
│   │   ├── demographics.py
│   │   ├── medical.py
│   │   ├── clinical.py
│   │   ├── metabolic.py
│   │   ├── behavioral.py
│   │   └── lifestyle.py
│   │
│   ├── validation/             # Schema validation
│   │   ├── __init__.py
│   │   └── schema.py
│   │
│   └── logging/                # Logging utilities
│       ├── __init__.py
│       └── default_logger.py
│
├── tests/                      # Test suite
│   ├── test_demographics.py
│   ├── test_medical.py
│   ├── test_pipeline.py
│   └── conftest.py
│
├── .github/workflows/          # CI/CD
│   └── ci.yml
│
├── pyproject.toml              # Dependencies & metadata
├── README.md
└── .gitignore
```

---

## 🪵 Logging

Professional logging via **Loguru** with context-aware output:

```python
from medrisk_features.logging import get_logger

logger = get_logger("custom-pipeline")
logger.info("Starting feature engineering")
logger.warning("Missing optional column: hba1c")
logger.error("Schema validation failed")
```

**Features:**
- Notebook-friendly colorized output
- Kaggle-compatible logging
- Production-ready structured logs
- Configurable log levels

---

## 🎯 Design Philosophy

### Core Principles

1. **Explainability First** – Every feature has clear clinical meaning
2. **No Silent Failures** – Explicit validation with actionable errors
3. **Separation of Concerns** – Modular architecture for maintainability
4. **Production-Minded** – Built for real-world deployment
5. **ML-Friendly** – Designed for model training, not just EDA

### What This Package **Intentionally Avoids**

- ❌ Hard coupling to specific ML frameworks
- ❌ Hidden data assumptions and transformations
- ❌ Over-engineered dependencies
- ❌ Black-box feature engineering
- ❌ Unstable numerical operations

---

## 🧠 Target Audience

- **Data Scientists** building healthcare ML models
- **ML Engineers** deploying production risk models
- **Healthcare Analytics Teams** requiring interpretable features
- **Insurance Analysts** working on underwriting models
- **Students & Researchers** developing serious ML portfolios
- **Applied AI Projects** in health, pharma, and wellness

---

## 🛣️ Roadmap

### Planned Features

- [ ] 📦 PyPI release for `pip install medrisk-features`
- [ ] 📊 MLflow experiment tracking integration
- [ ] 🔍 SHAP explainability helpers
- [ ] ⚙️ YAML-based configuration files
- [ ] 🧪 Property-based testing (Hypothesis)
- [ ] 📐 Great Expectations schema contracts
- [ ] 🌐 Multi-language support (French medical terms)
- [ ] 📈 Feature importance analysis utilities
- [ ] 🔄 Online learning compatibility

### Contributions Welcome

Open to contributions! See `CONTRIBUTING.md` for guidelines.

---

## 👤 Author

**Rostand Surel**  
📧 [rostandsurel@yahoo.com](mailto:rostandsurel@yahoo.com)  
🔗 [GitHub](https://github.com/Manda404)

---

## 📄 License

MIT License – Free to use, modify, and distribute.

See `LICENSE` file for details.

---

## 🙏 Acknowledgments

This project synthesizes best practices from:
- Clinical guidelines (ADA, WHO, ESC, JNC)
- ML engineering patterns (scikit-learn, MLOps)
- Healthcare AI research literature
- Production ML system design

---

## ⭐ Support This Project

If **medrisk-features** helps your work:
- ⭐ Star the repository
- 🐛 Report issues or request features
- 🤝 Contribute improvements
- 📢 Share with your network

Built with ❤️ for the healthcare ML community.

---

## 📚 Citation

If you use this package in research or production, please cite:

```bibtex
@software{medrisk_features,
  author = {Surel, Rostand},
  title = {medrisk-features: Clinical Feature Engineering for Healthcare ML},
  year = {2025},
  url = {https://github.com/Manda404/medrisk-features}
}
```

---

**Questions?** Open an issue or contact [rostandsurel@yahoo.com](mailto:rostandsurel@yahoo.com)