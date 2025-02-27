![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
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
A look at used and new car sales.

## Goal
The goal is to:
1. Show a predicted used car price for a particular vehicle based on make, model, year, mileage, etc.
2. Give advice to a used-car salesman, if he should buy a particular car to add to his stock (based on potential resale value)
3. 
## How to Use
1. clone repo
2. `cd` into root of repo
3. build a virtual environment via `venv` using the command: `python3 -m venv venv`
4. activate virtual environment with: `source venv/bin/activate`
5. load requirements with: `pip install -r requirements.txt`
### Using the Streamlit app
- run `streamlit run frontend/app.py` from the root of the repo
### Running models and getting performance in the Terminal
- run `python3 src/main.py`
### Using Docker
-  Follow steps 1-2
-  Run in the terminal at the root of the repo: `docker build -t used-cars .` (might need `sudo` at the beginning)
-  Run: `docker run -p 8501:8501 used-cars` (might need `sudo` at the beginning)
