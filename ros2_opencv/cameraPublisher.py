#######
# PUBLISHING & SUBSCRIBING
#######

import cv2
import rclpy
from sensor_msgs.msg import Image
from rclpy.node import Node
from cv_bridge import CvBridge

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

class PublisherNodeClass(Node):

    def __init__(self):
        super().__init__('publisher_node')

        self.cameraDeviceNumber=0
        self.camera = self.create_subscription(Image,'/camera/image_raw',self.timer_callbackFunction,10)
        # self.camera = cv2.VideoCapture(0)
        self.bridgeObject = CvBridge()
        self.topicNameFrames = 'face_eye_detection'
        self.queueSize = 20
        self.publisher = self.create_publisher(Image, self.topicNameFrames, self.queueSize)
        # self.periodCommunication = 0.02
        # self.timer = self.create_timer(self.periodCommunication, self.timer_callbackFunction)
        # self.i = 0
    
    def timer_callbackFunction(self, msg):

        # success, frame = self.camera.read()
        # frame = cv2.resize(frame, (1080, 720), interpolation=cv2.INTER_CUBIC)

        # if success == True:
        #     ROS2ImageMessage = self.bridgeObject.cv2_to_imgmsg(frame, 'bgr8')
        #     self.publisher.publish(ROS2ImageMessage)
        
        # self.get_logger().info('Publishing image number %d' % self.i)
        # self.i += 1
        frame = self.bridgeObject.imgmsg_to_cv2(msg, 'bgr8')    
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
            roi_gray = gray[y : y + h, x : x + w]
            roi_color = frame[y : y + h, x : x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 5)
        

        ROS2ImageMessage = self.bridgeObject.cv2_to_imgmsg(frame, 'bgr8')               
        self.publisher.publish(ROS2ImageMessage)

def main(args=None):
    rclpy.init(args=args)
    publisherObject = PublisherNodeClass()
    rclpy.spin(publisherObject)
    publisherObject.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()


#######
# ONLY PUBLISHING
#######

# import cv2
# import rclpy
# from sensor_msgs.msg import Image
# from rclpy.node import Node
# from cv_bridge import CvBridge

# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# class PublisherNodeClass(Node):

#     def __init__(self):
#         super().__init__('publisher_node')

#         self.cameraDeviceNumber=0
#         self.camera = cv2.VideoCapture(self.cameraDeviceNumber)
#         self.bridgeObject = CvBridge()
#         self.topicNameFrames = 'face_eye_detection'
#         self.queueSize = 20
#         self.publisher = self.create_publisher(Image, self.topicNameFrames, self.queueSize)
#         self.periodCommunication = 0.02
#         self.timer = self.create_timer(self.periodCommunication, self.timer_callbackFunction)
#         self.i = 0
    
#     def timer_callbackFunction(self):

#         # success, frame = self.camera.read()
#         # frame = cv2.resize(frame, (1080, 720), interpolation=cv2.INTER_CUBIC)

#         # if success == True:
#         #     ROS2ImageMessage = self.bridgeObject.cv2_to_imgmsg(frame, 'bgr8')
#         #     self.publisher.publish(ROS2ImageMessage)
        
#         # self.get_logger().info('Publishing image number %d' % self.i)
#         # self.i += 1
#         success, frame = self.camera.read()
#         if success == True:    
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = face_cascade.detectMultiScale(gray, 1.2, 5)

#             for (x, y, w, h) in faces:
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
#                 roi_gray = gray[y : y + h, x : x + w]
#                 roi_color = frame[y : y + h, x : x + w]
#                 eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
#                 for (ex, ey, ew, eh) in eyes:
#                     cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 5)
            

#             ROS2ImageMessage = self.bridgeObject.cv2_to_imgmsg(frame, 'bgr8')               
#             self.publisher.publish(ROS2ImageMessage)

# def main(args=None):
#     rclpy.init(args=args)
#     publisherObject = PublisherNodeClass()
#     rclpy.spin(publisherObject)
#     publisherObject.destroy_node()
#     rclpy.shutdown()
#     cv2.destroyAllWindows()

# if __name__ == '__main__':
#     main()



#########
# EXAMPLE (SUBSCRIBING & PUBLISHING)
#########


# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge
# import cv2

# class ImageProcessor(Node):
#     def __init__(self):
#         super().__init__('image_processor')

#         # Subscriber to raw image
#         self.subscription = self.create_subscription(
#             Image,
#             '/camera/image_raw',  # Change if your topic is different
#             self.image_callback,
#             10)
        
#         # Publisher for processed image
#         self.publisher = self.create_publisher(Image, '/camera/processed', 10)

#         # Bridge to convert ROS <-> OpenCV
#         self.bridge = CvBridge()

#     def image_callback(self, msg):
#         try:
#             # Convert ROS Image to OpenCV format
#             cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

#             # Example processing: Convert to grayscale
#             gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

#             # Optional: Display processed image
#             # cv2.imshow("Processed Image", gray_image)
#             # cv2.waitKey(1)

#             # Convert processed OpenCV image back to ROS Image
#             processed_msg = self.bridge.cv2_to_imgmsg(gray_image, encoding='mono8')

#             # Publish the processed image
#             self.publisher.publish(processed_msg)

#         except Exception as e:
#             self.get_logger().error(f"Error processing image: {e}")

# def main(args=None):
#     rclpy.init(args=args)
#     node = ImageProcessor()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()
#     cv2.destroyAllWindows()

# if __name__ == '__main__':
#     main()

            