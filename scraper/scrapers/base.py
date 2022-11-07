import math
from abc import ABC, abstractmethod
from decimal import DivisionByZero
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from tqdm import tqdm

from scraper.models.car import Car, CarLink


class BaseScraper(ABC):
    __items_per_page__: int = 0
    __domain__: str = ""

    @abstractmethod
    def _retrieve_items_list(self, pages_count: int, keyword: str) -> List[CarLink]:
        pass

    def _get_page_content(self, query: str) -> Optional[BeautifulSoup]:
        resp = requests.get(f"{self.__domain__}/{query}")
        if resp.status_code == 200:
            return BeautifulSoup(resp.content)
        raise Exception("Cannot reach content!")

    @abstractmethod
    def _retrieve_car_info(self, link: CarLink) -> Optional[Car]:
        pass

    def scrape(self, cars_count: int, keyword: str) -> List[Car]:
        try:
            pages_count = math.ceil(cars_count / self.__items_per_page__)
        except ZeroDivisionError:
            raise AttributeError("Cars per page is set to 0!")
        car_links = self._retrieve_items_list(pages_count, keyword)
        scraped_cars: List[Optional[Car]] = []
        for car_link in tqdm(car_links):
            scraped_car = self._retrieve_recipe_info(car_link)
            if scraped_car:
                scraped_cars.append(scraped_car)
        return scraped_cars