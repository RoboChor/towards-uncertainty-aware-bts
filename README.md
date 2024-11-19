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
|   README.md               # This file
└---mission-specification
|   |   adaptable_bt.xml    # Adaptable BT of the mission
|   |   al1.xml             # Navigation alternative 1 (Dust)
|   |   al2.xml             # Navigation alternative 1 (Rocks)
|   |   requirements.txt    # FRETISH conditions specification
|   └---imgs                # Mission BT images
└---bt_generator    
└---fretish_syntax
```

## Instructions
### Pre-requisites
- Docker

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

Simulate the runtime conditions by using ROS2 topics:

```bash
ros2 topic pub --once /condition_update std_msgs/msg/String "{data: 'OnDust'}"
```

or

```bash
ros2 topic pub --once /condition_update std_msgs/msg/String "{data: 'OnRocks'}"
```


### Compile and run the uncertainty-aware BT

Run the `execute_mission.sh` script to send the uncertainty-aware BT to the BT Manager and start its execution. The rover's behavior will follow the simulated conditions.
