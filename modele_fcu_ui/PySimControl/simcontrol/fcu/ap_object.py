# PyFcu, a simple fcu written in python
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

from PyQt5.QtCore import pyqtProperty, QObject, pyqtSignal
from PyQt5.QtQml import qmlRegisterSingletonType
from ivy.std_api import IvyBindMsg


class APQObject(QObject):
    sig = pyqtSignal(name='APStateChanged')

    def __init__(self, parent=None):
        super(APQObject, self).__init__(parent)
        self._activated = False
        # subscribe to ap1 message
        IvyBindMsg(self.on_ap_msg, "^FCUAP1 (.*)")

    def on_ap_msg(self, agent, *larg):
        self._activated = larg[0] == "on"
        self.sig.emit()

    @pyqtProperty(bool, notify=sig)
    def activated(self):
        return self._activated

    @activated.setter
    def activated(self, activate):
        self._activated = activate


def register_ap1_object():
    qmlRegisterSingletonType(APQObject, "fr.enac.AP1",
                             1, 0, "AP1",
                             lambda e, se: APQObject())
