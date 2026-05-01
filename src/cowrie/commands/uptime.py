# Copyright (c) 2009 Upi Tamminen <desaster@gmail.com>
# See the COPYRIGHT file for more information

from __future__ import annotations

import time

from cowrie.core import utils
from cowrie.shell.command import HoneyPotCommand

commands = {}


# class Command_uptime(HoneyPotCommand):
#     def call(self) -> None:
#         self.write(
#             "{}  up {},  1 user,  load average: 0.00, 0.00, 0.00\n".format(
#                 time.strftime("%H:%M:%S"), utils.uptime(self.protocol.uptime())
#             )
#         )

class Command_uptime(HoneyPotCommand):
    def call(self) -> None:
        # 42 days in seconds (42 * 24 * 60 * 60)
        # This acts as a base offset so the server never looks brand new.
        offset = 3628800 
        
        # Calculate fake uptime: current session uptime + our 42-day offset
        total_uptime_seconds = self.protocol.uptime() + offset
        
        # Format the time and uptime string
        current_time = time.strftime("%H:%M:%S")
        uptime_str = utils.uptime(total_uptime_seconds)
        
        # Load averages: Slightly active server (typical for a 40-core machine)
        # A load of 0.15 on a 40-core CPU means it's effectively 99% idle, 
        # but looks more "real" than 0.00.
        load_avg = "0.08, 0.12, 0.15"

        self.write(
            "{}  up {},  1 user,  load average: {}\n".format(
                current_time, uptime_str, load_avg
            )
        )

commands["/usr/bin/uptime"] = Command_uptime
commands["uptime"] = Command_uptime
