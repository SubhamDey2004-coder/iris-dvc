# Iris Classification with Git & DVC

A small Machine Learning project built to learn and demonstrate **DVC (Data Version Control)** together with **Git and GitHub**.

The machine learning problem is intentionally simple. The primary goal of this project is understanding how to version datasets, create reproducible ML pipelines, track metrics, and manage data separately from Git using DVC.

---

## 📌 Project Overview

This project performs **Iris flower classification** using a Random Forest Classifier.

The model predicts the species of an Iris flower using four features:

* Sepal length
* Sepal width
* Petal length
* Petal width

The Iris dataset contains 150 samples belonging to three classes.

The ML model itself is deliberately simple because the main purpose of this project is learning **DVC and ML pipeline management**, not building a sophisticated model.

---

## 🎯 Main Objectives

The project was created with the following learning objectives:

1. Understand the relationship between **Git and DVC**
2. Track datasets using DVC
3. Store large ML artifacts separately from Git
4. Configure a DVC remote
5. Push and pull DVC-tracked data
6. Build an ML pipeline using DVC
7. Understand dependencies between pipeline stages
8. Reproduce the pipeline using `dvc repro`
9. Understand `dvc.lock`
10. Track model evaluation metrics
11. Understand how Git and DVC work together for reproducible ML projects

---

# 🏗️ Project Architecture

The complete ML workflow is:

```text
                  Iris Dataset
                       │
                       ▼
                  prepare.py
                       │
              ┌────────┴────────┐
              ▼                 ▼
         train.csv           test.csv
              │                 │
              ▼                 │
           train.py             │
              │                 │
              ▼                 │
          model.pkl             │
              │                 │
              └────────┬────────┘
                       ▼
                  evaluate.py
                       │
                       ▼
                 metrics.json
```

DVC manages the dependency relationships between these stages.

---

# 📁 Project Structure

```text
iris-dvc/
│
├── data/
│   ├── raw/
│   │   ├── iris.csv
│   │   └── iris.csv.dvc
│   │
│   ├── train.csv
│   ├── test.csv
│   └── .gitignore
│
├── models/
│   ├── model.pkl
│   └── .gitignore
│
├── metrics/
│   └── metrics.json
│
├── src/
│   ├── create_dataset.py
│   ├── prepare.py
│   ├── train.py
│   └── evaluate.py
│
├── .dvc/
│   ├── config
│   └── .gitignore
│
├── .dvcignore
├── dvc.yaml
├── dvc.lock
├── requirements.txt
└── README.md
```

---

# 🤖 Machine Learning Workflow

## 1. Dataset Creation

`src/create_dataset.py` uses Scikit-learn's built-in Iris dataset and saves it as:

```text
data/raw/iris.csv
```

The dataset contains:

```text
150 samples
4 input features
1 target column
```

The target represents the Iris species.

---

## 2. Data Preparation

`src/prepare.py` reads:

```text
data/raw/iris.csv
```

and splits it into:

```text
data/train.csv
data/test.csv
```

The split uses:

```python
test_size=0.2
random_state=42
stratify=df["target"]
```

Therefore:

* 80% of the data is used for training
* 20% is used for testing
* The split is reproducible

---

## 3. Model Training

`src/train.py` trains a Random Forest Classifier.

The model uses:

```python
RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
```

The trained model is saved as:

```text
models/model.pkl
```

---

## 4. Model Evaluation

`src/evaluate.py` loads:

```text
data/test.csv
models/model.pkl
```

and calculates classification accuracy.

The result is saved to:

```text
metrics/metrics.json
```

Example:

```json
{
    "accuracy": 0.9
}
```

The current model achieved:

```text
Accuracy: 0.9000
```

---

# 🔄 DVC Pipeline

The complete pipeline is defined in:

```text
dvc.yaml
```

The pipeline contains three stages:

```text
prepare
   ↓
train
   ↓
evaluate
```

## Pipeline dependencies

### Prepare

```text
Inputs:
    src/prepare.py
    data/raw/iris.csv

Outputs:
    data/train.csv
    data/test.csv
```

### Train

```text
Inputs:
    src/train.py
    data/train.csv

Output:
    models/model.pkl
```

### Evaluate

```text
Inputs:
    src/evaluate.py
    data/test.csv
    models/model.pkl

Metric:
    metrics/metrics.json
```

The pipeline can be visualized using:

```bash
dvc dag
```

---

# 🗃️ Git vs DVC

One of the most important concepts demonstrated by this project is the difference between Git and DVC.

## Git

Git tracks:

```text
Source code
Configuration
dvc.yaml
dvc.lock
.dvc files
Project metadata
```

GitHub stores these Git-tracked files.

## DVC

DVC tracks:

```text
Datasets
Models
Large generated files
Pipeline outputs
```

These files are stored in a DVC remote rather than directly inside the Git repository.

Conceptually:

```text
                    GitHub
                       │
                       │ Git
                       ▼
              ┌─────────────────┐
              │ Source code     │
              │ dvc.yaml        │
              │ dvc.lock        │
              │ iris.csv.dvc    │
              └────────┬────────┘
                       │
                       │ DVC
                       ▼
                 DVC Remote
                       │
                       ▼
                Actual Dataset
```

This separation allows Git to remain lightweight while DVC manages potentially large ML artifacts.

---

# 📦 Tracking the Dataset with DVC

Initially, Git was tracking:

```text
data/raw/iris.csv
```

This was intentionally changed.

The dataset was removed from Git tracking using:

```bash
git rm --cached data/raw/iris.csv
```

The actual file remained on the computer.

Then it was added to DVC:

```bash
dvc add data/raw/iris.csv
```

DVC created:

```text
data/raw/iris.csv.dvc
```

The `.dvc` file contains metadata identifying the dataset.

For example:

```yaml
outs:
- md5: 21d441a28bce4417276097df955afc50
  size: 2928
  hash: md5
  path: iris.csv
```

The MD5 hash acts as a fingerprint for the dataset contents.

Git tracks:

```text
iris.csv.dvc
```

while DVC manages:

```text
iris.csv
```

---

# 🌐 DVC Remote

For this learning project, a **local DVC remote** was used instead of cloud storage.

The project structure was:

```text
MLOps/
│
├── iris-dvc/
│
└── dvc-storage/
```

The remote was configured using:

```bash
dvc remote add -d local_storage ../dvc-storage
```

The remote is intentionally local because the purpose of this project was learning DVC concepts quickly without introducing unnecessary cloud configuration.

In a production project, the same concept can be used with remote storage such as cloud/object storage.

---

# ⬆️ Pushing Data to the DVC Remote

After configuring the remote:

```bash
dvc push
```

was used.

This uploaded the DVC-managed dataset to the remote storage.

The actual dataset is stored by DVC using its content hash rather than simply using the original filename.

---

# ⬇️ Pulling Data

The dataset can be retrieved from the DVC remote using:

```bash
dvc pull
```

For example:

```bash
dvc pull
```

resulted in:

```text
Everything is up to date.
```

This demonstrates that the actual dataset does not need to be stored inside GitHub.

---

# 🔁 Reproducing the Pipeline

The most important DVC command in this project is:

```bash
dvc repro
```

Instead of manually running:

```bash
python src/prepare.py
python src/train.py
python src/evaluate.py
```

DVC can execute the entire pipeline:

```bash
dvc repro
```

DVC checks the dependencies of each stage and determines which stages need to be executed.

---

# ⚡ Incremental Pipeline Execution

One of the main advantages demonstrated by this project is that DVC does not blindly rerun every stage.

For example, initially:

```text
prepare → train → evaluate
```

all stages were executed.

Running:

```bash
dvc repro
```

again without any changes resulted in:

```text
prepare   → skipped
train     → skipped
evaluate  → skipped
```

because nothing had changed.

---

## Dependency Tracking Example

The training code was modified:

```text
n_estimators=100
```

was changed to:

```text
n_estimators=200
```

Running:

```bash
dvc repro
```

resulted in:

```text
prepare   → skipped
train     → executed
evaluate  → executed
```

Why?

Because:

```text
train.py changed
      ↓
train stage becomes outdated
      ↓
model.pkl changes
      ↓
evaluate depends on model.pkl
      ↓
evaluate must run again
```

However:

```text
prepare
```

did not depend on the changed training code, so it did not need to run again.

This demonstrates the dependency-aware nature of DVC pipelines.

---

# 🔒 dvc.yaml vs dvc.lock

The pipeline definition is stored in:

```text
dvc.yaml
```

It describes:

> How should the pipeline be executed?

The exact state of the pipeline is recorded in:

```text
dvc.lock
```

It records the versions/hashes of dependencies and outputs used during pipeline execution.

A useful mental model is:

```text
dvc.yaml
    ↓
"What should happen?"

dvc.lock
    ↓
"What exact state produced the result?"
```

Both files should be committed to Git.

---

# 📊 Metrics

The evaluation stage produces:

```text
metrics/metrics.json
```

The metric is registered in the DVC pipeline using the `-M` option.

Metrics can be displayed using:

```bash
dvc metrics show
```

Example:

```text
Path                  accuracy
metrics\metrics.json  0.9
```

This makes it possible to track model performance alongside the pipeline.

---

# 🔀 Git + DVC Workflow

The project demonstrates the following overall workflow:

```text
                     GitHub
                        ▲
                        │ git push
                        │
                ┌───────┴────────┐
                │                 │
             Git repo         DVC remote
                │                 │
                │                 │
        Code + metadata        Data
        dvc.yaml               Models
        dvc.lock
        *.dvc
                │                 │
                └───────┬─────────┘
                        │
                        ▼
                  Reproducible
                   ML project
```

A typical workflow becomes:

```bash
git pull
dvc pull

# Modify code/data/parameters

dvc repro

dvc push

git add .
git commit -m "Update pipeline"
git push
```

---

# 🛠️ Important Commands Learned

## DVC Initialization

```bash
dvc init
```

Initialize DVC inside a Git repository.

---

## Track Data

```bash
dvc add <file>
```

Start tracking a dataset or other large artifact with DVC.

---

## Check DVC State

```bash
dvc status
```

Check whether data and pipeline stages are up to date.

---

## Configure Remote

```bash
dvc remote add -d <name> <path>
```

Configure the default DVC remote.

---

## Upload Data

```bash
dvc push
```

Upload DVC-tracked data to the remote.

---

## Download Data

```bash
dvc pull
```

Download DVC-tracked data from the remote.

---

## Create Pipeline Stage

```bash
dvc stage add
```

Create a stage in the DVC pipeline.

---

## Visualize Pipeline

```bash
dvc dag
```

Display the dependency graph.

---

## Reproduce Pipeline

```bash
dvc repro
```

Run only the pipeline stages that need to be reproduced.

---

## Show Metrics

```bash
dvc metrics show
```

Display tracked metrics.

---

# 🧰 Technologies Used

* Python
* Pandas
* Scikit-learn
* Git
* GitHub
* DVC
* YAML

---

# ⚙️ Setup

## 1. Clone the repository

```bash
git clone <repository-url>
cd iris-dvc
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Pull DVC data

```bash
dvc pull
```

> Note: This learning project uses a local DVC remote, so the local remote path must exist when reproducing the original setup. For sharing the project across different machines, the DVC remote should be replaced with a shared remote such as cloud/object storage.

## 5. Reproduce the pipeline

```bash
dvc repro
```

## 6. View metrics

```bash
dvc metrics show
```

---

# 🧪 Running the Pipeline Manually

Although DVC manages the pipeline, the individual stages can also be executed manually:

```bash
python src/prepare.py
```

```bash
python src/train.py
```

```bash
python src/evaluate.py
```

However, the recommended approach for this project is:

```bash
dvc repro
```

because DVC understands the dependencies between the stages.

---

# 📈 Result

The current model achieved:

```text
Accuracy: 0.9000
```

or:

```text
90% accuracy
```

The model performance is not the primary focus of this project. The main objective was demonstrating reproducible data and pipeline management using DVC.

---

# 🧠 Key Lessons

The most important concepts learned from this project are:

### 1. Git and DVC are complementary

DVC does not replace Git.

```text
Git → Code + project metadata
DVC → Data + large ML artifacts
```

### 2. `.dvc` files are lightweight metadata

Git can safely track the `.dvc` file while DVC manages the actual dataset.

### 3. DVC remotes store the actual data

The GitHub repository does not need to contain the dataset itself.

### 4. `dvc.yaml` defines the pipeline

It describes stages, dependencies, and outputs.

### 5. `dvc.lock` records the exact pipeline state

This helps make experiments reproducible.

### 6. `dvc repro` understands dependencies

Only stages affected by changes need to be rerun.

### 7. Metrics can be versioned alongside the pipeline

DVC can track model metrics such as accuracy and compare results between pipeline versions.

---

# 🚀 Possible Future Improvements

This project intentionally remains small. Possible next steps for a larger ML project would include:

* Using a cloud DVC remote
* Adding `params.yaml`
* Running DVC experiments
* Comparing multiple model configurations
* Tracking multiple datasets
* Adding more evaluation metrics
* Using a larger real-world dataset
* Integrating DVC into a CI/CD workflow
* Adding automated model validation

These are intentionally outside the scope of this introductory project.

---

# 📜 License

This project is intended primarily as a learning and demonstration project for Git, GitHub, DVC, and reproducible Machine Learning workflows.
