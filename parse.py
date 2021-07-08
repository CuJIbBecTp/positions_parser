import requests
from bs4 import BeautifulSoup


class Parse:
    def __init__(self, link):
        data = requests.get(link)
        self.psoup = BeautifulSoup(data.text, "html.parser")

    def get_job_title(self):
        return self.psoup.find(name="h1", attrs={"class": "job-offer-title"}).text.strip()

    def get_job_department(self):
        return self.psoup.find(name="div", attrs={"class": "job-offer-department"}).text.strip()

    def get_job_tags(self):
        tags_data = self.psoup.find(name="span", attrs={"class": "job-offer-tags"}).find_all("a")
        return ', '.join([i.text.strip() for i in tags_data])

    def get_job_description(self):
        return self.psoup.find(name="div", attrs={"class": "job-offer-description"}).find("p").text.strip()

    def get_bullets(self):
        bullets = self.psoup.find_all(name="div", attrs={"class": "section-bullets"})
        return [i.text.strip() for i in bullets]

    def get_job_responsibilities(self):
        return self.get_bullets()[0]

    def get_job_requirements(self):
        return self.get_bullets()[1]

    def build_job_dict(self):
        result = {}
        result['title'] = self.get_job_title()
        result['department'] = self.get_job_department()
        result['tags'] = self.get_job_tags()
        result['description'] = self.get_job_description()
        result['responsibilities'] = self.get_job_responsibilities()
        result['requirements'] = self.get_job_requirements()
        return result
