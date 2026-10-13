# ros2_vrpn_client

ROS 2 client for motion capture systems (OptiTrack, Vicon) that stream over [VRPN](https://github.com/vrpn/vrpn). It publishes the pose and velocity of tracked rigid bodies as ROS 2 topics and TF.

Based on [ethz-asl/ros_vrpn_client](https://github.com/ethz-asl/ros_vrpn_client) and its ROS 2 port [pascalau/ros_vrpn_client](https://github.com/pascalau/ros_vrpn_client/tree/ros2).

## Installation

Requirements: Ubuntu 24.04, ROS 2 Jazzy. The first build downloads the VRPN library, so an internet connection is needed.

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/aau-cns/ros2_vrpn_client.git
git clone -b ros2 https://github.com/pascalau/vrpn_catkin.git vrpn_vendor

cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -y
colcon build --symlink-install --packages-up-to ros_vrpn
source install/setup.bash
```

The ROS 2 package name is `ros_vrpn`.

## Usage

```bash
ros2 launch ros_vrpn optitrack_dronehall.launch.py object_name:=<rigid_body_name> vrpn_server_ip:=<server_ip>
```

`object_name` must match the rigid body name in the motion capture software exactly (case-sensitive).

## License

Apache 2.0, see [LICENSE](LICENSE).
