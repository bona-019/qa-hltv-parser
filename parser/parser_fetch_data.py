from parser.parser_script import HLTVParser
from parser.parser_utils import fetch_map_data, normalize_date, normalize_format, fetch_team_data, normalize_mode
import sys
import json
from pathlib import Path
OUTPUT_DIR = rf"{Path(__file__).resolve().parent}\output"

def fetch_data(file):
    parser = HLTVParser(file)
    event = parser.get_event()
    date = normalize_date(parser.get_date())
    teams = fetch_team_data(parser.get_teams())
    format = normalize_format(parser.get_format())
    mode = normalize_mode(parser.get_format())
    stage = parser.get_stage()
    maps = parser.get_maps()
    scores = parser.get_scores()
    fetched_scores = fetch_map_data(maps, scores)

    match_data = {
        "event": event,
        "date": date,
        "teams": teams,
        "format": format,
        "mode": mode,
        "stage": stage,
        "score": fetched_scores,
    }

    return match_data

def export_json(file, match_data):
    with open(rf"{OUTPUT_DIR}\{file}.json", "w", encoding="utf-8") as f:
        json.dump(match_data, f, ensure_ascii=False, indent=4)
        print(f"Arquivo criado: {file}.json")
    
    return rf"{OUTPUT_DIR}\{file}.json"
     
if __name__ == "__main__":
    try:    
        export_json(sys.argv[1], fetch_data(sys.argv[1]))
    except Exception as e:
        print(f"Erro ao carregar arquivo HTML: {type(e).__name__}")