from bs4 import BeautifulSoup

from abc import ABC, abstractmethod
import requests


class Food(ABC):
    def __init__(self, area, category):
        # 地區
        self.area = area

        # 美食類別
        self.category = category

    @abstractmethod
    def scrape(self):
        pass


# 愛食記爬蟲
class IFoodie(Food):
    def scrape(self):
        response = requests.get(
            "https://ifoodie.tw/explore/" + self.area +
            "/list/" + self.category +
            "?sortby=popular&opening=true"
        )

        soup = BeautifulSoup(response.content, "html.parser")

        # 爬取前五比餐廳卡片資料
        cards = soup.find_all('div', {'class': 'jsx-2133253768 restaurant-item track-impression-ga'}, limit=5)

        content = ""
        for card in cards:
            # 餐廳名稱
            title = card.find(
                "a", {"class": "jsx-2133253768 title-text"}).getText()

            # 餐廳評價
            stars = card.find(
                "div", {"class": "jsx-1207467136 text"}).getText()

            # 餐廳地址
            address = card.find(
                "div", {"class": "jsx-2133253768 address-row"}).getText()

            # 將取得的餐廳名稱、評價及地址連結一起，並且指派給content變數
            content += f"{title} \n{stars}顆星 \n{address} \n\n"

        return content
