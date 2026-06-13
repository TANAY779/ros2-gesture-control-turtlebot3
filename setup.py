from setuptools import find_packages, setup

package_name = 'gesture_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
 	('share/' + package_name + '/launch',
        	['launch/gesture_control.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='tanay',
    maintainer_email='tanay@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'gesture_control = gesture_control.cmd_vel_publisher:main',
            'gesture_node = gesture_control.gesture_node:main',
        ],
    },
)
