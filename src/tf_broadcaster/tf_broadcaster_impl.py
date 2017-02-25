#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import rospy
import tf_broadcaster_widget_utils as widget_utils

from geometry_msgs.msg import TransformStamped, Vector3, Quaternion
from tf2_msgs.msg import TFMessage
from tf.transformations import euler_from_quaternion, quaternion_from_euler

DEFAULT_NODE_NAME = 'tf_publisher'


class TFBroadcasterImpl(object):
    def __init__(self, frame_id='parent_frame', child_frame_id='child_frame'):
        self._static_tf_pub = rospy.Publisher("/tf_static", TFMessage, queue_size=100, latch=True)
        self._tf_pub = rospy.Publisher("/tf", TFMessage, queue_size=1)

        self._tf_stamped = TransformStamped()
        self._init_tf_stamped(frame_id, child_frame_id)

        self._status = widget_utils.Status.stop
        self._is_published_static_tf = False

    def _init_tf_stamped(self, frame_id, child_frame_id):
        self._tf_stamped.header.stamp = rospy.Time.now()
        self._tf_stamped.header.frame_id = frame_id
        self._tf_stamped.child_frame_id = child_frame_id
        self._tf_stamped.transform.translation = Vector3(x=0.0, y=0.0, z=0.0)
        self._tf_stamped.transform.rotation = Quaternion(x=0.0, y=0.0, z=0.0, w=1.0)

    def set_frames(self, frame_id, child_frame_id):
        self.set_frame_id(frame_id)
        self.set_child_frame_id(child_frame_id)

    def set_frame_id(self, frame_id):
        self._tf_stamped.header.frame_id = frame_id

    def set_child_frame_id(self, child_frame_id):
        self._tf_stamped.child_frame_id = child_frame_id

    def set_position(self, x, y, z):
        self._tf_stamped.transform.translation = Vector3(x=x, y=y, z=z)

    def set_orientation(self, roll, pitch, yaw, is_rad=True):
        if is_rad is False:
            roll, pitch, yaw = math.radians(roll), math.radians(pitch), math.radians(yaw)
        q = quaternion_from_euler(roll, pitch, yaw)
        self._tf_stamped.transform.rotation = Quaternion(x=q[0], y=q[1], z=q[2], w=q[3])

    def set_status(self, status):
        self._status = status

    def set_stop_status(self):
        self._status = widget_utils.Status.stop

    def set_static_tf_status(self):
        self._status = widget_utils.Status.static_tf

    def set_tf_status(self):
        self._status = widget_utils.Status.tf

    def broadcast_tf(self):
        self._tf_stamped.header.stamp = rospy.Time.now()

        if self._status == widget_utils.Status.stop:
            self._is_published_static_tf = False

        elif self._status == widget_utils.Status.tf:
            self._is_published_static_tf = False
            self._tf_pub.publish(TFMessage([self._tf_stamped]))

        elif self._status == widget_utils.Status.static_tf:
            if self._is_published_static_tf is not True:
                self._is_published_static_tf = True
                self._static_tf_pub.publish([self._tf_stamped])


# --------------------------------------------
if __name__ == '__main__':
    rospy.init_node(DEFAULT_NODE_NAME, anonymous=True)
    rate_mgr = rospy.Rate(100)  # Hz

    tf_publisher = TFBroadcasterImpl(frame_id='root', child_frame_id='oculus')

    roll = 0.0
    while not rospy.is_shutdown():
        roll += 1.0
        tf_publisher.set_orientation(roll % 360 - 180, 0.0, 0.0, is_rad=False)
        tf_publisher.broadcast_tf()
        rate_mgr.sleep()
