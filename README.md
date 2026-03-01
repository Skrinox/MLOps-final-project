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








