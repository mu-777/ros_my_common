#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math, numpy


class Status:
    stop = 1
    tf = 2
    static_tf = 3


class StatusInputWidgetSet:
    def __init__(self, qt_stop_radiobtn, qt_static_tf_radiobtn, qt_tf_radiobtn,
                 stop_toggled_callback, static_tf_toggled_callback, tf_toggled_callback):
        self._qt_stop_radiobtn = qt_stop_radiobtn
        self._qt_static_tf_radiobtn = qt_static_tf_radiobtn
        self._qt_tf_radiobtn = qt_tf_radiobtn
        self._stop_toggled_callback = stop_toggled_callback
        self._static_tf_toggled_callback = static_tf_toggled_callback
        self._tf_toggled_callback = tf_toggled_callback

        self.status = Status.stop
        self._qt_stop_radiobtn.setChecked(True)
        self._activate()

    def _activate(self):
        self._qt_stop_radiobtn.clicked.connect(self.stop_toggled)
        self._qt_static_tf_radiobtn.clicked.connect(self.static_tf_toggled)
        self._qt_tf_radiobtn.clicked.connect(self.tf_toggled)

    def stop_toggled(self, flag):
        if flag is True and self.status is not Status.stop:
            self.status = Status.stop
            self._stop_toggled_callback()

    def static_tf_toggled(self, flag):
        if flag is True and self.status is not Status.static_tf:
            self.status = Status.static_tf
            self._static_tf_toggled_callback()

    def tf_toggled(self, flag):
        if flag is True and self.status is not Status.tf:
            self.status = Status.tf
            self._tf_toggled_callback()


class FrameIDInputWidgetSet:
    def __init__(self, qt_lineedit, qt_update_btn, init_str, updated_callback):
        self._qt_lineedit = qt_lineedit
        self._qt_update_btn = qt_update_btn
        self.str = init_str
        self.updated_callback = updated_callback
        self._activate()

    def _activate(self):
        self._qt_lineedit.setText(self.str)
        self._qt_lineedit.textChanged.connect(self._lineedit_textChanged)
        self._qt_update_btn.clicked.connect(self._update_btn_clicked)

    def _lineedit_textChanged(self, str):
        self.str = str

    def _update_btn_clicked(self):
        self.updated_callback(self.str)

    def update(self, frame_id):
        self.str = frame_id
        self._qt_lineedit.setText(self.str)
        self.updated_callback(self.str)


class SliderSpinboxInputWidgetSet:
    def __init__(self, qt_slider, qt_spinbox, qt_reset_btn, init_value, max_value, min_value):
        self._qt_slider = qt_slider
        self._qt_spinbox = qt_spinbox
        self._qt_reset_btn = qt_reset_btn
        self._init_val = init_value
        self._max_val = max_value
        self._min_val = min_value
        self._slider_max_val = 100000.0  # See .ui

        self.value = self._init_val
        self._activate()

    def _activate(self):
        self._qt_slider.setValue(self._value2slider(self.value))
        self._qt_slider.valueChanged.connect(self._slider_valueChanged)
        self._qt_spinbox.setValue(self.value)
        self._qt_spinbox.valueChanged.connect(self._spinbox_valueChanged)
        self._qt_reset_btn.clicked.connect(self._reset_btn_clicked)

    def _slider2value(self, slider):
        return slider * (self._max_val - self._min_val) / self._slider_max_val + self._min_val

    def _value2slider(self, value):
        return self._slider_max_val * (value - self._min_val) / (self._max_val - self._min_val)

    def _slider_valueChanged(self, slider):
        self.value = self._slider2value(slider)
        self._qt_spinbox.setValue(self.value)

    def _spinbox_valueChanged(self, value):
        self.set_val(value)

    def _reset_btn_clicked(self):
        self.value = self._init_val
        self._qt_slider.setValue(self._value2slider(self.value))
        self._qt_spinbox.setValue(self.value)

    def set_val(self, value):
        self.value = value
        self._qt_slider.setValue(self._value2slider(self.value))
