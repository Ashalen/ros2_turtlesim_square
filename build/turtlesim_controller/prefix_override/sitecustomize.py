import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ashalen/ros2_projects/project2_turtlesim/install/turtlesim_controller'
