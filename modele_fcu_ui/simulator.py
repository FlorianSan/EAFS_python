#!/usr/bin/env python3

# Copyright (C) 2017 Mickael Royer <mickael.royer@enac.fr>
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
import shlex
import subprocess
import signal
import argparse
import logging
import time


def execute(cmd_line, wait=True, verbose=False, cwd=None):
    logging.debug("Execute command '%s'" % cmd_line)
    args = shlex.split(cmd_line)
    stdout = verbose and sys.stdout or subprocess.PIPE
    process = subprocess.Popen(args,
                               cwd=cwd,
                               stdout=stdout,
                               stderr=subprocess.STDOUT,
                               stdin=subprocess.PIPE)
    if wait:
        process.wait()
        if process.returncode != 0 and not verbose:
            logging.error(process.stdout.read())
    return process


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # parse options
    usage = "usage: %prog [options]"
    parser = argparse.ArgumentParser(description="Simulator launch scripts")
    parser.add_argument(
        "-b", "--ivy-bus", type=str, dest="ivy_bus",
        default="127.255.255.255:2010",
        help="Bus id (format @IP:port, default to 127.255.255.255:2010)")
    parser.add_argument(
        "-q", "--quiet", action="store_false", dest="verbose", default=True,
        help="Hide log messages")
    parser.add_argument(
        "-m", "--disable-model", action="store_false", dest="model",
        default=True, help="Disable aircraft model")
    parser.add_argument(
        "-v", "--fg", action="store_true", dest="fg",
        default=False, help="Launch visualisation (flightgear)")
    options = parser.parse_args()

    # init log
    level = logging.INFO
    if options.verbose:  # update logging level
        level = logging.DEBUG
    logging.getLogger().setLevel(level)

    ###################
    m_process, fg_process, ui_process = None, None, None
    if options.model:
        logging.info("Launch aircraft model on bus %s" % options.ivy_bus)
        m_cmd_line = "python3 ./PyAircraftModel/"\
                     "pyAircraftModel.py -i -b %s" % options.ivy_bus
        m_process = execute(m_cmd_line, wait=False, verbose=options.verbose)
        time.sleep(0.3)

    if options.fg:
        logging.info("Launch flightgear")
        fg_cmd_line = "python3 ./PyIvy2Fg/pyIvy2Fg.py -b %s" % options.ivy_bus
        fg_process = execute(fg_cmd_line, wait=False, verbose=options.verbose)
        time.sleep(1.0)

    def stop(signum, frame):
        for p in (m_process, fg_process, ui_process):
            if p is not None and p.poll() is None:
                p.terminate()
                p.wait()
                p = None

    # Set the signal handler for SIGTERM and SIGINT signal
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)

    logging.info("Launch ui controller")
    ui_cmd_line = "python3 ./PySimControl/pySimControl.py "\
                  "-b %s" % options.ivy_bus
    ui_process = execute(ui_cmd_line, wait=True, verbose=options.verbose)
    stop(None, None)