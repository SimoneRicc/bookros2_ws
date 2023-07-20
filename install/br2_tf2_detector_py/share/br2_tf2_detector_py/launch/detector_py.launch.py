# Copyright 2021 Intelligent Robotics Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    detector_py_cmd = Node(package='br2_tf2_detector_py',
                        executable='obstacle_detector_node',
                        output='screen',
                        parameters=[{
                            'use_sim_time': True
                        }],
                        remappings=[
                            ('input_scan', '/scan_raw')
                        ])
    monitor_py_cmd = Node(package='br2_tf2_detector_py',
                        executable='obstacle_monitor_node',
                        output='screen',
                        parameters=[{
                            'use_sim_time': True
                        }])

    ld = LaunchDescription()
    ld.add_action(detector_py_cmd)
    ld.add_action(monitor_py_cmd)

    return ld
