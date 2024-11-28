import re
import datetime
import pandas as pd

def get_date_time(timestamp):
    if timestamp is None:
        return (None, None)
    timestamp_sec = timestamp/1000
    dt_object = datetime.datetime.fromtimestamp(timestamp_sec)
    
    year = dt_object.year
    month = dt_object.month
    day = dt_object.day

    hour = dt_object.hour
    minute = dt_object.minute
    second = dt_object.second

    date = f'{year}-{month:02d}-{day:02d}'
    time = f'{hour:02d}:{minute:02d}:{second:02d}'
    return date, time


def get_player_data(playerdata):
    gametype = playerdata.get('gametype', '')
    cinsiyet = playerdata.get('cinsiyet', '')
    studentname = playerdata.get('student_name', '')
    grade_name = playerdata.get('grade_name', '')
    school_name = playerdata.get('school_name', '')
    student_id = playerdata.get('student_id', '')
    if student_id == '':
        student_id = playerdata.get('student_no', '')
    return (gametype, cinsiyet, grade_name, student_id, studentname, school_name)

def get_init_row(game_ID,
                 student_id_p1,
                 student_id_p2,
                 cinsiyet_p1,
                 cinsiyet_p2,
                 grade_name_p1,
                 grade_name_p2,
                 gametype,
                 school_name_p1,
                 school_name_p2,
                 GAME_NAME
                 ):

    return [
        game_ID,
        gametype,
        student_id_p1,
        student_id_p2,
        cinsiyet_p1,
        cinsiyet_p2,
        grade_name_p1,
        grade_name_p2,
        school_name_p1,
        school_name_p2,
        GAME_NAME
    ]

def get_executed_player(blockType):
    player = -1
    for block in blockType:
        if block is not None:
            match = re.search(r'\d+', block)
            if match is not None:
                player = match.group()
    return int(player)

def get_execute_data(blockType, eventType, message, starttime, gametype, level_num):
    execute_data = {}
    actions_count = 0
    execute_count = 0
    idx = 0

    delete_count = 0
    create_count = 0
    move_count = 0

    delete_count_2 = 0
    create_count_2 = 0
    move_count_2 = 0

    player = 1

    for i in range(len(eventType)):
        if eventType[i] == 'execute':
            execute_time = starttime[i]
            try:
                status = message[i+1]
            except IndexError:
                status = 'incomplete'
            except:
                status = 'incomplete'
            
            if status == 'missionincomplete' or status is None:
                status = 'incomplete'
            elif status == 'accomplished_odullu':
                status = 'success*'
            else:
                status = 'success'
            
            if gametype == 'individual' or gametype == 'competitive':
                player = 1
            else:
                player = get_executed_player(blockType[idx:i])
                idx = i

            execute_count += 1

            execute_data[execute_count] = (execute_count, execute_time, actions_count, status, player, [create_count, create_count_2], [move_count, move_count_2], [delete_count, delete_count_2])
            actions_count = 0
            actions_count_2 = 0

            delete_count = 0
            create_count = 0
            move_count = 0
    
            delete_count_2 = 0
            create_count_2 = 0
            move_count_2 = 0

        else:
            if eventType[i] == 'move':
                move_count += 1
            elif eventType[i] == 'delete':
                delete_count += 1
            elif eventType[i] == 'create':
                create_count += 1
            
            if gametype == 'cooperative':
                if eventType[i] == 'move' and str(player) in blockType[i]:
                    move_count_2 += 1
                elif eventType[i] == 'delete' and str(player) in blockType[i]:
                    delete_count_2 += 1
                elif eventType[i] == 'create' and str(player) in blockType[i]:
                    create_count_2 += 1

        actions_count += 1

    
    return execute_data

def get_stage_data(playerlevels, gametype, stage_num):
    stage_data = {}

    for i, level in enumerate(playerlevels, start=1):
        if level is None:
            stage_data[f's{stage_num}_l{i}'] = {}
            continue

        event_data = {
            "blockId": [event.blockId for event in level.events],
            "blockType": [event.blockType for event in level.events],
            "code": [event.code for event in level.events],
            "eventType": [event.eventType for event in level.events],
            "starttime": [event.starttime for event in level.events],
            "message": [event.message for event in level.events]
        }

        blockType = event_data['blockType']
        eventType = event_data['eventType']
        message = event_data['message']
        starttime = event_data["starttime"]

        execute_data = get_execute_data(blockType, eventType, message, starttime, gametype, i)
        stage_data[f's{stage_num}_l{i}'] = execute_data
    
    return stage_data


def get_rows(stage_data, player, NUM_LEVELS, competitive=False, MAX_EXECUTION=10):
    rows = {}
    for i in range(1, MAX_EXECUTION + 1):
        rows[i] = [i]

    count = 1
    for lv, execute_data in stage_data.items():
        for i in range(1, MAX_EXECUTION + 1):
            try:
                tup = execute_data[i]
                if player == tup[4]:
                    rows[i].append(get_date_time(tup[1])[1])
                    x = tup[5][0] - tup[5][1] + tup[6][0] - tup[6][1] + tup[7][0] - tup[7][1]
                    rows[i].append(x) # num_actions
                    rows[i].append(tup[5][0] - tup[5][1]) # create
                    rows[i].append(tup[6][0] - tup[6][1]) # move
                    rows[i].append(tup[7][0] - tup[7][1]) # delete
                    rows[i].append(tup[3])

                    if competitive:
                        rows[i].append(2)
                    else:
                        rows[i].append(tup[4])
                    
                else:
                    rows[i].append(None)   # time
                    x = tup[5][1] + tup[6][1] + tup[7][1]
                    rows[i].append(x) # num_actions
                    rows[i].append(tup[5][1]) # create
                    rows[i].append(tup[6][1]) # move
                    rows[i].append(tup[7][1]) # delete
                    rows[i].append(None)

                    if competitive:
                        rows[i].append(2)
                    else:
                        rows[i].append(player)
                    
                    
            except KeyError:
                rows[i].append(None) # time
                rows[i].append(None) # num_actions
                rows[i].append(None) # create
                rows[i].append(None) # move
                rows[i].append(None) # delete
                rows[i].append(None)

                if competitive:
                    rows[i].append(2)
                else:
                    rows[i].append(player)
        
        if count == NUM_LEVELS:
            break
        count += 1
    
    return rows

def get_column_names(stage_data, NUM_LEVELS):
    column_names = ['execute_no']
    count = 1
    for lv, execute_data in stage_data.items():
        time = f'{lv}_execute_time'
        no_action = f'{lv}_no_action'
        create_count = f'{lv}_no_create'
        move_count = f'{lv}_no_move'
        delete_count = f'{lv}_no_delete'
        status = f'{lv}_status'
        player = f'{lv}_player'

        column_names.append(time)
        column_names.append(no_action)
        column_names.append(create_count)
        column_names.append(move_count)
        column_names.append(delete_count)
        column_names.append(status)
        column_names.append(player)

        if count == NUM_LEVELS:
            break
        count += 1
    
    return column_names

def export_stage_data(data, stage_data, filename, student_data, NUM_LEVELS, stage_num):
    tmp_main_columns = get_column_names(stage_data, NUM_LEVELS)
    
    main_columns = [
        'game_id', 'game_type', 'p1_student_id', 'p2_student_id',
        'p1_gender', 'p2_gender', 'p1_grade', 'p2_grade',
        'school_p1', 'school_p2', 'game_name'
    ] + tmp_main_columns

    sub_col = [None] * len(student_data) + ['Clicks on Run button']
    for i in range(NUM_LEVELS):
        sub_col.append(f'Stage {stage_num} Level {i+1}')
        sub_col.append(f'Stage {stage_num} Level {i+1}')
        sub_col.append(f'Stage {stage_num} Level {i+1}')
        sub_col.append(f'Stage {stage_num} Level {i+1}')
        sub_col.append(f'Stage {stage_num} Level {i+1}')
        sub_col.append(f'Stage {stage_num} Level {i+1}')
        sub_col.append(f'Stage {stage_num} Level {i+1}')
    
    df = pd.DataFrame(data, columns=main_columns)
    df.loc[-1] = sub_col
    df.index = df.index + 1
    df = df.sort_index()

    # df.to_excel(filename, index=False)

    return df
