#!/usr/bin/env python
# -*- coding: utf-8 -*-


from rqt_gui_py.plugin import Plugin
from .tf_broadcaster_widget import TFBroadcasterWidget


class TFBroadcaster(Plugin):
    """
    テンプレ通り
    """

    def __init__(self, context):
        super(TFBroadcaster, self).__init__(context)
        self.setObjectName('TFBroadcaster')
        self._widget = TFBroadcasterWidget(self)
        self._widget.start()
        context.add_widget(self._widget)

    def save_settings(self, plugin_settings, instance_settings):
        self._widget.save_settings(plugin_settings, instance_settings)

    def restore_settings(self, plugin_settings, instance_settings):
        self._widget.restore_settings(plugin_settings, instance_settings)

    def shutdown_plugin(self):
        self._widget.shutdown_plugin()
