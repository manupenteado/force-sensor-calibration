import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import numpy as np

class SubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber_node')
        self.subscription = self.create_subscription(
            Float64MultiArray,
            'measurement',
            self.callback,
            10
        )

    def callback(self, msg):
        np.savetxt("400g-5.txt",abs(np.array(msg.data)), fmt='%f')
        self.get_logger().info("Dados salvos em dados.txt")

def main(args=None):
    rclpy.init(args=args)
    subscriber_node = SubscriberNode()
    try:
        rclpy.spin(subscriber_node)
    except KeyboardInterrupt:
        pass
    finally:
        subscriber_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
