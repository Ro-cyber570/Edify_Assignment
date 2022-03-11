import pandas as pd
from .models import Purchase

# dataset from https://www.kaggle.com/aungpyaeap/supermarket-sales
# headers changed and invoice number col removed
def csv_to_db():
    df = pd.read_csv('C:\Users\G15-D560542WIN9W\Downloads\archive\diabetes.csv') # use pandas to read the csv