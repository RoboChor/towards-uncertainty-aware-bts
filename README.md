# Towards Adaptable and Uncertainty-aware Behavior Trees

This repository contains the replication package of the paper **Towards Adaptable and Uncertainty-aware Behavior Trees** submitted at **7th International Workshop on Robotics Software Engineering (RoSE’25)**

## Authors
This study has been designed, developed, and reported by the following investigators:
- Mehran Rostamnia (Gran Sasso Science Institute, Italy)
- Gianluca Filippone (Gran Sasso Science Institute, Italy)
- Ricardo Caldas (Chalmers and University of Gothenburg, Italy)
- Patrizio Pelliccione (Gran Sasso Science Institute, Italy)

## Repository Structure
```
towards-uncertainty-aware-bts
|   README.md                   # This file
|   execute_mission.sh          # Script for launching the mission
|   update_alternatives.sh      # Script for updating the mission with new alternatives
├---bt-generator
|   |   condition_tree_gen.py   # Condition-checking subtree generator
|   |   tree_generator.py       # Uncertainty-aware BT generator
|   ├---mission
|   |      fretRequirements.json    # Fretish requirements to be parsed by the condition_tree_gen.py
|   |      mission.xml          # Adapbtle BT of the mission to be parsed by tree_generator.py
|   └---resource                # BTs of the alternatives 
├---fretish-syntax              # ANTLR definition of the FRETISH grammar subset
└---mission-scenario
    |   adaptable_bt.xml        # Adaptable BT of the mission
    |   al1.xml                 # Navigation alternative 1 (Dust)
    |   al2.xml                 # Navigation alternative 1 (Rocks)
    |   requirements.txt        # FRETISH conditions specification
    |   uncertainty_aware_bt.xml    # Uncertainty-aware BT of the mission
    └---imgs                    # Mission BT images
```

### BT Manager
The BT Manager implementation is provided within the forked [Space ROS Demo repository](https://github.com/gianlucafilippone/spaceros-demos).

## Example mission

### Adaptable Behavior Tree
<p align="center">
  <img src="/mission-scenario/imgs/adaptable_bt.png" alt="adaptable behavior tree">
</p>

### Provided behavior alternatives
Robot's navigation on dust terrain (`alt1`):
<p align="center">
  <img src="/mission-scenario/imgs/alt1.png" alt="on dust alternative">
</p>

Fretish requirement:
```
In navigation IF OnDust Mission SHALL SATISFY selected_alt=alt1
```

Robot's navigation on rocks (`alt2`):
<p align="center">
  <img src="/mission-scenario/imgs/alt2.png" alt="on rocks alternative">
</p>

Fretish requirement:
```
In navigation IF OnRock Mission SHALL SATISFY selected_alt=alt2
```

## Instructionss
### Pre-requisites
- Docker
- Python 3

### Installation
Clone the forked [Space Ros Docker repository](https://github.com/gianlucafilippone/uncertainty-bt-space-ros-docker):

```bash
git clone https://github.com/gianlucafilippone/uncertainty-bt-space-ros-docker
```

Follow the [instructions](https://github.com/gianlucafilippone/uncertainty-bt-space-ros-docker/blob/main/space_robots/README.md) to build Moveit2 and space robots:

```bash
cd uncertainty-bt-space-ros-docker/moveit2
./build.sh
cd ../space_robots
./build.sh
```

> [!NOTE]  
> Building `moveit2` and `space_robots` requires some minutes

### Running the Docker container

Run the following to allow GUI passthrough:
```bash
xhost +local:docker
```

Then run the container:
```bash
./run.sh
```
> [!NOTE]
> Depending on the host computer, you might need to remove the ```--gpus all``` flag in ```run.sh```, which uses your GPUs.

After running the `run.sh` script, a bash within the Docker container will be accessed.

### Running the Mars Rover

Run the following command to launch the Gazebo simulation of Curiosity Mars Rover:

```bash
ros2 launch mars_rover mars_rover.launch.py
```

To manually interact with the rover, follow the [space robots instructions in the Docker repository](https://github.com/gianlucafilippone/uncertainty-bt-space-ros-docker/blob/main/space_robots/README.md#perform-tasks).

### Run the BT Manager component

Open a new terminal and attach to the currently running container:

```bash
docker exec -it <container-name> bash
```

> [!NOTE]
> To get the container name, run `docker container ls`

Source Space ROS and demo packages:

```bash
source ${SPACEROS_DIR}/install/setup.bash
source ~/demos_ws/install/setup.bash
```

Run the BT Manager:

```bash
ros2 launch mars_rover_bt_manager mars_rover_bt_manager_launch.py
```

To simulate the runtime conditions, open a new terminal as before and publish runtime data by using ROS2 topics:

```bash
ros2 topic pub --once /condition_update std_msgs/msg/String "{data: 'OnDust'}"
```

or

```bash
ros2 topic pub --once /condition_update std_msgs/msg/String "{data: 'OnRocks'}"
```

### Run the uncertainty-aware BT

Run the `execute_mission.sh` script to send the uncertainty-aware BT to the BT Manager and start its execution:

```bash
./execute_mission.sh <container-name>
```

### Addition or update of alternatives

To add new alternatives for the navigation adaptable node, add a new folder within `bt-generator/resource/navigation` folder and add the xml file of the alternative therein.
Update the `fretRequirements.json` file inside the `bt-generaotr/mission` folder with the new FRETISH requirements.

Run the `update_alternatives.sh` file to update the BT manager:

```bash
./update_alternatives.sh <container-name>
```

The robot will update its mission or start executing it.

> [!NOTE]
> To update the fretRequirements.json file, [FRET](https://github.com/NASA-SW-VnV/fret) is required.
