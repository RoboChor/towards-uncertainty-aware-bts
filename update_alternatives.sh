#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <container-name>"
    exit 1
fi

CONTAINER_NAME=$1

python3 bt-generator/condition_tree_gen.py
if [ $? -ne 0 ]; then
    exit 1
fi

python3 bt-generator/tree_generator.py
if [ $? -ne 0 ]; then
    exit 1
fi

XML_CONTENT=$(cat bt_generator/output/concrete_mission.xml)

docker exec $CONTAINER_NAME bash -c "
    source \${SPACEROS_DIR}/install/setup.bash && \
    source ~/demos_ws/install/setup.bash && \
    ros2 topic pub --once /behavior_tree std_msgs/msg/String \"{data: '$XML_CONTENT'}\"
"
