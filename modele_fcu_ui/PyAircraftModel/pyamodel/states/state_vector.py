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
from numpy import array
from pyamodel import ivy
from pyamodel import require_ivy
from pyamodel.states.base import float_setter
from pyamodel.states.base import BaseStateVector
from pyamodel.utils import pi, DEG2RAD, modulo_min_max


class _StateVector(BaseStateVector):

    def __init__(self):
        self.is_init = False
        self.x, self.y, self.z = 0.0, 0.0, 0.0
        self.vp, self.fpa, self.psi, self.phi = 1.0, 0.0, 0.0, 0.0

    def reset(self):
        self.is_init = False
        self.x, self.y, self.z = 0.0, 0.0, 0.0
        self.vp, self.fpa, self.psi, self.phi = 1.0, 0.0, 0.0, 0.0

    def initialized(self):
        return self.is_init

    def set_pos(self, x, y, z):
        try:
            self.x, self.y, self.z = (float(x), float(y), float(z))
        except TypeError:
            logging.error(
                "Position is not well formated: '%s, %s, %s'", x, y, z)

    @float_setter
    def set_vp(self, vp):
        self.vp = vp

    @float_setter
    def set_fpa(self, fpa):
        self.fpa = fpa

    @float_setter
    def set_psi(self, psi):
        self.psi = psi

    @float_setter
    def set_phi(self, phi):
        self.phi = phi

    def get_pos(self):
        return self.x, self.y, self.z

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def get_vp(self):
        return self.vp

    def get_fpa(self):
        return self.fpa

    def get_psi(self):
        return self.psi

    def get_phi(self):
        return self.phi

    def to_array(self):
        return array((self.x, self.y, self.z, self.vp,
                      self.fpa, self.psi, self.phi))

    def update_from_array(self, ar_state):
        # array is formated like this: [x, y, z, vp, fpa, psi]
        self.set_pos(ar_state[0], ar_state[1], ar_state[2])
        self.set_vp(ar_state[3])
        self.set_fpa(ar_state[4])
        self.set_psi(ar_state[5])
        self.set_phi(ar_state[6])


class AircraftStateVector(_StateVector):
    INIT_STATE_BIND = "^InitStateVector\s+x=(\S+)\s+y=(\S+)\s+z=(\S+)\s+"\
                      "Vp=(\S+)\s+fpa=(\S+)\s+psi=(\S+)\s+phi=(\S+)"
    STATE_MSG = "StateVector x={} y={} z={} Vp={} fpa={} psi={} phi={}"

    def reset(self):
        super(AircraftStateVector, self).reset()
        ivy.IvySendMsg(self.STATE_MSG.format(*self.to_array()))

    @require_ivy
    def subscribe(self):
        ivy.IvyBindMsg(
            lambda a, *larg: self.init_state_vector(*larg),
            self.INIT_STATE_BIND)

    @require_ivy
    def send_to_ivy(self):
        if not self.is_init:
            logging.warning(
                "SV has to been sent to ivy, however it is not initialized")
            return
        ivy.IvySendMsg(self.STATE_MSG.format(*self.to_array()))

    def init_state_vector(self, x, y, z, vp, fpa, psi, phi):
        if self.is_init:
            return

        logging.debug(
            "Init State Vector: %s, %s, %s, %s, %s, %s %s"
            % (x, y, z, vp, fpa, psi, phi))
        self.set_pos(x, y, z)
        self.set_vp(vp)
        self.set_fpa(fpa)
        self.set_psi(psi)
        self.set_phi(phi)
        self.is_init = True


class IntruderStateVector(_StateVector):
    SET_STATE_BIND = "^SetIntruStateVector\s+x=(\S+)\s+y=(\S+)\s+z=(\S+)\s+"\
                     "Vp=(\S+)\s+fpa=(\S+)\s+psi=(\S+)\s+phi=(\S+)"
    STATE_MSG = "IntruStateVector x={} y={} z={} Vp={} fpa={} psi={} phi={}"
    SET_CONFLICT_POS = "^SetIntruConflictPos tcpa=(\S+) dcpa=(\S+) r0=(\S+) dtrack=(\S+)"

    def reset(self):
        super(IntruderStateVector, self).reset()
        ivy.IvySendMsg(self.STATE_MSG.format(*self.to_array()))

    @require_ivy
    def subscribe(self):
        ivy.IvyBindMsg(
            lambda a, *larg: self.set_state_vector(*larg),
            self.SET_STATE_BIND)
        ivy.IvyBindMsg(
            lambda a, *larg: self.set_conflict_pos(*larg),
            self.SET_CONFLICT_POS)

    @require_ivy
    def send_to_ivy(self):
        if not self.is_init:
            return
        ivy.IvySendMsg(self.STATE_MSG.format(*self.to_array()))

    def set_state_vector(self, x, y, z, vp, fpa, psi, phi):
        self.set_pos(x, y, z)
        self.set_vp(vp)
        self.set_fpa(fpa)
        self.set_psi(psi)
        self.set_phi(phi)

        self.is_init = True

    def set_conflict_pos(self, tcpa, dcpa, r0, delta_trk):
        ast_vector = AircraftStateVector.getInstance()
        intru_state = self.__calculate_intruder_state(
            float(tcpa), float(dcpa), float(r0), float(delta_trk)
        )
        # init intruder state vector
        self.set_pos(intru_state["x"], intru_state["y"], ast_vector.get_z())
        self.set_vp(intru_state["vp"])
        self.set_fpa(0)
        self.set_psi(intru_state["psi"])
        self.set_phi(0)

        self.is_init = True

    # calculate an intruder position to enable conflict based on the
    # following parameters :
    #   - tcpa: time before the minimal reconciliation
    #   - dcpa : distance for the minimal reconciliation
    #   - ro : initial distance between the aircraft and the intruder
    #   - delta_trk : cross angle 
    def __calculate_intruder_state(self, tcpa, dcpa, r0, delta_trk):
        ast_vector = AircraftStateVector.getInstance()
        a_psi, a_vp = ast_vector.get_psi(), ast_vector.get_vp()
        a_x, a_y = ast_vector.get_x(), ast_vector.get_y()

        if r0 < dcpa:
            self.send_to_ivy(
                "IntruError msg={}".format("r0 must be greater than dcpa"))
            return
        d0 = (pow(r0, 2) - pow(dcpa, 2))**0.5

        if tcpa <= 0:
            self.send_to_ivy(
                "IntruError msg={}".format("tcpa must be greater than 0"))
            return
        Vr = d0 / tcpa

        delta_trk = DEG2RAD * delta_trk
        i_psi = a_psi + delta_trk
        i_psi = modulo_min_max(i_psi, -pi, pi)
        gs_2_vrsin_delta = a_vp / Vr*math.sin(a_psi-i_psi)
        if abs(gs_2_vrsin_delta) > 1:
            self.send_to_ivy(
                "IntruError msg={}".format("abs(gs_2_vrsin_delta) > 1"))
            return

        trk_vr1 = i_psi + math.asin(gs_2_vrsin_delta)
        trk_vr2 = i_psi + pi - math.asin(gs_2_vrsin_delta)

        trk1_check1 = math.atan2(
            a_vp*math.sin(a_psi) - Vr*math.sin(trk_vr1),
            a_vp*math.cos(a_psi) - Vr*math.cos(trk_vr1))
        trk_vr = abs(trk1_check1 - i_psi) < 1*DEG2RAD and trk_vr1 or trk_vr2

        gs1cos_trk1 = a_vp*math.cos(a_psi) - Vr*math.cos(trk_vr)
        gs1sin_trk1 = a_vp*math.sin(a_psi) - Vr*math.sin(trk_vr)

        return {
            "vp": (gs1cos_trk1**2 + gs1sin_trk1**2)**0.5,
            "psi": math.atan2(gs1sin_trk1, gs1cos_trk1),
            "x": a_x + math.cos(trk_vr)*d0 - math.sin(trk_vr)*dcpa,
            "y": a_y + math.sin(trk_vr)*d0 + math.cos(trk_vr)*dcpa
        }
