from scraping_core import run_scraping
import os

os.environ["ENV"] = "lambda"  

def scraping_lambda(event=None, context=None):
    return run_scraping()
