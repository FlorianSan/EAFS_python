# ivy-simulator-control, a simple gui to control mini aircraft simulator
# Copyright (C) 2016 Mickael Royer <mickael.royer@enac.fr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from collections import deque
from PyQt5.QtCore import pyqtProperty, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import QTimer
from PyQt5.QtQml import qmlRegisterSingletonType
from ivy.std_api import IvyGetApplicationList, IvyGetApplication
from ivy.std_api import IvySendMsg, IvyBindMsg, IvyUnBindMsg


class IvyQObject(QObject):
    __instance = None
    LOG_MAX_LINES = 100
    # define signals
    ivy_log_sig = pyqtSignal(name='ivyLogChanged')
    applications_sig = pyqtSignal(name='applicationListChanged')
    bindings_sig = pyqtSignal(name='bindingListChanged')

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self, parent=None):
        super(IvyQObject, self).__init__(parent)

        # custom properties
        self._log_lines = deque(maxlen=self.LOG_MAX_LINES)
        self._log = ""
        self._log_recording = False
        self._log_binding_id = None
        # models used to record the the application list and the bindings
        self._application_list = QStringListModel()
        self._binding_list = QStringListModel()

    @pyqtProperty(QStringListModel, notify=applications_sig)
    def application_list(self):
        return self._application_list

    def update_application_list(self):
        # this function is called from a worker thread
        # so use QTimer to update applications in the GUI thread
        QTimer.singleShot(0, self.update_applications_model)

    @pyqtSlot()
    def update_applications_model(self):
        self._application_list.setStringList(IvyGetApplicationList())
        self.applications_sig.emit()

    @pyqtProperty(QStringListModel, notify=bindings_sig)
    def binding_list(self):
        return self._binding_list

    @pyqtSlot(int)
    def update_bindings_list(self, current_row):
        if current_row == -1:
            return
        row_index = self._application_list.createIndex(current_row, 0)
        application_name = self._application_list.data(row_index, 0)
        client = IvyGetApplication(application_name)
        if client is not None:
            bindings = ["<strong>%d</strong>->'%s'" % (idx, r_exp)
                        for (idx, r_exp) in client.get_regexps()]
            self._binding_list.setStringList(bindings)
            self.bindings_sig.emit()

    @pyqtProperty(str, notify=ivy_log_sig)
    def log(self):
        return self._log

    @pyqtProperty(bool, notify=ivy_log_sig)
    def log_recording(self):
        return self._log_recording

    @log.setter
    def log(self, log):
        self._log = log

    @pyqtSlot(str)
    def send_msg(self, msg):
        if msg != "":
            IvySendMsg(msg)
            if self._log_recording:
                agent = "SimControl"
                if msg.startswith("Time"):
                    agent = "Clock"
                elif msg.startswith("FCU"):
                    agent = "Fcu"
                elif msg.startswith("SetIntru"):
                    agent = "Intruder"
                self.append_to_log(agent, msg)

    @pyqtSlot()
    def clear(self):
        self._log = ""
        self._log_lines = deque(maxlen=self.LOG_MAX_LINES)
        self.ivy_log_sig.emit()

    @pyqtSlot(bool)
    def record(self, active):
        if active and self._log_binding_id is None:
            self._log_binding_id = IvyBindMsg(
                self.append_to_log, "(.*)")
        elif not active and self._log_binding_id is not None:
            IvyUnBindMsg(self._log_binding_id)
            self._log_binding_id = None
        self._log_recording = active
        self.ivy_log_sig.emit()

    def append_to_log(self, agent, txt):
        self._log_lines.appendleft("<strong>%s</strong>: %s" % (agent, txt))
        self._log = "<br/>".join(self._log_lines)
        self.ivy_log_sig.emit()


def register_ivy_object():
    qmlRegisterSingletonType(IvyQObject, "fr.enac.IvyBus",
                             1, 0, "IvyBus",
                             lambda e, se: IvyQObject.getInstance())
