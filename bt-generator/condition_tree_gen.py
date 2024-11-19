import json
import xml.etree.ElementTree as ET
import os
import shutil

def load_json(address):
    requierments = json.load(open(address, 'r'))
    return requierments


def info_elicitation(requierments):
    for req in requierments:
        if req['semantics']['component_name'].lower() == 'mission':
            adapt_name = req['semantics']['scope_mode']
            conditons = req['semantics']['pre_condition']
            response = req['semantics']['post_condition']
            conditions_name, conditions_value = condition_elicitation(conditons)
            alt_name = altname_elicitation(response)
            make_Condition_BT(adapt_name, conditions_name, conditions_value, alt_name)


def make_Condition_BT(adapt_name: str, conditions_name: str, conditions_value: str, alt_name: str):
    directory = 'resource/' + adapt_name
    if not os.path.exists(directory):
        os.makedirs(directory)
    address = directory + '/' + alt_name + '_conditions.xml'
    tree = ET.fromstring('<root main_tree_to_execute = "MainTree"></root>')
    root = tree.getroot()
    BT_element = ET.Element('BehaviorTree')
    BT_element.set('ID', adapt_name.lower() + '_' + alt_name.lower() + '_conditions')
    sequence_element = ET.Element('Sequence')
    CheckCondition = ET.Element(conditions_name)
    sequence_element.append(CheckCondition)
    BT_element.append(sequence_element)
    root.append(BT_element)
    tree.write(address)


def altname_elicitation(response: str):
    return response.split('=')[1].replace(')', '').strip()


def condition_elicitation(conditions):

    conditions = remove_paranthesis(conditions)
    conditions = remove_blank_space(conditions)
    if check_inversion(conditions):
        conditions = remove_inverter_from_condition(conditions)
        conditions = remove_blank_space(conditions)
        conditions_name = conditions
        conditions_value = 'false'
    else:
        conditions = remove_blank_space(conditions)
        conditions_name = conditions
        conditions_value = 'true'
    return conditions_name, conditions_value


def remove_inverter_from_condition(cond: str):
    return cond.replace('!', '')


def remove_paranthesis(cond: str):
    return cond.replace('(', '').replace(')', '')


def remove_blank_space(cond: str):
    return cond.strip()


def check_inversion(cond: str):
    op = '!'
    return cond[0].__eq__(op)


if __name__ == '__main__':
    requirement_loc = "mission/fretRequirements.json"
    info_elicitation(load_json(requirement_loc))
