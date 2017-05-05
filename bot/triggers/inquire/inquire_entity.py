"""Trigger implementation for inquiring entity info"""

import json
from os import listdir

from app import APP_INSTANCE as app
from utils import tts

def run(execution_context):
    """run the action"""
    # opening = app.get_config('behavior.entity_react.opening')
    no_data_react = app.get_config('behavior.entity_react.no_data')
    confused_react = app.get_config('behavior.entity_react.confused')
    not_support_react = app.get_config('behavior.entity_react.not_support')

    inquire_type = execution_context.event_name.split('.')[2]
    tagged_text = execution_context.event.get('tagged_text')
    entity_name = [w[0] for w in tagged_text if w[1] == 'NN' or w[1] == 'JJ']

    file_names = get_file_names(entity_name)
    if len(file_names) == 0:
        tts.say_random_finish(no_data_react, execution_context)
        return

    if len(file_names) > 1:
        entitie_names = [get_entity_name(f) for f in file_names]
        tts.say_random_finish(confused_react, execution_context, {
            'count': len(file_names),
            'entities': ', '.join(entitie_names)
        })
        return

    entity = get_entity(file_names[0])
    if inquire_type not in entity:
        tts.say_random_finish(not_support_react, execution_context)
        return
    info = entity[inquire_type]
    execution_context.finish(info)
    tts.say([info])

def get_file_names(entity_name):
    """get the matched file names for a given entity name"""
    files = list(filter(lambda file: ".json" in file, listdir('cache/entities')))
    result = []
    for file_name in files:
        file_name = file_name.replace('.json', '')
        frags = file_name.split('_')
        matched = count_match(frags, entity_name)
        if matched == len(frags):
            return [file_name]
        if matched > 0:
            result.append(file_name)
    return result

def count_match(frags, entity_name):
    """check if the file matchs entity_name"""
    return len([f for f in frags if f in entity_name])

def get_entity_name(file_name):
    """get entity name from file"""
    entity = get_entity(file_name)
    return entity['name']

def get_entity(file_name):
    """get entity by file name"""
    with open('cache/entities/' + file_name + '.json') as data_file:
        return json.load(data_file)