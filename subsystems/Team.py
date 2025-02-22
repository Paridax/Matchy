from dotenv import dotenv_values
import requests

# get environment variables
env_vars = dotenv_values('.env')

# get api key
headers = {
    "X-TBA-Auth-Key": env_vars['X-TBA-Auth-Key']
}

class Team:
    def __init__(self, team: str, year: str):
        self.team = team
        self.year = year
        self.team_number = team[3:]
        self.url = f"https://www.thebluealliance.com/api/v3/team/{team}/matches/{year}"
        self.fetch()

    def fetch(self):
        response = requests.request("GET", self.url, headers=headers)
        # if the response has an error in it, return the error
        if "Error" in response.json():
            self.error = True
            self.error_msg = response.json()["Error"]
            self.games = []
        else:
            self.error = False
            self.error_msg = None
            self.games = response.json()
        
    def getAlliance(self, blue_teams: list[str]):
        if self.team in blue_teams:
            # we are blue
            our_alliance = "blue"
        else:
            # we are red
            our_alliance = "red"
        return our_alliance

    def getWinPercentage(self):
        # (re)set variables
        self.wins = 0
        self.loses = 0
        self.ties = 0

        # loop over games
        for game in self.games:
            blue_teams = game['alliances']['blue']['team_keys']
            our_alliance = self.getAlliance(blue_teams)
            
            # check if we won
            if our_alliance == game['winning_alliance']:
                # print("We won.")
                self.wins += 1
            elif game['alliances']['blue']['score'] == game['alliances']['red']['score']:
                # print("We tied.")
                # ties are inferred
                pass
            else:
                # print ("We lost")
                self.loses += 1
        # get total games
        total = len(self.games)

        # get ties
        self.ties = total - (self.wins + self.loses)

        # get percents
        # desired / total
        self.winPercent = self.wins/total
        self.tiePercent = self.ties/total
        self.losePercent = self.loses/total
        return {
            'winPercent': self.winPercent,
            'tiePercent': self.tiePercent,
            'losePercent': self.losePercent
        }
    
    def getAverageScore(self):
        # (re)set variables
        self.total_points = 0
        for game in self.games:
            # get alliance
            blue_teams = game['alliances']['blue']['team_keys']
            our_alliance = self.getAlliance(blue_teams)

            # find current team points and increment total points
            if our_alliance == "blue":
                blue_total_points = game['score_breakdown']['blue']['totalPoints']
                self.total_points += blue_total_points
            else:
                red_total_points = game['score_breakdown']['red']['totalPoints']
                self.total_points += red_total_points
            
        self.average_score = self.total_points/len(self.games)
        return self.average_score
    
"""
example game
{
    "actual_time": 1649352719,
    "alliances": {
      "blue": {
        "dq_team_keys": [],
        "score": 44,
        "surrogate_team_keys": [],
        "team_keys": [
          "frc6327",
          "frc1676",
          "frc293"
        ]
      },
      "red": {
        "dq_team_keys": [],
        "score": 71,
        "surrogate_team_keys": [],
        "team_keys": [
          "frc2016",
          "frc3637",
          "frc1403"
        ]
      }
    },
    "comp_level": "qm",
    "event_key": "2022mrcmp",
    "key": "2022mrcmp_qm1",
    "match_number": 1,
    "post_result_time": 1649352926,
    "predicted_time": 1649352783,
    "score_breakdown": {
      "blue": {
        "adjustPoints": 0,
        "autoCargoLowerBlue": 0,
        "autoCargoLowerFar": 0,
        "autoCargoLowerNear": 0,
        "autoCargoLowerRed": 0,
        "autoCargoPoints": 12,
        "autoCargoTotal": 3,
        "autoCargoUpperBlue": 1,
        "autoCargoUpperFar": 1,
        "autoCargoUpperNear": 0,
        "autoCargoUpperRed": 1,
        "autoPoints": 18,
        "autoTaxiPoints": 6,
        "cargoBonusRankingPoint": true,
        "endgamePoints": 6,
        "endgameRobot1": "Mid",
        "endgameRobot2": "None",
        "endgameRobot3": "None",
        "foulCount": 1,
        "foulPoints": 0,
        "hangarBonusRankingPoint": false,
        "matchCargoTotal": 20,
        "quintetAchieved": false,
        "rp": 1,
        "taxiRobot1": "Yes",
        "taxiRobot2": "Yes",
        "taxiRobot3": "Yes",
        "techFoulCount": 0,
        "teleopCargoLowerBlue": 6,
        "teleopCargoLowerFar": 4,
        "teleopCargoLowerNear": 0,
        "teleopCargoLowerRed": 4,
        "teleopCargoPoints": 20,
        "teleopCargoTotal": 17,
        "teleopCargoUpperBlue": 0,
        "teleopCargoUpperFar": 1,
        "teleopCargoUpperNear": 0,
        "teleopCargoUpperRed": 2,
        "teleopPoints": 26,
        "totalPoints": 44
      },
      "red": {
        "adjustPoints": 0,
        "autoCargoLowerBlue": 0,
        "autoCargoLowerFar": 0,
        "autoCargoLowerNear": 0,
        "autoCargoLowerRed": 0,
        "autoCargoPoints": 16,
        "autoCargoTotal": 4,
        "autoCargoUpperBlue": 2,
        "autoCargoUpperFar": 1,
        "autoCargoUpperNear": 1,
        "autoCargoUpperRed": 0,
        "autoPoints": 20,
        "autoTaxiPoints": 4,
        "cargoBonusRankingPoint": false,
        "endgamePoints": 25,
        "endgameRobot1": "Traversal",
        "endgameRobot2": "None",
        "endgameRobot3": "High",
        "foulCount": 0,
        "foulPoints": 4,
        "hangarBonusRankingPoint": true,
        "matchCargoTotal": 15,
        "quintetAchieved": false,
        "rp": 3,
        "taxiRobot1": "Yes",
        "taxiRobot2": "No",
        "taxiRobot3": "Yes",
        "techFoulCount": 0,
        "teleopCargoLowerBlue": 0,
        "teleopCargoLowerFar": 0,
        "teleopCargoLowerNear": 0,
        "teleopCargoLowerRed": 0,
        "teleopCargoPoints": 22,
        "teleopCargoTotal": 11,
        "teleopCargoUpperBlue": 1,
        "teleopCargoUpperFar": 3,
        "teleopCargoUpperNear": 5,
        "teleopCargoUpperRed": 2,
        "teleopPoints": 47,
        "totalPoints": 71
      }
    },
    "set_number": 1,
    "time": 1649352600,
    "videos": [
      {
        "key": "Y_3eIXcah4A",
        "type": "youtube"
      }
    ],
    "winning_alliance": "red"
}
"""