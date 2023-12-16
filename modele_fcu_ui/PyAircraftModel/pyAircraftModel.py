#!/usr/bin/env python3

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

import argparse
from ivy.std_api import IvyInit, IvyStart, IvyMainLoop
from pyamodel import set_connected
from pyamodel.states.input_vector import InputVector
from pyamodel.states.state_vector import AircraftStateVector
from pyamodel.states.state_vector import IntruderStateVector
from pyamodel.states.command_vector import AircraftCommandVector
from pyamodel.states.command_vector import IntruderCommandVector
from pyamodel.model import AircraftModel, IntruderModel
import logging

ivy_logger = logging.getLogger('Ivy')
logging.basicConfig(format='AirCraftModel - %(levelname)s - %(message)s')


def connect(app_name, ivy_bus):
    def on_cx_proc(agent, connected):
        pass

    def on_die_proc(agent, _id):
        pass

    global IVY_CONNECTED
    IvyInit(app_name,                   # application name for Ivy
            "%s ready" % app_name,      # ready message
            0,                          # main loop is local (ie. IvyMainloop)
            on_cx_proc,                 # handler called on connect/disconnect
            on_die_proc)
    IvyStart(ivy_bus)
    IVY_CONNECTED = True


def run(options):
    # connection to the ivy bus
    connect(options.app_name, options.ivy_bus)
    set_connected()

    # init states
    states = {
        "aircraft": AircraftStateVector.getInstance(),
        "input": InputVector.getInstance(),
        "command": AircraftCommandVector.getInstance(),
    }
    for s in list(states.values()):
        s.subscribe()

    # launch model
    logging.info("Launch aircraft model")
    model = AircraftModel()
    model.run()

    # launch intruder in necessary
    if options.intruder:
        IntruderStateVector.getInstance().subscribe()
        IntruderCommandVector.getInstance().subscribe()

        logging.info("Launch intruder model")
        model = IntruderModel()
        model.run()

    IvyMainLoop()


if __name__ == '__main__':
    # parse options
    parser = argparse.ArgumentParser(description='Simple aircraft model')

    parser.add_argument(
        "-d", "--debug", action="store_true", dest="debug", default=False,
        help="Log more debug informations")
    parser.add_argument(
        "--ivy-debug", action="store_true", dest="ivy_debug", default=False,
        help="View ivy log messages")
    parser.add_argument(
        "-i", "--intruder", action="store_true",
        dest="intruder", default=False,
        help="Activate intruder aircraft")
    parser.add_argument(
        "-b", "--ivy-bus", type=str, dest="ivy_bus",
        default="127.255.255.255:2010",
        help="Bus id (format @IP:port, default to 127.255.255.255:2010)")
    parser.add_argument(
        "-a", "--app-name", type=str, dest="app_name",
        default="PyAircraftModel", help="Application Name")
    args = parser.parse_args()

    # init log
    level, ivy_level = logging.INFO, logging.ERROR
    if args.debug:  # Si mode verbeux choisi
        level = logging.DEBUG
    if args.ivy_debug:
        ivy_level = logging.INFO
    logging.getLogger().setLevel(level)
    ivy_logger.setLevel(ivy_level)

    run(args)
