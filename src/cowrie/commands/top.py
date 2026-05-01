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
        # Start with a more populated process list for a 40-core server
        self.procs = self._init_processes()
        self.update()

    def _init_processes(self) -> list:
        # Format: (Command, User, Base CPU, Base Mem MiB, Custom VIRT string)
        process_templates = [
            # Infrastructure & Dev Stack
            ("code", "srv_admin", 1.3, 202.2, "1393.8g"),
            ("brave", "srv_admin", 1.3, 97.4, "48.5g"),
            ("gnome-terminal-", "srv_admin", 1.3, 69.0, "717308"),
            ("mongod", "mongodb", 2.1, 2048.0, "4.2g"),
            ("grafana-serv", "grafana", 0.5, 512.0, "1.1g"),
            ("java", "jenkins", 4.2, 4096.0, "8.5g"),
            
            # Desktop/System Services (Portals)
            ("xdg-desktop-por", "srv_admin", 0.3, 43.2, "687400"),
            ("xdg-document-po", "srv_admin", 0.3, 7.6, "683904"),
            ("gnome-session-b", "srv_admin", 0.7, 16.5, "486632"),
            ("gsd-sharing", "srv_admin", 0.3, 12.7, "469340"),
            ("ibus-extension-", "srv_admin", 0.3, 32.7, "423508"),
            ("dbus-daemon", "message+", 1.3, 8.6, "12212"),
            ("pipewire", "srv_admin", 1.0, 16.0, "109160"),
            
            # System Daemons
            ("systemd", "root", 0.1, 12.0, "168340"),
            ("systemd-resolve", "systemd+", 0.3, 14.8, "23344"),
            ("containerd-shim", "root", 0.3, 16.2, "1239916"),
            ("avahi-daemon", "avahi", 0.3, 4.6, "6800"),
            
            # Kernel Threads
            ("[rcu_preempt]", "root", 0.3, 0.0, "0"),
            ("[migration/14]", "root", 0.3, 0.0, "0"),
            ("[kworker/5:2-ev]", "root", 0.3, 0.0, "0"),
            ("[irq/75-rtw89_p]", "root", 0.3, 0.0, "0"),
            ("[kblockd]", "root", 0.1, 0.0, "0"),

            # --- Security & Networking ---
            ("sshd", "root", 0.1, 12.4, "15.2m"),
            ("rsyslogd", "syslog", 0.1, 8.2, "224500"),
            ("fail2ban-server", "root", 0.5, 45.0, "980m"),
            ("systemd-journal", "root", 0.3, 28.5, "45000"),
            
            # --- Hardware & Management ---
            ("irqbalance", "root", 0.1, 4.2, "12500"),
            ("thermald", "root", 0.0, 2.1, "350m"),
            ("smartd", "root", 0.0, 3.4, "8500"),
            ("atop", "root", 0.7, 12.0, "25000"), # Performance monitor
            
            # --- Container Overhead ---
            ("kube-proxy", "root", 0.2, 38.0, "1.2g"),
            ("coredns", "root", 0.1, 24.0, "700m"),
            ("containerd-shim", "root", 0.1, 10.5, "1.1g"),
            
            # --- More Kernel Threads (Brackets) ---
            ("[kcompactd0]", "root", 0.0, 0.0, "0"),
            ("[khugepaged]", "root", 0.0, 0.0, "0"),
            ("[kswapd0]", "root", 0.1, 0.0, "0"),
            ("[jbd2/sda1-8]", "root", 0.1, 0.0, "0"), # Filesystem journal
            ("[ext4-rsv-conver]", "root", 0.0, 0.0, "0"),
        ]

        procs = []
        for name, user, cpu, mem, virt in process_templates:
            procs.append({
                "pid": random.randint(100, 90000),
                "user": user,
                "name": name,
                "cpu": cpu,
                "mem_val": mem,
                "virt_str": virt,
                "state": "I" if "[" in name else "S",
                "time": f"{random.randint(0, 5)}:{random.randint(10, 59)}.{random.randint(10, 99)}"
            })
        return procs

    def update(self) -> None:
        if not self.running:
            return

        self.frame += 1

        for p in self.procs:
            # Fluctuating CPU and Memory
            p["cpu"] = max(0.1, round(p["cpu"] + random.uniform(-0.5, 0.5), 1))
            # Shift memory slightly to look dynamic
            p["mem_val"] = max(16.0, p["mem_val"] + random.uniform(-2.0, 2.0))
            
            if random.random() < 0.05:
                p["state"] = random.choice(["S", "R", "I"])

        # Occasionally add short-lived processes (like someone running a cron or bash)
        if random.random() < 0.1:
            self.procs.append({
                "pid":      random.randint(20000, 40000),
                "user":     "root",
                "name":     random.choice(["bash", "ls", "grep", "sed", "python3"]),
                "cpu":      round(random.uniform(0.1, 2.0), 1),
                "mem_val":  32.0,
                "state":    "R",
                "time":     "0:00.01"
            })

        # Keep process list size reasonable
        if len(self.procs) > 50:
            self.procs.pop(random.randint(12, len(self.procs) - 1))

        self._render()
        self._delayed_call = reactor.callLater(3, self.update)  # every 3seconds, the top should update

    def _render(self) -> None:
        self.write("\r\033[H")

        # Enterprise Load Averages (40 cores means 2.0 is very low load)
        load1  = "1.12"
        load5  = "1.05"
        load15 = "0.98"

        self.write(
            f"top - {time.strftime('%H:%M:%S')} up 42 days,  1 user,  "
            f"load average: {load1}, {load5}, {load15}\n"
        )
        self.write(
            f"Tasks: {len(self.procs) + 380:3} total,  "
            f"{random.randint(1, 3)} running, {len(self.procs) + 377} sleeping,  0 stopped,  0 zombie\n"
        )
        # Low CPU usage % (95%+ Idle is common for large servers)
        self.write("%Cpu(s):  1.8 us,  0.9 sy,  0.0 ni, 97.1 id,  0.1 wa,  0.0 hi,  0.1 si,  0.0 st\n")

        total_mem = 128765.4 # 128GB in MiB
        used_mem  = 42150.8  # ~42GB used
        free_mem  = total_mem - used_mem
        
        self.write(
            f"MiB Mem : {total_mem:9.1f} total, {free_mem:9.1f} free, "
            f"{used_mem:9.1f} used, {18500.0:9.1f} buff/cache\n"
        )
        self.write(
            f"MiB Swap: {16384.0:9.1f} total, {16384.0:9.1f} free, "
            f"{0.0:9.1f} used. {82000.0:9.1f} avail Mem\n\n"
        )

        self.write(
            f"{'PID':<7}{'USER':<10}{'PR':<4}{'NI':<4}"
            f"{'VIRT':<9}{'RES':<7}{'SHR':<7}{'S':<2}"
            f"{'%CPU':>5}{'%MEM':>5}  {'TIME+':<10}COMMAND\n"
        )

        # Sort by CPU usage to look like real top
        sorted_procs = sorted(self.procs, key=lambda x: x["cpu"], reverse=True)

        for p in sorted_procs[:30]:
            # Calculate %MEM based on 128GB total
            mem_percent = round((p["mem_val"] / total_mem) * 100, 1)
            # Fake VIRT/RES/SHR based on base_mem
            virt = int(p["mem_val"] * 1.2 * 1024)
            res = int(p["mem_val"] * 1024)
            shr = int(p["mem_val"] * 0.4 * 1024)

            self.write(
                f"{p['pid']:<7}{p['user']:<10}{'20':<4}{'0':<4}"
                f"{virt:<9}{res:<7}{shr:<7}{p['state']:<2}"
                f"{p['cpu']:>5.1f}{mem_percent:>5.1f}  {p['time']:<10}{p['name']}\n"
            )

    def handle_CTRL_C(self) -> None:
        self.running = False
        if self._delayed_call is not None and self._delayed_call.active():
            self._delayed_call.cancel()
        self.write("\r\n")
        self.exit()

commands: dict = {}
commands["top"]          = Command_top
commands["/usr/bin/top"] = Command_top
commands["/bin/top"]     = Command_top