import os

os.environ["ENV"] = "local"
os.environ["DYNAMO_TABLE_NAME"] = "scraping_data"

from scraping_core import run_scraping



if __name__ == "__main__":
    result = run_scraping()
    print(result)
