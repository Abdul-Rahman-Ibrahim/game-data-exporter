import os
import json
from libs.helper import *
from libs.elmas.home import Home
from libs.elmas.stages import Stages
from libs.elmas.stage6 import Stage6
from libs.elmas.stage1_5 import Stage1_5
from libs.elmas.stage2_3_4 import Stage2_3_4


class Game:
    def __init__(self, ID, data):
        self.ID = ID
        self.home = Home(data[ID]['home'])
        self.main = data[ID]['main']
        self.parameters = data[ID]['parameters']
        self.stage1 = Stage1_5(data[ID]['stage1'])
        self.stage2 = Stage2_3_4(data[ID]['stage2'])
        self.stage3 = Stage2_3_4(data[ID]['stage3'])
        self.stage4 = Stage2_3_4(data[ID]['stage4'])
        self.stage5 = Stage1_5(data[ID]['stage5'])
        self.stage6 = Stage6(data[ID]['stage6'])
        self.stages = Stages(data[ID]['stages'])


if __name__ == '__main__':
    GAMELOG_IN = 'gamelog_in/'
    GAME_NAME = 'Elmas'

    files = os.listdir(GAMELOG_IN)
    json_files = [f for f in files if f.endswith('.json')]

    STAGE2DATA = []
    STAGE3DATA = []
    NUM_LEVELS = 10
    
    for json_file in json_files:
        file_path = f'{GAMELOG_IN}/{json_file}'
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        try:
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

                STAGE2 = game.stage2
                STAGE3 = game.stage3

                gametype = selection.gametype
                player1data = selection.player1data
                student_id_p1, cinsiyet_p1, studentname_p1, gametype_p1, grade_name_p1, grup_p1, school_name_p1, variation_p1 = (None,) * 8
                if player1data is not None and type(player1data) is not bool:
                    gametype_p1, cinsiyet_p1, grade_name_p1, student_id_p1, studentname_p1, school_name_p1 = get_player_data(player1data)

                player2data = selection.player2data
                student_id_p2, cinsiyet_p2, studentname_p2, gametype_p2, grade_name_p2, grup_p2, school_name_p2, variation_p2 = (None,) * 8
                if player2data is not None and type(player2data) is not bool:
                    gametype_p2, cinsiyet_p2, grade_name_p2, student_id_p2, studentname_p2, school_name_p2 = get_player_data(player2data)

                playerdata = selection.playerdata
                student_id_p, cinsiyet_p, studentname_p, gametype_p, grade_name_p, grup_p, school_name_p, variation_p = (None,) * 8
                if playerdata is not None and type(playerdata) is not bool:
                    gametype_p, cinsiyet_p, grade_name_p, student_id_p, studentname_p, school_name_p = get_player_data(playerdata)
                
                if gametype == 'cooperative':
                    if student_id_p1 == student_id_p2:
                        continue

                if student_id_p1 is None and student_id_p2 is None:
                    student_id_p1, student_id_p2 = student_id_p, student_id_p
                if cinsiyet_p1 is None and cinsiyet_p2 is None:
                    cinsiyet_p1, cinsiyet_p2 = cinsiyet_p, cinsiyet_p
                if school_name_p1 is None and school_name_p2 is None:
                    school_name_p1, school_name_p2 = school_name_p, school_name_p
                if grade_name_p1 is None and grade_name_p2 is None:
                    grade_name_p1, grade_name_p2 = grade_name_p, grade_name_p
                
                if (student_id_p1 and student_id_p2 and cinsiyet_p1 and cinsiyet_p2):

                    student_data2 = get_init_row(game_ID, student_id_p1, student_id_p2, cinsiyet_p1, cinsiyet_p2, grade_name_p1, grade_name_p2, gametype, school_name_p1, school_name_p2, GAME_NAME)
                    stage2_data = get_stage_data(STAGE2.player1levels, gametype, 2)
                    rows = get_rows(stage2_data, 1, NUM_LEVELS)
                    for exe_no, lst in rows.items():
                        STAGE2DATA.append(student_data2 + lst)         
                    if gametype == 'cooperative':
                        student_data2 = get_init_row(game_ID, student_id_p1, student_id_p2, cinsiyet_p1, cinsiyet_p2, grade_name_p1, grade_name_p2, gametype, school_name_p1, school_name_p2, GAME_NAME)
                        stage2_data = get_stage_data(STAGE2.player1levels, gametype, 2)
                        rows = get_rows(stage2_data, 2, NUM_LEVELS)
                        for exe_no, lst in rows.items():
                            STAGE2DATA.append(student_data2 + lst)     
                    elif gametype == 'competitive':
                        if not all(i is None for i in STAGE2.player2levels) and not all(i is None for i in STAGE3.player2levels):
                            student_data2 = get_init_row(game_ID, student_id_p1, student_id_p2, cinsiyet_p1, cinsiyet_p2, grade_name_p1, grade_name_p2, gametype, school_name_p1, school_name_p2, GAME_NAME)
                            stage2_data = get_stage_data(STAGE2.player2levels, gametype, 2)
                            rows = get_rows(stage2_data, 1, NUM_LEVELS, competitive=True)
                            for exe_no, lst in rows.items():
                                STAGE2DATA.append(student_data2 + lst)
                        else:
                            pass
                            for exe_no, lst in rows.items():
                                STAGE2DATA.pop()

                    student_data3 = get_init_row(game_ID, student_id_p1, student_id_p2, cinsiyet_p1, cinsiyet_p2, grade_name_p1, grade_name_p2, gametype, school_name_p1, school_name_p2, GAME_NAME)
                    stage3_data = get_stage_data(STAGE3.player1levels, gametype, 3)
                    rows = get_rows(stage3_data, 1, NUM_LEVELS)
                    for exe_no, lst in rows.items():
                        STAGE3DATA.append(student_data3 + lst)     
                    if gametype == 'cooperative':
                        student_data3 = get_init_row(game_ID, student_id_p1, student_id_p2, cinsiyet_p1, cinsiyet_p2, grade_name_p1, grade_name_p2, gametype, school_name_p1, school_name_p2, GAME_NAME)
                        stage3_data = get_stage_data(STAGE3.player1levels, gametype, 3)
                        rows = get_rows(stage3_data, 2, NUM_LEVELS)
                        for exe_no, lst in rows.items():
                            STAGE3DATA.append(student_data3 + lst)     
                    elif gametype == 'competitive':
                        if not all(i is None for i in STAGE2.player2levels) and not all(i is None for i in STAGE3.player2levels):
                            student_data3 = get_init_row(game_ID, student_id_p1, student_id_p2, cinsiyet_p1, cinsiyet_p2, grade_name_p1, grade_name_p2, gametype, school_name_p1, school_name_p2, GAME_NAME)
                            stage3_data = get_stage_data(STAGE3.player2levels, gametype, 3)
                            rows = get_rows(stage3_data, 1, NUM_LEVELS, competitive=True)
                            for exe_no, lst in rows.items():
                                STAGE3DATA.append(student_data3 + lst)
                        else:
                            pass
                            for exe_no, lst in rows.items():
                                STAGE3DATA.pop()                  
                
                num_columns2 = len(student_data2) + len(lst)
                if len(STAGE2DATA) and not all(i is None for i in STAGE2DATA[-1]):
                    STAGE2DATA.append([None] * num_columns2)

                num_columns3 = len(student_data3) + len(lst)
                if len(STAGE3DATA) and not all(i is None for i in STAGE3DATA[-1]):
                    STAGE3DATA.append([None] * num_columns3)
        except:
            print(f'Error: {json_file}')

    
    df2 = export_stage_data(STAGE2DATA, stage2_data, "elma_s2.xlsx", student_data2, NUM_LEVELS, 2)
    df3 = export_stage_data(STAGE3DATA, stage3_data, "elma_s3.xlsx", student_data3, NUM_LEVELS, 3)


    common_columns = [
        'game_id', 'game_type','p1_student_id', 'p2_student_id',
        'p1_gender', 'p2_gender', 'p1_grade',
        'p2_grade', 'school_p1',
        'school_p2', 'game_name', 'execute_no'
    ]

    df3.drop(columns=common_columns, inplace=True)
    df_combined = pd.concat([df2, df3], axis=1)
    df_combined.to_excel("elma_s2_s3.xlsx", index=False)