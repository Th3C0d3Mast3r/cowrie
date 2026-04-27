from __future__ import annotations
from cowrie.shell.command import HoneyPotCommand
from twisted.internet import reactor
import random
import time


class Command_top(HoneyPotCommand):

    def start(self) -> None:
        self.running = True
        self.frame = 0
        self._delayed_call = None
        self.procs = self._init_processes()
        self.update()

    def _init_processes(self) -> list:
        base = [
            ("sshd",     0.5),
            ("nginx",    1.5),
            ("mysqld",   4.0),
            ("docker",   1.2),
            ("kubelet",  2.5),
            ("java",     5.0),
            ("node",     3.0),
            ("python3",  2.0),
            ("rsyslogd", 0.3),
            ("cron",     0.2),
        ]
        procs = []
        pid = 1200
        for name, base_cpu in base:
            procs.append({
                "pid":      pid,
                "name":     name,
                "cpu":      round(random.uniform(0.1, base_cpu), 2),
                "mem":      round(random.uniform(0.5, 5.0), 2),
                "state":    "S",
                "base_cpu": base_cpu,
            })
            pid += random.randint(10, 60)
        return procs

    def update(self) -> None:
        if not self.running:
            return

        self.frame += 1

        for p in self.procs:
            p["cpu"] = max(0.0, round(p["cpu"] + random.uniform(-0.6, 0.9), 2))
            p["mem"] = max(0.1, round(p["mem"] + random.uniform(-0.3, 0.4), 2))
            if random.random() < 0.07:
                p["state"] = random.choice(["S", "R"])

        if random.random() < 0.15:
            self.procs.append({
                "pid":      random.randint(2000, 5000),
                "name":     random.choice(["worker", "node", "java", "python3", "nginx"]),
                "cpu":      round(random.uniform(0.2, 2.5), 2),
                "mem":      round(random.uniform(0.5, 3.5), 2),
                "state":    "S",
                "base_cpu": 1.0,
            })

        if len(self.procs) > 18 and random.random() < 0.1:
            self.procs.pop(random.randint(0, len(self.procs) - 1))

        if random.random() < 0.2:
            p = random.choice(self.procs)
            p["cpu"] = round(p["cpu"] + random.uniform(3, 10), 2)

        self._render()

        self._delayed_call = reactor.callLater(1.0, self.update)

    def _render(self) -> None:
        self.write("\033[2J\033[H")

        load1  = round(random.uniform(0.2, 1.5), 2)
        load5  = round(random.uniform(0.3, 1.2), 2)
        load15 = round(random.uniform(0.1, 1.0), 2)

        self.write(
            f"top - {time.strftime('%H:%M:%S')} up 23 days,  "
            f"load average: {load1}, {load5}, {load15}\n"
        )
        self.write(
            f"Tasks: {len(self.procs):>3} total,  "
            f"{random.randint(1, 3)} running, "
            f"{len(self.procs) - 2} sleeping,  0 stopped,  0 zombie\n"
        )
        self.write("%Cpu(s):  3.2 us,  1.1 sy,  0.0 ni, 95.0 id,  0.7 wa\n")

        total_mem = 131072
        used      = random.randint(40000, 80000)
        self.write(
            f"MiB Mem : {total_mem:>8} total, {total_mem - used:>8} free, "
            f"{used:>8} used\n\n"
        )

        self.write(
            f"{'PID':<7}{'USER':<10}{'PR':<4}{'NI':<4}"
            f"{'VIRT':<9}{'RES':<7}{'SHR':<7}{'S':<2}"
            f"{'%CPU':>5}{'%MEM':>5}  {'TIME+':<10}COMMAND\n"
        )

        for p in sorted(self.procs, key=lambda x: x["cpu"], reverse=True)[:12]:
            self.write(
                f"{p['pid']:<7}{'root':<10}{'20':<4}{'0':<4}"
                f"{'500000':<9}{'120000':<7}{'80000':<7}{p['state']:<2}"
                f"{p['cpu']:>5}{p['mem']:>5}  {'0:01.00':<10}{p['name']}\n"
            )

    def handle_CTRL_C(self) -> None:
        self.running = False
        if self._delayed_call is not None and self._delayed_call.active():
            self._delayed_call.cancel()
        self.write("^C\n")
        self.exit()


commands: dict = {}
commands["top"]          = Command_top
commands["/usr/bin/top"] = Command_top
commands["/bin/top"]     = Command_top