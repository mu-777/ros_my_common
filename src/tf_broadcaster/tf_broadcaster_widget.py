#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os, time

import rospkg
import rospy
from rospy.exceptions import ROSException

from python_qt_binding import loadUi
from python_qt_binding.QtCore import Qt, QTimer, Signal, Slot
from python_qt_binding.QtWidgets import QWidget


from .tf_broadcaster_impl import TFBroadcasterImpl
from .tf_broadcaster_widget_utils import SliderSpinboxInputWidgetSet, FrameIDInputWidgetSet, StatusInputWidgetSet

FRAME_ID = 'parent_frame_id'
CHILD_FRAME_ID = 'child_frame_id'
POS_MAX_VALUE = 10.0
POS_MIN_VALUE = -10.0
ORI_MAX_VALUE = 180.0
ORI_MIN_VALUE = -180.0


class TFBroadcasterWidget(QWidget):
    def __init__(self, widget):
        super(TFBroadcasterWidget, self).__init__()
        rospkg_pack = rospkg.RosPack()
        ui_file = os.path.join(rospkg_pack.get_path('my_common'), 'resource', 'TFBroadcaster.ui')
        loadUi(ui_file, self)

        self._frame_id, self._child_frame_id = FRAME_ID, CHILD_FRAME_ID
        self._tf_manager = TFBroadcasterImpl(self._frame_id, self._child_frame_id)

        self.setup_ui()

        self._updateTimer = QTimer(self)
        self._updateTimer.timeout.connect(self.timeout_callback)

    def setup_ui(self):
        self._status_widget = StatusInputWidgetSet(self.qt_stop_radiobtn,
                                                   self.qt_static_tf_radiobtn,
                                                   self.qt_tf_radiobtn,
                                                   self._tf_manager.set_stop_status,
                                                   self._tf_manager.set_static_tf_status,
                                                   self._tf_manager.set_tf_status)

        self._frame_id_widget = FrameIDInputWidgetSet(self.qt_frame_id_lineedit,
                                                      self.qt_frame_id_update_btn,
                                                      self._frame_id,
                                                      self._tf_manager.set_frame_id)

        self._child_frame_id_widget = FrameIDInputWidgetSet(self.qt_child_frame_id_lineedit,
                                                            self.qt_child_frame_id_update_btn,
                                                            self._child_frame_id,
                                                            self._tf_manager.set_child_frame_id)

        self._x_widget = SliderSpinboxInputWidgetSet(self.qt_x_slider,
                                                     self.qt_x_spinbox,
                                                     self.qt_x_btn,
                                                     0.0, POS_MAX_VALUE, POS_MIN_VALUE)
        self._y_widget = SliderSpinboxInputWidgetSet(self.qt_y_slider,
                                                     self.qt_y_spinbox,
                                                     self.qt_y_btn,
                                                     0.0, POS_MAX_VALUE, POS_MIN_VALUE)
        self._z_widget = SliderSpinboxInputWidgetSet(self.qt_z_slider,
                                                     self.qt_z_spinbox,
                                                     self.qt_z_btn,
                                                     0.0, POS_MAX_VALUE, POS_MIN_VALUE)

        self._roll_widget = SliderSpinboxInputWidgetSet(self.qt_roll_slider,
                                                        self.qt_roll_spinbox,
                                                        self.qt_roll_btn,
                                                        0.0, ORI_MAX_VALUE, ORI_MIN_VALUE)
        self._pitch_widget = SliderSpinboxInputWidgetSet(self.qt_pitch_slider,
                                                         self.qt_pitch_spinbox,
                                                         self.qt_pitch_btn,
                                                         0.0, ORI_MAX_VALUE, ORI_MIN_VALUE)
        self._yaw_widget = SliderSpinboxInputWidgetSet(self.qt_yaw_slider,
                                                       self.qt_yaw_spinbox,
                                                       self.qt_yaw_btn,
                                                       0.0, ORI_MAX_VALUE, ORI_MIN_VALUE)


    def start(self):
        self._tf_manager.set_frames(self._frame_id, self._child_frame_id)
        self._updateTimer.start(10)  # loop rate[ms]

    def stop(self):
        self._updateTimer.stop()

    def timeout_callback(self):
        self._tf_manager.set_position(self._x_widget.value, self._y_widget.value, self._z_widget.value)
        self._tf_manager.set_orientation(self._roll_widget.value,
                                         self._pitch_widget.value,
                                         self._yaw_widget.value,
                                         is_rad=False)
        self._tf_manager.broadcast_tf()

    # override
    def save_settings(self, plugin_settings, instance_settings):
        self._frame_id = self._frame_id_widget.str
        self._child_frame_id = self._child_frame_id_widget.str
        instance_settings.set_value('frame_ids', (self._frame_id, self._child_frame_id))

    # override
    def restore_settings(self, plugin_settings, instance_settings):
        frames = instance_settings.value('frame_ids')
        try:
            self._frame_id, self._child_frame_id = frames
            self._frame_id_widget.update(self._frame_id)
            self._child_frame_id_widget.update(self._child_frame_id)
        except Exception:
            self._frame_id, self._child_frame_id = FRAME_ID, CHILD_FRAME_ID

    # override
    def shutdown_plugin(self):
        self.stop()

