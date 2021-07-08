import requests
from bs4 import BeautifulSoup
from sqlalchemy import Integer, String, Text, Column
from sqlalchemy.ext.declarative import declarative_base
from parse import Parse
from datahouse import Datahouse

base = declarative_base()


class Position(base):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    tags = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    responsibilities = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)


def get_offer_hrefs(url):
    """extract links for available positions"""
    dat = requests.get(url)
    soup = BeautifulSoup(dat.text, "html.parser")
    offer_wrappers = soup.find_all(name="a", attrs={"class": "offer-wrapper"})
    return [i.get("href") for i in offer_wrappers]


def main():
    base_url = 'https://www.gog.com'
    print('The program will go through gog.com/work job offers, extract them and store in a DB')
    data_collection = Datahouse(base, "sqlite:///database.db")
    inp = input("Press 'y' if you want to drop the current database, otherwise press any other button")
    if inp == 'y':
        data_collection.drop()
        print('The DB is empty')
    data_collection.create()
    hrefs = get_offer_hrefs(base_url+'/work')
    for h in hrefs:
        offer_data = Parse(base_url+h)
        data_collection.get_or_create(Position, **offer_data.build_job_dict())
    print('Currently the following positions are available:')
    cur_pos = data_collection.get_content(Position)
    for pos in cur_pos:
        print(f"id={pos[0]}, title={pos[1]}, department={pos[2]}")


if __name__ == "__main__":
    main()
