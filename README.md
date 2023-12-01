# URECA Code Readability Tool

This repository contains the necessary files to train a logistic regression model for code readability assessment with a simple rule-based feedback tool based on the trained model.

This project is designed to assess the readability of code using machine learning techniques. It utilizes a logistic regression model trained on a dataset of code snippets. The trained model is then applied to any given code snippet to provide a readability feedback.

## Getting Started

#### Navigate Project

- `r/` - Contains the R files used to train the logistic regression model for the readability tool.
- `features-generator.ipynb` - A Jupyter Notebook to generate features from the code snippets in the dataset folder.
- `feedback_tool.ipynb` - A Jupyter Notebook that provides readability feedback on given code snippets.
- `feedback_tool.py` - A Python file version of feedback_tool.ipynb for use with streamlit deployment.
- `streamlit_deploy.py`- A Python file for deploying the feedback tool as a Streamlit web application.

#### Installations

Before getting started, you'll need to install the following Python packages. You can do this by running `pip install <package-name>` for each one:

- spacy
- pyspellchecker
- streamlit
- indexer

Next, download `en_core_web_sm` model in the Natural Language Processing library, spaCy by running:

```
python -m spacy download en_core_web_sm
```

#### Run

1. Clone the repository:

```
git clone <repository-url>
```

2. Navigate to the project directory:

```
cd URECA-Code-Readability-New
```

3. Run the Streamlit application:

```
streamlit run streamlit_deploy.py
```

4. Open the provided local URL in your web browser to interact with the application.

#### Recommended Workflow

1. The `features-generator.ipynb` notebook extracts features from the code snippets in the `dataset` folder, outputting them to a CSV file (`feature_matrix_x` in the `r/` folder) for training the logistic regression model.

2. The logistic regression model is trained using the R files in the `r/` folder, taking the generated CSV file as input.

3. The `feedback_tool.ipynb` notebook uses the trained model to provide readability feedback on given code snippets.

## References

* S. Scalabrino, M. Linares-Vásquez, R. Oliveto, and D. Poshyvanyk, “A comprehensive model for code readability,” J. Softw. Evol. Process, vol. 30, no. 6, p. e1958, 2018, doi: 10.1002/smr.1958.
