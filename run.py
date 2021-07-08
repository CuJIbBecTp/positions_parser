import requests
from bs4 import BeautifulSoup
import sqlalchemy as sqla
from sqlalchemy import Integer, String, Text, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_URL = 'https://www.gog.com'
page = requests.get(BASE_URL+'/work')


def get_offer_hrefs(url):
    dat = requests.get(url)
    soup = BeautifulSoup(dat.text, "html.parser")
    offer_wrappers = soup.find_all("a", attrs={"class": "offer-wrapper"})
    return [i.get("href") for i in offer_wrappers]


hrefs = get_offer_hrefs(BASE_URL+'/work')

results = []
for h in hrefs:
    result = {}
    data = requests.get(BASE_URL + h)
    psoup = BeautifulSoup(data.text, "html.parser")
    title = psoup.find(name="h1", attrs={"class": "job-offer-title"}).text.strip()
    result['title'] = title
    print(title)
    department = psoup.find(name="div", attrs={"class": "job-offer-department"}).text.strip()
    result['department'] = department
    tags_data = psoup.find(name="span", attrs={"class": "job-offer-tags"}).find_all("a")
    tags = ', '.join([i.text.strip() for i in tags_data])
    result['tags'] = tags
    job_description = psoup.find(name="div", attrs={"class": "job-offer-description"}).find("p").text
    result['description'] = job_description
    bullets = psoup.find_all(name="div", attrs={"class": "section-bullets"})
    bullets = [i.text.strip() for i in bullets]
    result['responsibilities'] = bullets[0]
    result['requirements'] = bullets[1]
    results.append(result)

engine = sqla.create_engine("sqlite:///database.db")
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


Session = sessionmaker(bind=engine)
session = Session()
base.metadata.create_all(engine)
# base.metadata.drop_all(engine)

connection = engine.connect()
metadata = sqla.MetaData()


def get_or_create(model, **kwargs):
    """avoid duplicates in db"""
    instance = get_instance(**kwargs)
    if instance is None:
        create_instance(model, **kwargs)
    else:
        return instance


def create_instance(model, **kwargs):
    """create instance and add it to db"""
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return True


def get_instance(**kwargs):
    """return first instance found"""
    query = sqla.text(f"SELECT id FROM positions WHERE title='{kwargs['title']}' AND department='{kwargs['department']}'")
    r_proxy = connection.execute(query)
    r_set = r_proxy.fetchall()
    if r_set:
        return r_set
    else:
        return


for i in results:
    print(get_or_create(Position, **i))


sql_query = sqla.text("SELECT id,title, department FROM positions")
result_proxy = connection.execute(sql_query)
result_set = result_proxy.fetchall()
print(result_set[:])
