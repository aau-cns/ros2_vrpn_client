from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    object_name = LaunchConfiguration('object_name').perform(context)
    remap = LaunchConfiguration('remap').perform(context).lower() in ['true', '1']
    remap_out_topic = LaunchConfiguration('remap_out_topic').perform(context)
    coordinate_system = LaunchConfiguration('coordinate_system').perform(context)
    vrpn_server_ip = LaunchConfiguration('vrpn_server_ip').perform(context)

    remappings = []
    if remap:
        remappings.append((
            f'/{object_name}/raw_pose',
            remap_out_topic
        ))

    return [
        Node(
            package='ros_vrpn',
            executable='ros_vrpn_client',
            namespace=object_name,
            parameters=[{
                'vrpn_server_ip': vrpn_server_ip,
                'vrpn_coordinate_system': coordinate_system,
                'timestamping_system': 'ros',
                'object_name': object_name,
                'verbose': True,
                'translational_estimator/kp': 0.5,
                'translational_estimator/kv': 0.5,
                'rotational_estimator/orientation_estimate_initial_covariance': 100.0,
                'rotational_estimator/rate_estimate_initial_covariance': 100.0,
                'rotational_estimator/orientation_process_covariance': 0.000002,
                'rotational_estimator/rate_process_covariance': 10.0,
                'rotational_estimator/orientation_measurementCovariance': 0.001,
                'rotational_estimator/outlier_rejection_method': 'mahalanobis_distance',
                'rotational_estimator/outlier_rejection_mahalanobis_threshold': 4.0,
                'rotational_estimator/outlier_rejection_subsequent_threshold_degrees': 30.0,
                'rotational_estimator/outlier_rejection_subsequent_maximum_count': 50,
                'rotational_estimator/output_minimal_quaternions': False,
            }],
            remappings=remappings
        )
    ]

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('object_name', default_value='red'),
        DeclareLaunchArgument('remap', default_value='True'),
        DeclareLaunchArgument('remap_out_topic', default_value='/mavros/vision_pose/pose'),
        DeclareLaunchArgument('coordinate_system', default_value='vicon'),
        DeclareLaunchArgument('vrpn_server_ip', default_value='localhost'),
        OpaqueFunction(function=launch_setup)
    ])
