from bs4 import BeautifulSoup
from pathlib import Path
from parser.parser_utils import normalize_format, normalize_mode
SAMPLES_DIR = rf"{Path(__file__).resolve().parent}\samples"

class HLTVParser():
    def __init__(self, file):
        self.file = file
        self.soup = BeautifulSoup(open(rf"{SAMPLES_DIR}\{file}", encoding="utf8"), "html.parser")
        self.flexboxcolumn = self.soup.find("div", class_="flexbox-column")
        self.timeandevent = self.soup.find("div", class_="timeAndEvent")
        self.paddingpreformatted = self.soup.find("div", class_="padding preformatted-text")

    def get_date(self):
        return self.timeandevent.select_one("div.date").text.strip()
    
    def get_event(self):
        return self.timeandevent.select_one("div.event").text.strip()

    def get_teams(self):
        teams = [team.text.strip() for team in self.flexboxcolumn.select("div.results-teamname.text-ellipsis")[0:2]]
        return teams

    def get_format(self):
        return self.paddingpreformatted.text.split("\n\n")[0]
    
    def get_stage(self):
        return self.paddingpreformatted.text.split("* ")[1]

    def get_maps(self):
        maps = [div.text for div in self.flexboxcolumn.select("div.mapname")]
        return maps

    def get_scores(self):
        scores = [div.text.strip() for div in self.flexboxcolumn.select("div.results-team-score")]
        return [(scores[i], scores[i+1]) for i in range(0, len(scores), 2)]