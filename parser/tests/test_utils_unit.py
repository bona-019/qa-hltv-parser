import pytest
from parser.parser_utils import (
    fetch_team_data,
    convert_score,
    fetch_map_data,
    normalize_date,
    normalize_format,
    normalize_mode
)

class TestConvertScore():
    def test_convert_score_valid(self):
        assert convert_score("13") == 13
        assert convert_score("0") == 0
        assert convert_score(2) == 2

    def test_convert_score_invalid(self):
        assert convert_score("RandomString") == None
        assert convert_score("") == None
        assert convert_score("-") == None

    def test_convert_score_special_char(self):
        assert convert_score("    13    ") == 13

    def test_convert_score_negative(self):
        assert convert_score("-5") == -5

class TestFetchTeamData():
    def test_fetch_team_data(self):
        teams = ["FURIA", "Natus Vincere"]
        assert fetch_team_data(teams) == [{"team1": "FURIA", "team2": "Natus Vincere"}]

    def test_fetch_team_data_structure(self):
        teams = ["B8", "Falcons"]
        result = fetch_team_data(teams)

        assert isinstance(result, list)
        assert len(result) == 1

        assert "team1" in result[0].keys()
        assert "team2" in result[0].keys()

class TestNormalizeDate():
    def test_normalize_date_st(self):
        assert normalize_date("1st of January 2025") == "2025-01-01"
        assert normalize_date("21st of March 2025") == "2025-03-21"
    
    def test_normalize_date_nd(self):
        assert normalize_date("2nd of February 2025") == "2025-02-02"
        assert normalize_date("22nd of April 2025") == "2025-04-22"
    
    def test_normalize_date_rd(self):
        assert normalize_date("3rd of March 2025") == "2025-03-03"
        assert normalize_date("23rd of May 2025") == "2025-05-23"
    
    def test_normalize_date_th(self):
        assert normalize_date("4th of April 2025") == "2025-04-04"
        assert normalize_date("15th of June 2025") == "2025-06-15"

class TestNormalizeFormat():
    def test_normalize_format_valid(self):
        assert normalize_format("Best of 1") == "bo1"
        assert normalize_format("Best of 3") == "bo3"
        assert normalize_format("Best of 5") == "bo5"

    def test_normalize_format_invalid(self):
        with pytest.raises(ValueError):
            normalize_format("Bestof 3")
    
        with pytest.raises(ValueError):
            normalize_format("bo5")
    
        with pytest.raises(ValueError):
            normalize_format("BO3")

class TestNormalizeMode():
    def test_normalize_mode_valid(self):
        assert normalize_mode("Best of 1 (LAN)") == "LAN"
        assert normalize_mode("Best of 3 (LAN)") == "LAN"
        assert normalize_mode("Best of 5 (LAN)") == "LAN"

        assert normalize_mode("Best of 1 (Online)") == "Online"
        assert normalize_mode("Best of 3 (Online)") == "Online"
        assert normalize_mode("Best of 5 (Online)") == "Online"

    def test_normalize_mode_invalid(self):
        with pytest.raises(ValueError):
            normalize_mode("BO1")

        with pytest.raises(ValueError):
            normalize_mode("Best of 3")

        with pytest.raises(ValueError):
            normalize_mode("best of 5 - LAN")

class TestFetchMapData():
    def test_fetch_map_data_valid_bo1(self):
        bo1 = [
            ["Inferno"],[[13,11]]
        ]

        map_data = fetch_map_data(bo1[0], bo1[1])

        assert map_data
        assert len(map_data) == 1

        for score in map_data:
            assert "map" in score.keys()
            assert "team1_score" in score.keys()
            assert "team2_score" in score.keys()
        
        assert [score for score in bo1[1][0] if type(score) == int]

    def test_fetch_map_data_valid_bo3_2maps(self):
        bo3_2maps = [
            ["Dust2", "Nuke", "Mirage"],
            [[13,7], [5,13], [None,None]]
        ]
        scores_first_2 = bo3_2maps[1][0:2]
        scores_last = bo3_2maps[1][-1]
        map_data = fetch_map_data(bo3_2maps[0], bo3_2maps[1])

        assert map_data
        assert len(map_data) == 3
        
        for score in map_data:
            assert "map" in score.keys()
            assert "team1_score" in score.keys()
            assert "team2_score" in score.keys()
        
        for i, score in enumerate(scores_first_2):
            assert [score for score in scores_first_2[i] if type(score) == int]

        assert [score for score in scores_last if score == None]
        
    def test_fetch_map_data_valid_bo3_3maps(self):
        bo3_3maps = [
            ["Dust2", "Nuke", "Mirage"],
            [[13,7], [5,13], [16,14]]
        ]
        
        map_data = fetch_map_data(bo3_3maps[0], bo3_3maps[1])
        
        assert map_data
        assert len(map_data) == 3

        for score in map_data:
            assert "map" in score.keys()
            assert "team1_score" in score.keys()
            assert "team2_score" in score.keys()

        for i, score in enumerate(bo3_3maps[1]):
            assert [score for score in bo3_3maps[1][i] if type(score) == int]

    def test_fetch_map_data_valid_bo5_3maps(self):
        bo5_3maps = [
            ["Mirage", "Ancient", "Inferno", "Nuke", "Train"],
            [[13,7], [13,5], [16,14], [None,None], [None,None]]
        ]
        scores_first_3 = bo5_3maps[1][0:3]
        scores_last_2 = bo5_3maps[1][3:5]
        map_data = fetch_map_data(bo5_3maps[0], bo5_3maps[1])
        
        assert map_data
        assert len(map_data) == 5

        for score in map_data:
            assert "map" in score.keys()
            assert "team1_score" in score.keys()
            assert "team2_score" in score.keys()

        for i, score in enumerate(scores_first_3):
            assert [score for score in scores_first_3[i] if type(score) == int]

        for i, score in enumerate(scores_last_2):
            assert [score for score in scores_last_2[i] if score == None]

    def test_fetch_map_data_valid_bo5_4maps(self):
        bo5_4maps = [
            ["Nuke", "Dust2", "Inferno", "Overpass", "Mirage"],
            [[6,13], [13,3], [13,9], [13,2], [None,None]]
        ]

        scores_first_4 = bo5_4maps[1][0:4]
        scores_last = bo5_4maps[1][-1]
        map_data = fetch_map_data(bo5_4maps[0], bo5_4maps[1])

        assert map_data
        assert len(map_data) == 5

        for score in map_data:
            assert "map" in score.keys()
            assert "team1_score" in score.keys()
            assert "team2_score" in score.keys()
            
        for i, score in enumerate(scores_first_4):
            assert [score for score in scores_first_4[i] if type(score) == int]

        for score in scores_last:
            assert [score for score in scores_last if score == None]

    def test_fetch_map_data_valid_bo5_5maps(self):
        bo5_5maps = [
            ["Nuke", "Dust2", "Inferno", "Overpass", "Mirage"],
            [[6,13], [13,3], [13,9], [13,2], [13,10]]
        ]
        map_data = fetch_map_data(bo5_5maps[0], bo5_5maps[1])

        assert map_data
        assert len(map_data) == 5

        for score in map_data:
            assert "map" in score.keys()
            assert "team1_score" in score.keys()
            assert "team2_score" in score.keys()
            
        for i, score in enumerate(bo5_5maps[1]):
            assert [score for score in bo5_5maps[1][i] if type(score) == int]