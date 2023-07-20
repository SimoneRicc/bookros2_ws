import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped

class ObstacleDetectorNode(Node):
    def __init__(self):
        super().__init__('obstacle_detector_node')
        self.detection_tf = TransformStamped()
        self.scan_sub_ = self.create_subscription(
            LaserScan,
            'input_scan',  # Replace 'scan_topic' with the actual topic name for LaserScan messages
            self.scan_callback,
            10  # Adjust the queue size as needed
        )
        self.tf_broadcaster_ = StaticTransformBroadcaster(self)

    def scan_callback(self, msg):
        dist = msg.ranges[len(msg.ranges)//2]
        if dist != float('inf'):
            self.detection_tf.header = msg.header
            self.detection_tf.child_frame_id = 'detected_obstacles'
            self.detection_tf.transform.translation.x = dist

            self.tf_broadcaster_.sendTransform(self.detection_tf)
        

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleDetectorNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
