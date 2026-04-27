from cowrie.shell.command import HoneyPotCommand

commands = {}

class Command_ps(HoneyPotCommand):

    def call(self):

        self.write("USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\n")
        self.write("root         1  0.0  0.1  22532  4104 ?        Ss   Jan01   0:02 /sbin/init\n")
        self.write("root       245  0.0  0.0  13248  1020 ?        Ss   Jan01   0:00 cron\n")
        self.write("root       512  0.1  0.3  65432 12320 ?        Ss   Jan01   0:03 sshd\n")
        self.write("mysql      902  0.2  1.2 212432 32320 ?        Sl   Jan01   0:40 mysqld\n")
        self.write("www-data  1023  0.0  0.2  41232  5320 ?        S    Jan01   0:02 nginx\n")
        self.write("root      2031  0.0  0.1  12232  2100 pts/0    Ss   14:00   0:00 bash\n")

        self.exit()

commands["ps"] = Command_ps