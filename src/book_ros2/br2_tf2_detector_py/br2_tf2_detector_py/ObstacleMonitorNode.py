import rclpy
from rclpy.node import Node
from rclpy.timer import Timer
from rclpy.time import Time
from tf2_ros import Buffer, TransformException
from tf2_ros import TransformListener, Time
from visualization_msgs.msg import Marker
from geometry_msgs.msg import TransformStamped, Point
import math


class ObstacleMonitorNode(Node):
    def __init__(self):
        super().__init__('obstacle_monitor_node')
        self.timer_ = self.create_timer(0.5, self.control_cycle)  # Timer with a 1-second interval
        self.tf_buffer_ = Buffer(self.get_clock())  # Use the node's clock for time resolution
        self.tf_listener_ = TransformListener(self.tf_buffer_, self)
        self.marker_pub_ = self.create_publisher(Marker, 'obstacle_marker', 10)
        self.robot2obstacle = TransformStamped()

        self.obstacle_arrow = Marker()
        self.start = Point()
        self.end = Point()

    def control_cycle(self):
        try:
            self.robot2obstacle = self.tf_buffer_.lookup_transform('base_footprint','detected_obstacles',Time())
        except TransformException as ex:
            self.get_logger().warn('Obstacle transform not found: %s' % ex)
            return

        x = self.robot2obstacle.transform.translation.x
        y = self.robot2obstacle.transform.translation.y
        z = self.robot2obstacle.transform.translation.z
        theta = math.atan2(y,x)

        self.get_logger().info(f'Obstacle detected at ({x} m, {y} m, {z} m) = {theta} rads')

        self.obstacle_arrow.header.frame_id = 'base_footprint'
        self.obstacle_arrow.header.stamp = self.get_clock().now().to_msg()
        self.obstacle_arrow.type = Marker.ARROW
        self.obstacle_arrow.action = Marker.ADD
        self.obstacle_arrow.lifetime.sec = 1

        self.start.x = 0.0
        self.start.y = 0.0
        self.start.z = 0.0

        self.end.x = x
        self.end.y = y
        self.end.z = z
    
        self.obstacle_arrow.points = [self.start,self.end]
        
        self.obstacle_arrow.color.r = 1.0
        self.obstacle_arrow.color.g = 0.0
        self.obstacle_arrow.color.b = 0.0
        self.obstacle_arrow.color.a = 1.0

        self.obstacle_arrow.scale.x = 0.02
        self.obstacle_arrow.scale.y = 0.1
        self.obstacle_arrow.scale.z = 0.1

        self.marker_pub_.publish(self.obstacle_arrow    )


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleMonitorNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
        