#!/usr/bin/python3

# simulator-control, a simple gui to control mini aircraft simulator
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

import sys
import logging
import os
from optparse import OptionParser
from os import path
import signal
from ivy.std_api import IvyInit, IvyStart, IvyStop
from PyQt5.QtCore import QUrl
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication, QIcon
from simcontrol.ivy_object import IvyQObject
from simcontrol.ivy_object import register_ivy_object
from simcontrol.aircraft_model import register_aircraft_model
from simcontrol.intruder_model import register_intruder_model
from simcontrol.fcu.ap_object import register_ap1_object
import time

os.environ['QT_QUICK_CONTROLS_STYLE'] = 'Material'
signal.signal(signal.SIGINT, signal.SIG_DFL)
logger = logging.getLogger('Ivy')


def connect(app_name, ivy_bus, on_cx_proc):
    def on_die_proc(agent, _id):
        pass

    IvyInit(app_name,                   # application name for Ivy
            "%s ready" % app_name,      # ready message
            0,                          # main loop is local (ie. IvyMainloop)
            on_cx_proc,                 # handler called on connect/disconnect
            on_die_proc)
    IvyStart(ivy_bus)


if __name__ == '__main__':

    time.sleep(3)

    # parse options
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.set_defaults(ivy_bus="127.255.255.255:2010", verbose=False,
                        app_name="IvySimulatorControl")
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
                      help='Be verbose.')
    parser.add_option('-b', '--ivybus', type='string', dest='ivy_bus',
                      help="Bus id (format @IP:port, "
                           "default to 127.255.255.255:2010)")
    parser.add_option('-a', '--appname', type='string', dest='app_name',
                      help='Application Name')
    (options, args) = parser.parse_args()

    # init log
    level = logging.ERROR
    if options.verbose:  # update logging level
        level = logging.DEBUG
    logger.setLevel(level)

    # connection to the ivy bus
    ivy_obj = IvyQObject.getInstance()

    def on_cx_proc(agent, connected):
        ivy_obj.update_application_list()
    connect(options.app_name, options.ivy_bus, on_cx_proc)
    ivy_obj.update_application_list()

    # register singleton objects
    register_ivy_object()
    register_aircraft_model()
    register_intruder_model()
    register_ap1_object()
    # Create the application instance.
    app = QGuiApplication(args)
    file_path = os.path.dirname(__file__)
    app_icon = os.path.join(file_path, "resources", "icons", "sim-app.png")
    app.setWindowIcon(QIcon(app_icon))

    # Create a QML engine.
    engine = QQmlApplicationEngine()
    script_path = path.abspath(path.dirname(__file__))
    p2 = QUrl.fromLocalFile(path.join(script_path, "resources", "main.qml"))
    engine.load(p2)

    app.aboutToQuit.connect(IvyStop)
    sys.exit(app.exec_())