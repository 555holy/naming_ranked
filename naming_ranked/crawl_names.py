"""
This file gets all the names from the specific years
"""

import os

import selenium.common
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_DIR = os.path.dirname(os.getcwd())
DATA_DIR = os.path.join(BASE_DIR, "data")


def crawl(years: list[int]) -> None:
    """
    crawl the text files for corresponding years if not already exist
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    crawling_years = []  # years without corresponding text files

    # collect years needed to be crawled
    for year in years:
        filepath = os.path.join(DATA_DIR, f"{year}.txt")
        if not os.path.exists(filepath):
            crawling_years.append(year)

    # start crawling
    if crawling_years:
        driver = webdriver.Chrome()
        for year in crawling_years:
            url = "https://www.ssa.gov/oact/babynames/decades/names" + str(year) + "s.html"
            driver.get(url)
            try:
                element_presence = EC.presence_of_element_located((By.CLASS_NAME, "t-stripe"))
                WebDriverWait(driver, 10).until(element_presence)
            except selenium.common.TimeoutException:
                print("Timeout")
                print("Exiting program...")
                driver.quit()
                exit(1)

            html = driver.page_source
            soup = BeautifulSoup(html, features="html.parser")
            table = soup.find("table", {"class": "t-stripe"})
            tbody = table.find("tbody")
            rows = tbody.find_all("tr")
            filepath = os.path.join(DATA_DIR, f"{year}.txt")
            with open(filepath, 'w') as f:
                f.write(str(year) + '\n')
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) == 5:
                        rank = cols[0].text
                        male_name = cols[1].text
                        female_name = cols[3].text
                        f.write(f"{rank}, {male_name}, {female_name}\n")

        driver.quit()
