import xml.etree.ElementTree as ET
import os
import shutil


def concretize_mission():
    tree = ET.parse('./mission/mission.xml')
    root = tree.getroot()
    for Abstract in root.iter('Adaptable'):
        name = Abstract.get('ID')
        missionAdd = ('./output/' + name + '.xml')
        Abstract.tag = 'SubTree'
        MissionTree = ET.parse(missionAdd)
        Missionroot = MissionTree.getroot()
        for BTree in Missionroot.iter('BehaviorTree'):
            root.append(BTree)

    tree.write('./output/adaptable_bt.xml')

def GenAdaptSubTree():

    resource_direction = "./resource"
    for adaptable_name in os.listdir(resource_direction):
        tree = ET.fromstring('<root main_tree_to_execute = "MainTree"></root>')
        root = tree.getroot()
        behavior = ET.Element('BehaviorTree')
        behavior.set('ID', adaptable_name)
        root.append(behavior)
        alternative_folder = os.path.join(resource_direction, adaptable_name)
        path = './output/' + adaptable_name + '.xml'
        adapt_fallback = ET.Element('Fallback')
        for alternative_name in os.listdir(alternative_folder):
            alternative_dir = os.path.join(alternative_folder, alternative_name)
            alternative_xml_dir = os.path.join(alternative_dir, (alternative_name)) + '.xml'
            alternative_condition_xml_dir = os.path.join(alternative_dir, (alternative_name)) + '_conditions.xml'
            alt_tree = ET.parse(alternative_xml_dir)
            alt_tree_root = alt_tree.getroot()
            alt_cond_tree = ET.parse(alternative_condition_xml_dir)
            alt_cond_tree_root = alt_cond_tree.getroot()
            alt_sequence = ET.Element('Sequence')
            new_element = ET.Element('SubTree')
            for altbehavior_tree in alt_tree_root.iter('BehaviorTree'):
                new_element.set('ID', altbehavior_tree.get('ID'))
                root.append(altbehavior_tree)
                break

            new_element2 = ET.Element('SubTree')

            for condbehavior_tree in alt_cond_tree_root.iter('BehaviorTree'):
                new_element2.set('ID', condbehavior_tree.get('ID'))
                root.append(condbehavior_tree)
                break

            alt_sequence.append(new_element2)
            alt_sequence.append(new_element)
            adapt_fallback.append(alt_sequence)

        tmp_sequence = ET.Element('Sequence')
        tmp_sequence.append(adapt_fallback)
        behavior.extend(tmp_sequence)
        path = './output/'+adaptable_name+'.xml'
        delete_file(path)
        #root.append(behavior)
        tree.write(path)



def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def ReadIDOftree(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root[0].get('ID')


def clear_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    root.clear()
    tree.write(filename)


def create_tmp_BT(ID):
    alt_tmp_tree = ET.parse('tmp/Alt_tmp.xml')
    alt_tmp_root = alt_tmp_tree.getroot()
    for BT in alt_tmp_root.iter('BehaviorTree'):
        BT.set("ID", ID)

    alt_tmp_tree.write('./Execute/Alt_tmp.xml')


if __name__ == '__main__':

    directory = './output'
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
    # adaptable subtree generation algorithm
    GenAdaptSubTree()
    concretize_mission()
    #concretize_mission()
    print('Done')
