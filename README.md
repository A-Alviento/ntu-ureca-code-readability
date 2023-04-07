# URECA-Code-Readability-New

This repository contains the necessary files to train a logistic regression model for code readability assessment and implement a feedback tool based on the trained model.

## Repository Structure

- `r/` - Contains the R files used to train the logistic regression model for the readability tool.
- `features-generator.ipynb` - A Jupyter Notebook to generate features from the code snippets in the `dataset` folder and output them to a CSV file for training in R.
- `feedback_tool.ipynb` - A Jupyter Notebook that uses the trained model from R to provide readability feedback on given code snippets.

## How it works

1. The `features-generator.ipynb` extract features from the code snippets in the `dataset` folder. This will generate a CSV file containing the features required for training the logistic regression model. The csv file already exist in the `r/` folder, named `feature_matrix_x`. `feature_matrix_5` is the most updated output and is the one used in training.
2. Train the logistic regression model using the R files in the `r/` folder, which take the generated CSV file as input. `data-to-df.R` converts the datasets into dataframes.
3. Once the model is trained, the model is extracted and used in `feedback_tool.ipynb`. This tool will provide readability feedback based on the trained model.

## Getting Started

To get started with this project, clone the repository and install the necessary dependencies (indicated by the library imports).
