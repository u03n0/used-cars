![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)

# Used Cars
A look at used car sales.

## Goal
The goal is to predict the sales price of a used car, based on features (make, model, year, hp, fuel, gear type, etc.).
   
## Downloading and Using (Linux and Mac)
### Option 1: Download (Clone) Repo locally 
Using the `terminal` run the following commands in a `directory` you want the repo to be in.
1. clone repo: `git clone git@github.com:u03n0/used-cars.git`
2. `cd` into root of repo
3. build a virtual environment via `venv` using the command: `python3 -m venv venv`
4. activate virtual environment with: `source venv/bin/activate`
5. load requirements with: `pip install -r requirements.txt`
### Option 2: Use Pre-Built Docker Image
- WIP
### Option 3: Build Docker Image from Repo
-  Follow steps 1-2 from above.
-  Ensure docker is running on your system.
-  Run in the terminal at the root of the repo: `docker build -t used-cars .` (might need `sudo` at the beginning)
-  Run: `docker run -p 8501:8501 used-cars` (might need `sudo` at the beginning)
## Running models
- No data or model is present in the repo, you need to run a script to download and clean the data.
- Run: `python3 scripts/download_data.py` to get clean data.
- Once this is complete, you will now have a folder called `data/` which has both a raw and cleaned dataset.
- Now you can choose which model to run (See below for which models are available)
- To run the model(s) use this command in the terminal: `python3 src/<python_file.py>` (replace `<python_file.py>` with whichever `py` is in `src`.
- You will now have a folder called `models/` and the score will be printed in the terminal.

## Using the Streamlit app
### In local repo
- Once you've ran a model with the steps provided above, you can use the Streamlit app
- run `streamlit run frontend/app.py` from the root of the repo.
- Select `Sell Vehicle` to simulate you selling your car and you will get a predicted price for it.
- Select `Buy Vehicle for Inventory` to simulate you as a sales agent who is deciding on what price to offer for a used car.
- - You can toggle your commission rate and expected profit margin.
### In Docker container
- It should automatically direct you to the streamlit app
## Available Models
- `LinearRegression` via sklean as `src/lr_sklearn_pipeline.py`
- `NeuralNetwork` via PyTorch (WIP)
  

