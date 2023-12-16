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

from PyQt5.QtCore import pyqtProperty, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtCore import QTimer
from PyQt5.QtQml import qmlRegisterSingletonType
from ivy.std_api import IvyGetApplicationList
from ivy.std_api import IvySendMsg, IvyBindMsg


class AircraftModelQObject(QObject):
    CMD_LINE_FORMAT = "nx=%.2f nz=%.2f p=%.2f"
    # define signals
    model_connected_sig = pyqtSignal(name='AircraftModelConnected')
    position_sig = pyqtSignal(name='AircraftPositionChanged')
    command_sig = pyqtSignal(name='AircraftCommandChanged')

    def __init__(self, parent=None):
        super(AircraftModelQObject, self).__init__(parent)

        # custom properties
        self._connected = False
        self._position = " N/A "
        self._command_vector = [0.0, 1.0, 0.0]  # nx, nz, p

        # ivy subscriptions
        IvyBindMsg(self.on_position_change,
                   "^StateVector\s+x=(\S+)\s+y=(\S+)\s+z=(\S+)\s+Vp=(\S+)\s+"
                   "fpa=(\S+)\s+psi=(\S+)")
        IvyBindMsg(lambda a, v: self.on_cmd_vector_change(0, v),
                   "^APNxControl nx=(\S+)")
        IvyBindMsg(lambda a, v: self.on_cmd_vector_change(1, v),
                   "^APNzControl nz=(\S+)")
        IvyBindMsg(lambda a, v: self.on_cmd_vector_change(2, v),
                   "^APLatControl rollRate=(\S+)")
        # init timer to verify state of aircrat model
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.verify_amodel)
        self._timer.start(1000)

    def verify_amodel(self):
        connected = "PyAircraftModel" in IvyGetApplicationList()
        if connected != self._connected:
            self._connected = connected
            self.model_connected_sig.emit()

    def on_position_change(self, agent, *largs):
        self._position = "X=%.1f Y=%.1f Z=%.1f" % (float(largs[0]),
                                                   float(largs[1]),
                                                   float(largs[2]))
        self._position += "\n vp=%.2f fpa=%.2f" % (float(largs[3]),
                                                   float(largs[4]))
        self.position_sig.emit()

    def on_cmd_vector_change(self, idx, value):
        self._command_vector[idx] = float(value)
        self.command_sig.emit()

    @pyqtProperty(str, notify=position_sig)
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @pyqtProperty(bool, notify=model_connected_sig)
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, connected):
        self._connected = connected

    @pyqtProperty(str, notify=command_sig)
    def command_vector(self):
        return self.CMD_LINE_FORMAT % tuple(self._command_vector)

    @pyqtSlot()
    def reset(self):
        IvySendMsg("AircraftModelReset")

    @pyqtSlot()
    def initialize(self):
        IvySendMsg("InitStateVector x=0 y=0 z=0 Vp=70 fpa=0 psi=0 phi=0")


def register_aircraft_model():
    qmlRegisterSingletonType(AircraftModelQObject, "fr.enac.AircraftModel",
                             1, 0, "AircraftModel",
                             lambda e, se: AircraftModelQObject())
