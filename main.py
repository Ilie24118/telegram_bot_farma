import requests as requests  # Requests for making network connections.
from bs4 import BeautifulSoup  # For extracting data from HTML and XML docs.
import re
from geopy.geocoders import Nominatim
import time
import math
import csv
from operator import itemgetter
import telegramBot
import multiprocessing
from multiprocessing import Pool
from difflib import Differ


def data(web_url):
    fetched_page = requests.get(web_url)

    beautifulsoup = BeautifulSoup(fetched_page.text, "html.parser")

    rows = []
    for info in beautifulsoup.find_all("span", "link link--underline"):
        farm = info.string[38:]
        if farm.find("Chisinau") != -1 and farm[0] == "C":
            rows.append([re.sub("\(.*?\)", "", farm.rstrip()).split("nr", 1)[0]])

    return rows


app = Nominatim(user_agent="test")


def get_location_by_address(address):
    """This function returns a location as raw from an address
    will repeat until success"""
    time.sleep(1)
    try:
        return app.geocode(address).raw
    except:
        return 0


def distance(address):
    # Location
    lat1 = 0 #  <---------  Latitude --------|
    long1 = 0 # <---------  Longitude -------|

    r = 6371  # radius of Earth (KM)
    p = 0.017453292519943295  # Pi/180

    location = get_location_by_address(address)
    if location != 0:
        lat2 = float(location["lat"])
        long2 = float(location["lon"])
        # print(f"{lat2}, {long2}")
        a = (
            0.5
            - math.cos((lat2 - lat1) * p) / 2
            + math.cos(lat1 * p) * (1 - math.cos((long2 - long1) * p)) / 2
        )
        d = 2 * r * math.asin(math.sqrt(a))
        return round(d, 2)
    else:
        pass


def write_csv(file, web_url):
    dataList = []

    for i in data(web_url):
        i.append(distance(*i))
        dataList.append(i)

    for x in dataList:
        if x[1] == None:
            x[1] = 999

    with open(file, "w") as f:
        write = csv.writer(f)
        write.writerows(sorted(dataList, key=itemgetter(1), reverse=True))


def diff(file1, file2):
    with open(file1) as file_1, open(file2) as file_2:
        differ = Differ()
        for line in differ.compare(file_1.readlines(), file_2.readlines()):
            if line.find("+") != -1:
                print(line)
                telegramBot.asyncio.run(telegramBot.send(str(telegramBot.usr_id), line))


def main():
    while True:
        print("START")
        old_file = "old_info.csv"
        file = "info.csv"

        #             <-----------------  WEB URL  ------------------->
        web_url = (
            "https://ff.md/products/roaccutane-10mg-caps?_pos=1&_sid=7d8282a68&_ss=r"
        )

        diff(old_file, file)

        clear_file = open(old_file, "w")
        clear_file.close()
        with open(file, "r") as firstfile, open(old_file, "a") as secondfile:
            for line in firstfile:
                secondfile.write(line)

        write_csv(file, web_url)


if __name__ == "__main__":
    p1 = multiprocessing.Process(target=main)
    p2 = multiprocessing.Process(target=telegramBot.application.run_polling)

    p1.start()
    p2.start()
