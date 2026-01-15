from datetime import datetime
import re

def fetch_team_data(teams):
     return [{
          "team1": teams[0],
          "team2": teams[1]
          }
        ]

def convert_score(value):
    try:
        return int(value)
    except:
        return None

def fetch_map_data(maps, scores):
            return [{
                "map": map_name,
                "team1_score": convert_score(team1),
                "team2_score": convert_score(team2)
                }
                for (map_name, (team1, team2)) in zip(maps, scores)
            ]

def normalize_date(date):
    # remove sufixos: st, nd, rd, th
    clean_date = re.sub(r'(st|nd|rd|th)', '', date)

    # remove o "of"
    clean_date = clean_date.replace(' of ', ' ')

    # converte para datetime
    dt = datetime.strptime(clean_date, "%d %B %Y")

    return dt.strftime("%Y-%m-%d")

def normalize_format(format):
    match = re.search(r'Best of (\d)', str(format))

    if not match:
        raise ValueError(f"Formato desconhecido: {str(format)}")
    
    return f"bo{match.group(1)}"

def normalize_mode(format):
    match = re.search(r'\(([^)]+)\)', str(format))

    if not match:
        raise ValueError(f"Formato desconhecido: {str(format)}")
    
    return match.group(1)