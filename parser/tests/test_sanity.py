from parser.parser_script import HLTVParser
from parser.parser_fetch_data import fetch_data, export_json
from parser.parser_utils import fetch_team_data, fetch_map_data, normalize_date, normalize_format
import pytest
from pathlib import Path
import os
import json

SAMPLES_DIR = rf"{Path(__file__).resolve().parent.parent}\samples"
html_files = [
    f for f in os.listdir(SAMPLES_DIR) if f.endswith(".html")
]

@pytest.fixture
def parser(request):
    return HLTVParser(request.param)

@pytest.mark.parametrize("parser", html_files, indirect=True)
def test_data_sanity(parser):
    event = parser.get_event()
    date = parser.get_date()
    teams = parser.get_teams()
    format_ = parser.get_format()
    stage = parser.get_stage()
    maps = parser.get_maps()
    scores = parser.get_scores()
    
    assert parser

    assert isinstance(date, str)
    assert date
    
    assert isinstance(event, str)
    assert event
    
    assert isinstance(teams, list)
    assert teams
    
    assert isinstance(format_, str)  
    assert format_
    
    assert isinstance(stage, str)
    assert stage
    
    assert isinstance(maps, list)
    assert maps

    assert isinstance(scores, list)
    assert scores

@pytest.mark.parametrize("file", html_files)
def test_fetch_data_sanity(file):
    match_data = fetch_data(file)

    assert isinstance(match_data, dict)
    assert match_data

@pytest.mark.parametrize("file", html_files)
def test_export_json_sanity(file):
    match_data = fetch_data(file)
    path = export_json(file, match_data)

    assert os.path.exists(path)

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    assert data == match_data