# Iris Classification with Git + DVC

A small reproducible ML project built to learn **Data Version Control (DVC)** alongside Git and GitHub.

The model is intentionally simple. The engineering focus is on dataset versioning, pipeline dependencies, reproducibility, and metric tracking.

## What this project demonstrates

- Versioning a dataset with DVC instead of Git
- Separating source code and ML metadata from data artifacts
- Defining an ML pipeline with `dvc.yaml`
- Reproducing the pipeline with `dvc repro`
- Tracking exact dependency/output state with `dvc.lock`
- Tracking evaluation metrics with DVC
- Understanding the Git + DVC workflow

## ML workflow

~~~text
Iris dataset
    ↓
prepare.py
    ↓
train.csv / test.csv
    ↓
train.py
    ↓
Random Forest model
    ↓
evaluate.py
    ↓
metrics/metrics.json
~~~

### Dataset

The project uses Scikit-learn's built-in Iris dataset:

- 150 samples
- 4 input features
- 3 target classes
- 80/20 stratified train/test split
- `random_state=42`

### Model

A Random Forest classifier is trained with:

~~~python
RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
~~~

The current recorded test accuracy is **0.90**.

## DVC pipeline

The pipeline contains three stages:

| Stage | Dependencies | Output |
|---|---|---|
| `prepare` | raw dataset, `prepare.py` | train/test CSVs |
| `train` | train CSV, `train.py` | model artifact |
| `evaluate` | test CSV, model, `evaluate.py` | accuracy metric |

Run the pipeline with:

~~~bash
dvc repro
~~~

View the dependency graph:

~~~bash
dvc dag
~~~

View metrics:

~~~bash
dvc metrics show
~~~

DVC only reruns stages affected by changed dependencies. For example, changing `train.py` invalidates the training stage and downstream evaluation, while leaving the preparation stage unchanged.

## Git vs DVC

Git tracks the project code and DVC metadata:

~~~text
src/
dvc.yaml
dvc.lock
data/raw/iris.csv.dvc
~~~

DVC manages the actual dataset and generated model artifacts.

The raw dataset is therefore represented in Git by:

~~~text
data/raw/iris.csv.dvc
~~~

while the actual `iris.csv` is excluded through `data/raw/.gitignore`.

## Project structure

~~~text
iris-dvc/
├── .dvc/
│   └── config
├── data/
│   └── raw/
│       ├── .gitignore
│       └── iris.csv.dvc
├── metrics/
│   └── metrics.json
├── models/
│   └── .gitignore
├── src/
│   ├── create_dataset.py
│   ├── prepare.py
│   ├── train.py
│   └── evaluate.py
├── dvc.yaml
├── dvc.lock
├── requirements.txt
└── README.md
~~~

Generated files such as `data/train.csv`, `data/test.csv`, and `models/model.pkl` are intentionally not committed directly.

## Setup

### 1. Create an environment

~~~bash
python -m venv .venv
~~~

Windows PowerShell:

~~~powershell
.\.venv\Scripts\Activate.ps1
~~~

### 2. Install dependencies

~~~bash
pip install -r requirements.txt
~~~

### 3. Obtain the DVC-tracked dataset

The repository contains the DVC metadata for the raw dataset. A shared DVC remote should be configured before running `dvc pull` on a fresh machine.

For local learning, configure a remote outside the repository:

~~~bash
dvc remote add -d local_storage ../dvc-storage
~~~

Then:

~~~bash
dvc pull
~~~

### 4. Reproduce the pipeline

~~~bash
dvc repro
~~~

### 5. Check the result

~~~bash
dvc metrics show
~~~

Expected recorded accuracy:

~~~text
0.9
~~~

## Manual execution

The individual stages can also be run directly:

~~~bash
python src/prepare.py
python src/train.py
python src/evaluate.py
~~~

For normal reproducible execution, prefer:

~~~bash
dvc repro
~~~

## Typical Git + DVC workflow

~~~bash
git pull
dvc pull

# Modify code or data
dvc repro

# Upload DVC-tracked artifacts when a shared remote is configured
dvc push

git add .
git commit -m "Update ML pipeline"
git push
~~~

## Key takeaway

This project is primarily an **MLOps/DVC demonstration**, not a model-performance project. The useful engineering lesson is how Git, DVC, pipeline dependencies, reproducibility, and metrics work together in an ML workflow.

## Author

**Subham Dey**
