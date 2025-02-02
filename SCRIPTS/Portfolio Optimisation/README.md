# Sigma_Risk

## Description

This repository contains several scripts for portfolio optimization and risk management. The main models used are the Hierarchical Clustering (HC), Efficient-Frontier (EF) and the Black-Litterman (BL) models. The scripts are written in Python and use several libraries such as Pandas, Numpy, Scipy, and Matplotlib.

## Scripts

### Tools

- `returns_histogram.py`: Creates a histogram for the arithmetic and logarithmic return distributions of a chosen stock.
- `returns_vs_market.py`: Creates a visualization of the beta of a chosen stock compared to that of a chosen benchmark.
- `Portfolio-matrices.py`: This script creates three different matrices illustrating the interaction between the stocks in the portfolio. The main purpose of this script is to circumvent the usage of the mean-variance optimization scripts to optimize workflow.
- `price_information.py`: Adds to each corrected ticker from All_Sectors their respective informations needed for the Black-Litterman and other models.
- `portfolio_matrices`: Calculates and visualises different matrixes, showcasing the inner workings of the models in the form of heatmaps.

### Portfolio

- `HC_portfolio.py`: Creates an optimal portfolio allocation based on the Hierarchical Risk Partiy model, saves them as a csv and makes a bar chart of it. Also creates an excel sheet comparing the effects of the risk measures
- `BL_portfolio.py`: This model incorporates investor views into the returns estimates, then uses the Efficient Frontier Covariance Matrix method to create the final portfolio allocation.
- `EF_portfolio.py`: Contains the model for traditional Efficient Frontier based optimization. The risk and return models, and the objectives can be modified at will, VERY customisable. Also creates an excel sheet comparing the effects of the risk measures

## Usage

The operation of the scripts can usually be altered using the inputs listed in the beginning of each script.
