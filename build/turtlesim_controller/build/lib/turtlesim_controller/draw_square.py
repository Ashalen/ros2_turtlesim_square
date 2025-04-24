#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class DrawSquareNode(Node):
    def __init__(self):
        super().__init__('draw_square')
        
        # Publisher to send velocity commands
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # Parameters for speed and side length (tuned for TurtleSim)
        self.declare_parameter('linear_speed', 2.0)  # Increased from 1.0
        self.declare_parameter('angular_speed', 1.0)  # Reduced from 1.57
        self.declare_parameter('side_duration', 2.0)  # Seconds to move each side
        self.declare_parameter('turn_duration', 1.57) # Seconds for 90° turn (π/2)
        
        self.linear_speed = self.get_parameter('linear_speed').value
        self.angular_speed = self.get_parameter('angular_speed').value
        self.side_duration = self.get_parameter('side_duration').value
        self.turn_duration = self.get_parameter('turn_duration').value

        # State variables
        self.current_side = 0
        self.state = 'MOVE_FORWARD'
        self.start_time = self.get_clock().now()

        # Use a faster timer for smoother control
        self.timer = self.create_timer(0.05, self.move_square)  # 20Hz control loop

    def move_square(self):
        """Move the turtle in a square pattern with precise timing."""
        cmd = Twist()
        current_time = self.get_clock().now()
        elapsed_time = (current_time - self.start_time).nanoseconds / 1e9

        if self.state == 'MOVE_FORWARD':
            # Move straight
            cmd.linear.x = self.linear_speed
            cmd.angular.z = 0.0
            self.get_logger().info(f"Moving forward (Side {self.current_side + 1})", throttle_duration_sec=1.0)
            
            if elapsed_time >= self.side_duration:
                self.state = 'TURN'
                self.start_time = current_time
                self.get_logger().info(f"Completed side {self.current_side + 1}. Preparing to turn.")

        elif self.state == 'TURN':
            # Turn in place
            cmd.linear.x = 0.0
            cmd.angular.z = self.angular_speed
            self.get_logger().info(f"Turning (Side {self.current_side + 1})", throttle_duration_sec=1.0)
            
            if elapsed_time >= self.turn_duration:
                self.state = 'MOVE_FORWARD'
                self.start_time = current_time
                self.current_side += 1
                
                if self.current_side >= 4:
                    self.get_logger().info("Square completed! Stopping turtle.")
                    self.stop_turtle()
                    self.timer.cancel()
                    return

        self.publisher.publish(cmd)

    def stop_turtle(self):
        """Stop the turtle by publishing zero velocities."""
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.publisher.publish(cmd)
        self.get_logger().info("Turtle stopped.")

def main(args=None):
    rclpy.init(args=args)
    node = DrawSquareNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
        node.stop_turtle()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()