<h1 align="center">MLOps Final Project</h1>
<h3 align="center">Predicting Toyota stock prices</h3>
<p align="center">
    <img src="https://img.shields.io/badge/Virgile-Martel-orange?style=flat-square" alt="Virgile Martel"/>
    <img src="https://img.shields.io/badge/Enzo-Greiner-blue?style=flat-square" alt="Enzo Greiner"/>
    <img src="https://img.shields.io/badge/Cedric-Hombourger-green?style=flat-square" alt="Cedric Hombourger"/>
</p>

---


```Markdown
# Deliverable

1. Github repository
2. Public production URL
3. README containing:
    - architecture diagram
    - CI/CD explanation
    - model promotion explanation
    - reproducibility instructions

4. Our in-class presentation 
```

# Dataset

For this project we will be using the Toyota Stock Prices: [1980-2026 Historical Data dataset](https://www.kaggle.com/datasets/omarshahrukh/toyota-stock-prices-1980-2026-historical-data?resource=download) from Kaggle. This dataset contains historical stock price data for Toyota from 1980 to 2026, including open, high, low, close prices, and trading volume.

With this dataset we aims to predict the closing price of Toyota stock based on the features open, high, low, `volume` using a machine learning model. We will train a Random Forest Regressor and evaluate its performance using Mean Squared Error (MSE) and Mean Absolute Error (MAE) metrics.

# Architecture Diagram

# CI/CD Explanation

## Pull request to `dev` branch pipeline

When a pull request is opened targeting the `dev` branch, a GitHub Actions workflow (`pr_to_dev.yml`) is automatically triggered. This pipeline ensures code quality and integration before any merge is allowed.

### Pipeline Steps

1. **Checkout code** : retrieves the latest code from the repository.
2. **Set up Python 3.10** : installs the required Python version.
3. **Install dependencies** : installs all backend dependencies from `backend/requirements.txt`.
4. **Run unit tests** : executes unit tests located in `tests/test_unit.py`
5. **Run integration tests** : executes integration tests in `tests/test_integration.py`
6. **Run End-to-End Tests** : executes end-to-end tests in `tests/test_e2e.py`
7. **Build backend docker image** : builds the backend Docker image from `./backend`
8. **Build frontend docker image** : builds the frontend Docker image from `./frontend`

> All steps must pass for the pull request to be eligible for merging into `dev`.

# Model Promotion

During training we log the folling information to MLflow:
- Metrics: MSE and MAE
- Parameters: model type (RandomForestRegressor), hyperparameters (n_estimators, max_depth)
- Versions: git commit hash and DVC version of the dataset

# Reproducibility Instructions

Setup DVC (with pipx):
- Install pipx: `python3 -m pip install --user pipx`
- Install DVC: `pipx install dvc`
- Initialize DVC in the project: `dvc init` in the root directory of the project
This will create a .dvc and .dvcignore file in the project.
- Add the dataset to DVC: `dvc add data/toyota_stock_prices.csv`
This will create a .dvc file for the dataset and add it to the DVC tracking.
- we can commit the files to git.

To **store our data remotly** we use **Dagshub**. After creating a new repository on DagsHub (connected to our Github repo) we add the DVC remote and setup our credentials:
```Bash
dvc remote add origin https://dagshub.com/Skrinox/MLOps-final-project.dvc

dvc remote modify origin --local auth basic
dvc remote modify origin --local user <dagshub_username>
dvc remote modify origin --local password <dagshub_token>
```








