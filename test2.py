import os
import json
from libs.helper import *
from libs.sections.home import Home
from libs.sections.stages import Stages
from libs.sections.stage6 import Stage6
from libs.sections.stage1_5 import Stage1_5
from libs.sections.stage2_3_4 import Stage2_3_4


class Game:
    def __init__(self, ID, data):
        self.ID = ID
        self.data = data
        self.home = Home(data.get(ID).get('home'))
        self.main = data.get(ID).get('main')
        self.parameters = data[ID].get('parameters')
        # self.stage1 = Stage1_5(data.get(ID, {}).get('stage1'))
        self.stage2 = Stage2_3_4(data.get(ID).get('stage2'))
        self.stage3 = Stage2_3_4(data.get(ID).get('stage3'))
        # self.stage4 = Stage2_3_4(data.get(ID, {}).get('stage4'))
        # self.stage5 = Stage1_5(data.get(ID, {}).get('stage5'))
        # self.stage6 = Stage6(data.get(ID, {}).get('stage6'))
        # self.stages = Stages(data.get(ID, {}).get('stages'))


if __name__ == '__main__':

    logdata = 'logdata/'
    folders = [name for name in os.listdir(logdata) if os.path.isdir(os.path.join(logdata, name))]

    STAGE2DATA = []
    STAGE3DATA = []
    NUM_LEVELS = 10

    json_files = []
    for folder in folders:
        files = os.listdir(f'{logdata}/{folder}')
        if len(files) == 0:
            continue
        json_files = json_files + [f'{logdata}/{folder}/{f}' for f in files if f.endswith('.json')]

    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        print(json_file)
        games = []
        for key in data.keys():
            games.append(Game(key, data))
        
        for game in games:
            game_ID = game.ID
            HOME = game.home
            selections = HOME.selections
            if selections:
                selection = selections[0]
            else:
                continue

            MAIN = game.main
            GAME_NAME = MAIN.get('gamename')

            STAGE2 = game.stage2
            STAGE3 = game.stage3

            gametype = selection.gametype
            player1data = selection.player1data