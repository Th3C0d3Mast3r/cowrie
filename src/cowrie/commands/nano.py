from cowrie.shell.command import HoneyPotCommand


class Command_nano(HoneyPotCommand):

    def start(self):
        if not self.args:
            self.write("Usage: nano <filename>\n")
            self.exit()
            return

        self.filename = self.args[0]
        self.buffer = [""]
        self.cursor_x = 0
        self.cursor_y = 0

        self.rows = 24
        self.cols = 80

        self.protocol.setRawMode()
        self.render()

    def render(self):
        self.write("\033[2J\033[H")  # clear screen

        # Top bar
        title = f" GNU nano 7.2 ".ljust(self.cols // 2)
        fname = self.filename.rjust(self.cols - len(title))
        self.write(title + fname + "\n")

        # Editor area
        for i in range(self.rows - 4):
            if i < len(self.buffer):
                line = self.buffer[i]
                self.write(line[:self.cols] + "\n")
            else:
                self.write("~\n")

        # Status bar
        status = "[ New File ]".rjust(self.cols)
        self.write(status + "\n")

        # Help bar (2 lines)
        self.write("^G Help  ^O Write Out  ^W Where Is  ^K Cut  ^T Execute  ^C Location\n")
        self.write("^X Exit  ^R Read File  ^\\ Replace  ^U Paste  ^J Justify  ^/ Go To Line\n")

        # Move cursor
        self.move_cursor()

    def move_cursor(self):
        row = self.cursor_y + 2
        col = self.cursor_x + 1
        self.write(f"\033[{row};{col}H")

    def characterReceived(self, ch):
        # CTRL+X → exit
        if ch == "\x18":
            self.exit_editor()
            return

        # CTRL+O → save
        if ch == "\x0f":
            self.save_file()
            return

        # ENTER
        if ch == "\r":
            current = self.buffer[self.cursor_y]
            left = current[:self.cursor_x]
            right = current[self.cursor_x:]

            self.buffer[self.cursor_y] = left
            self.buffer.insert(self.cursor_y + 1, right)

            self.cursor_y += 1
            self.cursor_x = 0
            self.render()
            return

        # BACKSPACE
        if ch in ("\x7f", "\b"):
            if self.cursor_x > 0:
                line = self.buffer[self.cursor_y]
                self.buffer[self.cursor_y] = line[:self.cursor_x - 1] + line[self.cursor_x:]
                self.cursor_x -= 1
            elif self.cursor_y > 0:
                prev_line = self.buffer[self.cursor_y - 1]
                current = self.buffer[self.cursor_y]

                self.cursor_x = len(prev_line)
                self.buffer[self.cursor_y - 1] = prev_line + current
                self.buffer.pop(self.cursor_y)
                self.cursor_y -= 1

            self.render()
            return

        # Normal text input
        if ch.isprintable():
            line = self.buffer[self.cursor_y]
            self.buffer[self.cursor_y] = line[:self.cursor_x] + ch + line[self.cursor_x:]
            self.cursor_x += 1
            self.render()

    def save_file(self):
        content = "\n".join(self.buffer)

        self.fs.mkfile(
            self.filename,
            self.protocol.user.uid,
            self.protocol.user.gid,
            len(content),
            0o100644,
        )

        self.fs.file_contents[self.filename] = content

        self.write("\033[2J\033[H")
        self.write(f"File '{self.filename}' written\n")

        self.protocol.setCookedMode()
        self.exit()

    def exit_editor(self):
        self.write("\033[2J\033[H")
        self.protocol.setCookedMode()
        self.exit()

commands: dict = {}
commands["nano"] = Command_nano
commands["/bin/nano"] = Command_nano
commands["/usr/bin/nano"] = Command_nano