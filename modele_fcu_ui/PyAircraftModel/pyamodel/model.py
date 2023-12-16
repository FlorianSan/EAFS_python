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
import math
from numpy import sign
from numpy import array
import sys
from pyamodel.states.input_vector import InputVector
from pyamodel.states.state_vector import AircraftStateVector
from pyamodel.states.state_vector import IntruderStateVector
from pyamodel.states.command_vector import AircraftCommandVector
from pyamodel.states.command_vector import IntruderCommandVector
from pyamodel import require_ivy
from pyamodel import ivy
from pyamodel.utils import modulo_min_max, NM2M, FEET2M, KTS2MS, DEG2RAD
from pyamodel.utils import vp2vi, limit_vp, saturate


class _Model(object):
    name = "unknown"
    time_msg = "^Time\s+t=(\S+)"
    reset_msg = ""

    def __init__(self):
        self.current_time = 0
        self.st_vector = None
        self.cmd_vector = None

    @require_ivy
    def run(self):
        ivy.IvyBindMsg(
            lambda a, t: self.update_position(t, update=True),
            self.time_msg)
        ivy.IvyBindMsg(lambda a: self.reset(), self.reset_msg)

    def reset(self):
        self.st_vector.reset()
        self.cmd_vector.reset()
        self.update_ui()

    def update_ui(self):
        pass

    def update_position(self, t, update=False):
        logging.debug("Update %s position for t=%s", self.name, t)
        try:
            t = float(t)
        except TypeError:
            logging.error("Time value has the wrong format: '%s'", t)
            return

        dt = t - self.current_time
        if dt > 0 and self.st_vector.initialized():
            state_vec = self.st_vector.to_array()
            new_state_vec = self.my_rk4(
                state_vec, self.current_time, dt, self.compute_position)
            # update psi value
            new_state_vec[5] = modulo_min_max(
                new_state_vec[5], 0.0, 2.0*math.pi)
            # gamma saturation
            new_state_vec[4] = saturate(
                new_state_vec[4], -3.0*DEG2RAD, 3.0*DEG2RAD)
            # vp saturation
            new_state_vec[3] = saturate(new_state_vec[3], 0.0, 350.0*KTS2MS)
            self.st_vector.update_from_array(new_state_vec)

        self.current_time = t
        if update and self.st_vector.initialized():
            self.update_ui()
            self.st_vector.send_to_ivy()

    def compute_position(self, t, s_vec):
        eps = sys.float_info.epsilon
        wx, wy = InputVector.getInstance().get_wind_components()
        c_state = self.cmd_vector

        # s_vec is an np.array like [x, y, z, vp, fpa, psi, phi]
        x, y, z, vp, fpa, psi, phi = list(s_vec)
        g = 9.80665   # acceleration of gravity, m/s^2

        x_dot = vp * math.cos(fpa) * math.cos(psi) + wx
        y_dot = vp * math.cos(fpa) * math.sin(psi) + wy
        z_dot = vp * math.sin(fpa)

        vp_dot = g * (c_state.get_nx() - math.sin(fpa))
        vp = limit_vp(vp)  # limitation a Vp > 0

        fpa_dot = (g / vp) * (c_state.get_nz() * math.cos(phi) - math.cos(fpa))
        cos_fpa = math.cos(fpa)
        if math.fabs(cos_fpa) < 1e3 * eps:
            cos_fpa = 1e3 * eps * sign(math.cos(fpa))
        psi_dot = (g / vp) * (math.sin(phi) / cos_fpa) * c_state.get_nz()
        phi_dot = c_state.get_p()

        return array([
            x_dot, y_dot, z_dot, vp_dot, fpa_dot, psi_dot, phi_dot
        ])

    def my_rk4(self, prev_state, prev_time, dt, compute_func):
        k1 = compute_func(prev_time, prev_state)
        k2 = compute_func(prev_time + dt/2, prev_state + k1*dt/2)
        k3 = compute_func(prev_time + dt/2, prev_state + k2*dt/2)
        k4 = compute_func(prev_time + dt, prev_state + k3*dt)

        return prev_state + (dt/6.0) * (k1 + 2*k2 + 2*k3 + k4)


class AircraftModel(_Model):
    name = "aircraft"
    reset_msg = "^AircraftModelReset$"

    def __init__(self):
        super(AircraftModel, self).__init__()
        self.st_vector = AircraftStateVector.getInstance()
        self.cmd_vector = AircraftCommandVector.getInstance()

    @require_ivy
    def update_ui(self):
        # send model state to flightgear
        a_state = self.st_vector
        i_state = InputVector.getInstance()

        pitch = a_state.get_fpa()         # rad
        X = a_state.get_y()/NM2M          # X en NM
        Y = a_state.get_x()/NM2M          # Y en NM
        Alt = a_state.get_z()/FEET2M      # Alt en feet
        Roll = a_state.get_phi()/DEG2RAD  # Roll en deg
        Pitch = pitch/DEG2RAD             # Pitch en deg
        # Yaw en deg
        Yaw = 0
        if a_state.get_vp() != 0:
            Yaw = 0*(9.80665*math.tan(a_state.get_phi())/a_state.get_vp()/DEG2RAD)
        Airspeed = vp2vi(a_state.get_vp(), a_state.get_z()) / KTS2MS
        # for heading, take magnetic deviation into accoun
        magnetic_cap = modulo_min_max(a_state.get_psi()
                                      - i_state.get_magnetic_deviation(),
                                      0.0, 2*math.pi)
        Heading = magnetic_cap/DEG2RAD  # Heading en deg
        g_speed = self.__calculate_ground_speed()

        msg = "AircraftSetPosition X={0} Y={1} Altitude-ft={2} Roll={3} "\
              "Pitch={4} Yaw={5} Heading={6} Airspeed={7} "\
              "Groundspeed={8}".format(X, Y, Alt, Roll, Pitch, Yaw, Heading,
                                       Airspeed, g_speed)
        logging.debug("Send new position to fligthgear: '%s'" % msg)
        ivy.IvySendMsg(msg)

    def __calculate_ground_speed(self):
        wx, wy = InputVector.getInstance().get_wind_components()
        a_state = AircraftStateVector.getInstance()
        vp = limit_vp(a_state.get_vp())
        fpa = a_state.get_fpa()
        psi = a_state.get_psi()

        den = vp*math.cos(fpa)*math.cos(psi) + wx
        num = vp*math.cos(fpa)*math.sin(psi) + wy
        gs = (pow(den, 2) + pow(num, 2))**0.5  # ground speed, m/sec

        return gs / KTS2MS


class IntruderModel(_Model):
    name = "intruder"
    reset_msg = "^IntruderModelReset$"

    def __init__(self):
        super(IntruderModel, self).__init__()
        self.st_vector = IntruderStateVector.getInstance()
        self.cmd_vector = IntruderCommandVector.getInstance()
