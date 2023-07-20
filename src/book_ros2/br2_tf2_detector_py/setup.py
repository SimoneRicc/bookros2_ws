from setuptools import setup
import os
from glob import glob

package_name = 'br2_tf2_detector_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='simone',
    maintainer_email='simone.ricciardelli98@gmail.com',
    description='TF2 Detector using Python',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'obstacle_detector_node = br2_tf2_detector_py.ObstacleDetectorNode:main',
        	'obstacle_monitor_node = br2_tf2_detector_py.ObstacleMonitorNode:main',
        ],
    },
)
