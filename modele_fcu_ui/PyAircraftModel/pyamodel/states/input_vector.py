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

import math
import logging
from pyamodel import ivy
from pyamodel import require_ivy
from pyamodel.states.base import BaseStateVector
from pyamodel.states.base import float_setter


class InputVector(BaseStateVector):
    wind_bing_msg = "^WindComponent\sVWind=(\S+)\s+dirWind=(\S+)"
    dev_bing_msg = "^MagneticDeclination=(\S+)"

    def __init__(self):
        self.wind = {
            "value": 0.0,
            "direction": 0.0
        }
        self.magnetic_deviation = 0.0

    @require_ivy
    def subscribe(self):
        ivy.IvyBindMsg(lambda a, *larg: self.update_wind(larg[0], larg[1]),
                       self.wind_bing_msg)
        ivy.IvyBindMsg(lambda a, *arg: self.update_magnetic_deviation(arg[0]),
                       self.dev_bing_msg)

    def update_wind(self, value, direction):
        try:
            self.wind.update({
                "value": float(value),
                "direction": float(direction)
            })
        except TypeError:
            logging.error("WindComponent msg is not well formated")

    @float_setter
    def update_magnetic_deviation(self, value):
        self.magnetic_deviation = value

    def get_wind_components(self):
        value, direction = self.wind["value"], self.wind["direction"]
        return (value * math.cos(direction + math.pi),
                value * math.sin(direction + math.pi))

    def get_magnetic_deviation(self):
        return self.magnetic_deviation

    def reset(self):
        self.wind = {
            "value": 0.0,
            "direction": 0.0
        }
        self.magnetic_deviation = 0.0
