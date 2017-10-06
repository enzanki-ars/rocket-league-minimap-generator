ball_objects = []
car_objects = {}
player_info = {}
game_event_num = None
team_blue = None
team_orange = None


def parse_ball_obj_nums():
    from rocketleagueminimapgenerator.data.actor_data import get_actor_data

    global ball_objects

    ball_objects = []

    for i, obj in enumerate(get_actor_data()):
        if 'TAGame.Ball_TA' in get_actor_data()[obj]:
            ball_objects.append(i)


def get_ball_obj_nums():
    return ball_objects


def parse_game_event_num():
    from rocketleagueminimapgenerator.data.actor_data import get_actor_data

    global game_event_num

    game_event_num = 1

    for i, obj in enumerate(get_actor_data()):
        if 'TAGame.GameEvent_Soccar_TA' in get_actor_data()[obj]:
            game_event_num = i
            return


def get_game_event_num():
    return game_event_num


def parse_car_obj_nums():
    from rocketleagueminimapgenerator.data.data_loader import get_data, \
        get_data_end

    global car_objects

    car_objects = {}

    for frame in get_data()['content']['frames'][:get_data_end()]:
        for actor in frame['replications']:

            actor_id = actor['actor_id']['value']

            if 'updated_replication_value' in actor['value'].keys():
                for updated_data in \
                        actor['value']['updated_replication_value']:
                    if updated_data['name'] == \
                            'Engine.Pawn:PlayerReplicationInfo':
                        if actor_id not in car_objects.keys():
                            player_id = updated_data['value'][
                                'flagged_int_attribute_value']['int']
                            car_objects[actor_id] = player_id


def get_car_obj_nums():
    return car_objects


def parse_player_info():
    from tqdm import tqdm
    from rocketleagueminimapgenerator.data.data_loader import get_data, \
        get_data_end

    global player_info, team_blue, team_orange

    player_info = {}

    for car_id in get_car_obj_nums():
        if get_car_obj_nums()[car_id] not in player_info:
            player_info[get_car_obj_nums()[car_id]] = {}

    for i in tqdm(range(0, get_data_end()), desc='Player Info', ascii=True):
        for frame_data in get_data()['content']['frames'][i]['replications']:
            if frame_data['actor_id']['value'] in player_info:
                player_id = frame_data['actor_id']['value']

                if 'updated_replication_value' in frame_data['value'].keys():
                    for updated_data in \
                            frame_data['value']['updated_replication_value']:
                        if updated_data['name'] == \
                                'Engine.PlayerReplicationInfo:Team':
                            if 'team' not in player_info[player_id].keys():
                                player_info[player_id]['team'] = \
                                    updated_data['value'][
                                        'flagged_int_attribute_value']['int']
                        elif updated_data['name'] == \
                                'Engine.PlayerReplicationInfo:PlayerName':
                            player_info[player_id]['name'] = \
                                updated_data['value'][
                                    'string_attribute_value']
                        elif updated_data['name'] == \
                                'TAGame.PRI_TA:ClientLoadouts':
                            player_info[player_id]['items'] = \
                                updated_data['value'][
                                    'loadouts_attribute_value']

    team_nums = []
    for player in player_info:
        team_nums.append(player['team'])

    team_blue = min(team_nums)
    team_orange = max(team_nums)


def get_player_team_name(player_id):
    if get_player_info()[player_id]['team'] == 2:
        team_color = 'blue'
    elif get_player_info()[player_id]['team'] == 3:
        team_color = 'orange'
    else:
        team_color = 'grey'

    return team_color


def get_player_info():
    return player_info
