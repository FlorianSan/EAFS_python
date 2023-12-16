# PyAircraftModel, a simplistc aircraft model for simulator based on ivy
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

from pyamodel import ivy
from pyamodel import require_ivy
from pyamodel.states.base import float_setter
from pyamodel.states.base import BaseStateVector


class _CommandVector(BaseStateVector):

    def __init__(self):
        self.nz = 1.0
        self.nx = 0.0
        self.p = 0.0

    @float_setter
    def set_nx(self, nx):
        self.nx = nx

    @float_setter
    def set_nz(self, nz):
        self.nz = nz

    @float_setter
    def set_p(self, p):
        self.p = p

    def get_nx(self):
        return self.nx

    def get_nz(self):
        return self.nz

    def get_p(self):
        return self.p

    def reset(self):
        self.nz = 1.0
        self.nx = 0.0
        self.p = 0.0


class AircraftCommandVector(_CommandVector):
    nx_msg = "^APNxControl\s+nx=(\S+)"
    nz_msg = "^APNzControl\s+nz=(\S+)"
    p_msg = "^APLatControl\s+rollRate=(\S+)"

    @require_ivy
    def subscribe(self):
        ivy.IvyBindMsg(lambda a, *larg: self.set_nz(larg[0]), self.nz_msg)
        ivy.IvyBindMsg(lambda a, *larg: self.set_nx(larg[0]), self.nx_msg)
        ivy.IvyBindMsg(lambda a, *larg: self.set_p(larg[0]), self.p_msg)


class IntruderCommandVector(_CommandVector):
    nx_msg = "^IPNxControl\s+nx=(\S+)"
    nz_msg = "^IPNzControl\s+nz=(\S+)"
    p_msg = "^IPLatControl\s+rollRate=(\S+)"

    @require_ivy
    def subscribe(self):
        ivy.IvyBindMsg(lambda a, *larg: self.set_nz(larg[0]), self.nz_msg)
        ivy.IvyBindMsg(lambda a, *larg: self.set_nx(larg[0]), self.nx_msg)
        ivy.IvyBindMsg(lambda a, *larg: self.set_p(larg[0]), self.p_msg)
