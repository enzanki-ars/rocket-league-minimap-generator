actor_data = {}


def get_actor_data():
    return actor_data


def parse_actor_data():
    global actor_data
    from rocketleaguereplayparser.data import get_data

    for frame in get_data()['content']['frames']:
        for actor in frame['replications']:

            actor_id = actor['actor_id']['value']

            if actor_id not in actor_data.keys():
                actor_data[actor_id] = []

            if 'spawned_replication_value' in actor['value'].keys():
                if actor['value']['spawned_replication_value'][
                    'class_name'] not in \
                        actor_data[actor_id]:
                    actor_data[actor_id].append(
                            actor['value']['spawned_replication_value'][
                                'class_name'])
            elif 'updated_replication_value' in actor['value'].keys():
                for updated_data in \
                        actor['value']['updated_replication_value']:
                    if updated_data['name'] not in actor_data[actor_id]:
                        actor_data[actor_id].append(updated_data['name'])
