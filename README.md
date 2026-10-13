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

| Argument | Default | Description |
|---|---|---|
| `object_name` | `red` | Rigid body name. Also used as the ROS namespace. |
| `vrpn_server_ip` | `localhost` | IP address of the VRPN server. |
| `coordinate_system` | `vicon` | `vicon`: data is used as streamed. `optitrack`: converts Y-up to Z-up. |
| `remap` | `True` | Remap `raw_pose` to `remap_out_topic`. |
| `remap_out_topic` | `/mavros/vision_pose/pose` | Target topic for `raw_pose`. |

## Topics

Published under the namespace `/<object_name>/`:

| Topic | Type | Description |
|---|---|---|
| `raw_transform` | `geometry_msgs/TransformStamped` | Raw measured pose |
| `raw_pose` | `geometry_msgs/PoseStamped` | Raw measured pose |
| `estimated_transform` | `geometry_msgs/TransformStamped` | Filtered pose |
| `estimated_odometry` | `nav_msgs/Odometry` | Filtered pose and velocity |

The transform `vicon` → `<object_name>` is also published on `/tf`.

Check that data arrives:

```bash
ros2 topic hz /<object_name>/estimated_odometry
```

## Coordinate frame

If the motion capture software streams with Z up, keep the default `coordinate_system:=vicon`. If it streams with Y up (OptiTrack default), use `coordinate_system:=optitrack`. In both cases the ROS frame is right-handed with Z pointing up.

## Troubleshooting

- **No data:** check that the VRPN server is reachable (`ping <server_ip>`), that VRPN streaming is enabled, and that the rigid body name is correct.
- **Topic not visible after changing networks:** restart the ROS 2 daemon with `ros2 daemon stop && ros2 daemon start`.
- **`VRPN Note: minor version number doesn't match`:** harmless.

## License

Apache 2.0, see [LICENSE](LICENSE).
