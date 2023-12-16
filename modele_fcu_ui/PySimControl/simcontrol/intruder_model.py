# ivy-simulator-control, a simple gui to control mini aircraft simulator
# Copyright (C) 2019 Mickael Royer <mickael.royer@enac.fr>
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


class IntruderModelQObject(QObject):
    # define signals
    model_connected_sig = pyqtSignal(name='IntruderModelConnected')
    position_sig = pyqtSignal(name='IntruderPositionChanged')

    def __init__(self, parent=None):
        super(IntruderModelQObject, self).__init__(parent)

        # custom properties
        self._connected = False
        self._position = " N/A "

        # ivy subscriptions
        IvyBindMsg(self.on_position_change,
                   "^IntruStateVector\s+x=(\S+)\s+y=(\S+)\s+z=(\S+)\s+"
                   "Vp=(\S+)\s+fpa=(\S+)\s+psi=(\S+)")
        # init timer to verify state of aircrat model
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.verify_model)
        self._timer.start(1000)

    def verify_model(self):
        connected = "PyAircraftModel" in IvyGetApplicationList()
        if connected != self._connected:
            self._connected = connected
            self.model_connected_sig.emit()

    def on_position_change(self, agent, *largs):
        self._position = "X=%.1f Y=%.1f Z=%.1f" % (float(largs[0]),
                                                   float(largs[1]),
                                                   float(largs[2]))
        self._position += " Vp=%.2f Psi=%.2f" % (float(largs[3]),
                                                   float(largs[5]))
        self.position_sig.emit()

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

    @pyqtSlot()
    def reset(self):
        IvySendMsg("IntruderModelReset")

    @pyqtSlot(str, str, str, str, str)
    def setPosition(self, x, y, z, vp, psi):
        IvySendMsg(
            "SetIntruStateVector x={} y={} z={} Vp={} "
            "fpa=0 psi={} phi=0".format(
                x, y, z, vp, psi
            ))

    @pyqtSlot(str, str, str, str)
    def initConflictPosition(self, tcpa, dcpa, r0, delta_trk):
        IvySendMsg(
            "SetIntruConflictPos tcpa={} dcpa={} r0={} dtrack={}".format(
                tcpa, dcpa, r0, delta_trk
            ))


def register_intruder_model():
    qmlRegisterSingletonType(
        IntruderModelQObject, "fr.enac.IntruderModel", 1, 0, "IntruderModel",
        lambda e, se: IntruderModelQObject())
