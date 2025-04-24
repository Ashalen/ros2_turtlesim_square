from setuptools import find_packages, setup

package_name = 'turtlesim_controller'

setup(
    name=package_name,
    version='0.0.1',  # Updated version to indicate progress
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ashalen',
    maintainer_email='ashalen.govender@gmail.com',
    description='A ROS 2 package to control turtlesim and draw a square pattern.',
    license='Apache License 2.0', 
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'draw_square = turtlesim_controller.draw_square:main'
        ],
    },
)
