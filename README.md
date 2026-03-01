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

# Architecture Diagram

# CI/CD Explanation

# Model Promotion

# Reproducibility Instructions

Setup DVC (with pipx):
- Install pipx: `python3 -m pip install --user pipx`
- Install DVC: `pipx install dvc`
- Initialize DVC in the project: `dvc init` in the root directory of the project
This will create a .dvc and .dvcignore file in the project.
- Add the dataset to DVC: `dvc add data/toyota_stock_prices.csv`
This will create a .dvc file for the dataset and add it to the DVC tracking.
- we can commit the files to git.




