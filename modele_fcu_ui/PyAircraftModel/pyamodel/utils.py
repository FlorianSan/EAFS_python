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

import logging
from math import pi

# conversion
FEET2M = 0.3048;
FPM2MS = FEET2M/60.0;
FL2M = 100.0*FEET2M;
NM2M = 1852.0;
KTS2MS = 1852.0/3600.0;
DEG2RAD = pi/180.0;


def saturate(val, val_min, val_max):
    return max(val_min, min(val, val_max)) 


def modulo_min_max(x, val_min, val_max):
    assert val_min < val_max

    y = x
    mod = val_max - val_min
    while y > val_max:
        y = y - mod
    while y <= val_min:
        y = y + mod

    return y


# vp2vi
# Vp: vitesse propre, m/s
# h: altitude, m
# Vi: vitesse indiquee, m/s
def vp2vi(vp, h):
    return vp - h*0.5/FL2M*KTS2MS  # Vi = Vp - FL/2


def vi2vp(vi, h):
    return vi + h*0.5/FL2M*KTS2MS  # Vp = Vi + FL/2


def limit_vp(vp):
    if vp < 1e-6:
        logging.warning("Low speed (limited to 1e-6 m/s")
        return 1e-6
    return vp


