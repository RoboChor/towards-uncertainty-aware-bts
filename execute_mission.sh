#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <container-name>"
  exit 1
fi

CONTAINER_NAME=$1

XML_FILE="mission-scenario/uncertainty_aware_bt.xml"
XML_CONTENT=$(cat "$XML_FILE")

docker exec -it "$CONTAINER_NAME" /bin/bash -c "
source \${SPACEROS_DIR}/install/setup.bash &&
source ~/demos_ws/install/setup.bash &&
ros2 topic pub --once /behavior_tree std_msgs/msg/String '{data: \"$XML_CONTENT\"}'
"
