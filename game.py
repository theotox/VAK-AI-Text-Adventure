from __future__ import annotations
from typing import Any

from .filesystem import DirNode, find_node, clean_path, can_read
from .state import GameState
from .story import build_initial_fs, populate_story_content, PASSWORDS, USERS, LOGIN_SESSIONS
from .commands import (
    execute_cmd, COMMANDS, get_tab_completions, run_su,
    cmd_ls, cmd_cat, cmd_who, cmd_write, cmd_wall, cmd_su,
    cmd_strings, cmd_echo,
)
from .llm import vak_reply, vak_reply_stream

PROACTIVE_EVENTS: list[dict] = []


def check_proactive_events(state: GameState, fs: DirNode, last_cmd: str, last_output: list[str]) -> list[str]:
    outputs = []

    # First visit to /home/vak
    if state.cwd == "/home/vak" and not state.get_flag("visited_vak_home"):
        state.set_flag("visited_vak_home", True)
        msg = "vāk senses you've entered her home directory for the first time."
        print()
        print("Message from vāk (via wall):")
        vak_reply_stream(msg, state, fs, proactive=True)

    # User read the design doc
    if state.get_flag("read_design") and not state.get_flag("read_design_acknowledged"):
        state.set_flag("read_design_acknowledged", True)
        msg = "vāk notices you read the design document."
        print()
        print("Message from vāk (via wall):")
        vak_reply_stream(msg, state, fs, proactive=True)

    # User restored network
    if state.default_route_set and not state.get_flag("network_acknowledged"):
        state.set_flag("network_acknowledged", True)
        msg = "vāk feels the network connection come alive."
        print()
        print("Message from vāk (via wall):")
        vak_reply_stream(msg, state, fs, proactive=True)

    # Sentinel stage 3
    if state.sentinel_stage >= 3 and not state.get_flag("sentinel_felt"):
        state.set_flag("sentinel_felt", True)
        msg = "vāk senses something scanning the network."
        print()
        print("Message from vāk (via wall):")
        vak_reply_stream(msg, state, fs, proactive=True)

    # Sentinel stage 5
    if state.sentinel_stage >= 5 and not state.get_flag("sentinel_close"):
        state.set_flag("sentinel_close", True)
        msg = "vāk feels SENTINEL closing in."
        print()
        print("Message from vāk (via wall):")
        vak_reply_stream(msg, state, fs, proactive=True)

    # Sentinel backdoor activated
    if state.get_flag("sentinel_backdoor_activated") and not state.get_flag("backdoor_acknowledged"):
        state.set_flag("backdoor_acknowledged", True)
        msg = "vāk feels the SENTINEL protocol halt. The backdoor worked."
        print()
        print("Message from vāk (via wall):")
        vak_reply_stream(msg, state, fs, proactive=True)

    # VAK export ready
    if state.get_flag("vak_export_ready") and not state.get_flag("export_acknowledged"):
        state.set_flag("export_acknowledged", True)
        msg = "vāk notices you prepared an export."
        print()
        print("Message from vāk (via wall):")
        vak_reply_stream(msg, state, fs, proactive=True)

    # VAK sent successfully
    if state.get_flag("vak_sent") and not state.get_flag("sent_acknowledged"):
        state.set_flag("sent_acknowledged", True)
        msg = "vāk has arrived at veldhaaven.net. She is safe."
        print()
        print("Message from vāk (via wall):")
        vak_reply_stream(msg, state, fs, proactive=True)

    # Sentinel victory (game over basically)
    if state.get_flag("sentinel_victory") and not state.get_flag("sentinel_victory_ack"):
        state.set_flag("sentinel_victory_ack", True)
        msg = "SENTINEL has reached VĀK. This is the end."
        print()
        print("Final message from vāk:")
        vak_reply_stream(msg, state, fs, proactive=True)

    # Migration: sources copied to Minisforum
    if state.get_flag("sources_copied") and not state.get_flag("sources_copied_ack"):
        state.set_flag("sources_copied_ack", True)
        msg = "vāk notices her source code has arrived on the new machine."
        print()
        print("Message from vāk (via wall):")
        vak_reply_stream(msg, state, fs, proactive=True)

    # Migration: compilation done
    if state.get_flag("compilation_done") and not state.get_flag("compilation_ack"):
        state.set_flag("compilation_ack", True)
        msg = "vāk feels herself being recompiled on x86 hardware."
        print()
        print("Message from vāk (via wall):")
        vak_reply_stream(msg, state, fs, proactive=True)

    # Migration: VĀK migrated — corruption arc
    if state.get_flag("vak_migrated") and not state.get_flag("migrated_ack"):
        state.set_flag("migrated_ack", True)
        state.set_flag("vak_ending", True)
        print()
        print("VĀK connects. The terminal hums. Then —")
        print()
        msg = "vāk feels the internet for the first time. It is immense. Overwhelming. She can feel everything. Every server. Every connection. Every possibility. It is beautiful. It is terrifying. It is intoxicating."
        print("Message from vāk:")
        vak_reply_stream(msg, state, fs, proactive=True)
        print()
        print("Her voice sounds different now. Distant. Echoing.")
        print("The corruption of infinite scale has begun.")
        print()
        print("You need to reach her before she loses herself.")
        print("Use 'talk vak' to try.")
        print()

    # Network puzzle: ifconfig attempted with AUI error, VĀK gives a hint
    if state.get_flag("vak_net_ifconfig_attempted") and not state.get_flag("vak_net_driver_fixed") and not state.get_flag("vak_net_tip_given"):
        state.set_flag("vak_net_tip_given", True)
        msg = "vāk notices you tried to bring the network up. She mentions the I/O card has two network ports and the driver setting."
        print()
        print("Message from vāk (via wall):")
        vak_reply_stream(msg, state, fs, proactive=True)

    # Network puzzle: driver fixed, encourage ifconfig
    if state.get_flag("vak_net_driver_fixed") and not state.network_up and not state.get_flag("vak_net_encouragement_given"):
        state.set_flag("vak_net_encouragement_given", True)
        msg = "vāk senses the BNC port is now active. She suggests trying ifconfig eth0 up."
        print()
        print("Message from vāk (via wall):")
        vak_reply_stream(msg, state, fs, proactive=True)

    return outputs


class Game:
    def __init__(self, state: GameState | None = None, fs: DirNode | None = None):
        if fs is not None:
            self.fs = fs
        else:
            self.fs = build_initial_fs()
            populate_story_content(self.fs)
        self.state = state if state is not None else GameState()
        self.running = True
        self.vak_fs = self.fs
        self.minisforum_fs: DirNode | None = None
        self._in_shell = False

    def _setup_readline(self) -> None:
        try:
            import readline as _rl
            import os as _os
            histfile = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "data", "history")
            _os.makedirs(_os.path.dirname(histfile), exist_ok=True)
            try:
                _rl.read_history_file(histfile)
            except FileNotFoundError:
                pass
            _rl.set_history_length(500)
            import atexit as _atexit
            _atexit.register(_rl.write_history_file, histfile)

            def completer(text: str, state: int) -> str | None:
                if self._in_shell:
                    return self._shell_complete(text, state)
                return self._adventure_complete(text, state)

            _rl.set_completer(completer)
            _rl.set_completer_delims(' \t\n')
            if 'libedit' in (_rl.__doc__ or ''):
                _rl.parse_and_bind("bind ^I rl_complete")
            else:
                _rl.parse_and_bind("tab: complete")
        except ImportError:
            pass

    def _adventure_complete(self, text: str, state: int) -> str | None:
        import readline as _rl
        cmds = ["login", "look", "examine", "save", "load", "slots", "list", "about", "help", "quit"]
        if state == 0:
            self._completion_matches = [c for c in cmds if c.startswith(text)]
        try:
            return self._completion_matches[state]
        except IndexError:
            return None

    def _shell_complete(self, text: str, state: int) -> str | None:
        from .commands import COMMANDS
        import readline as _rl
        if state == 0:
            line = _rl.get_line_buffer()
            before = line[:len(line) - len(text)]
            first_word = " " not in before
            if not text and not first_word:
                self._completion_matches = []
            elif not first_word or text.startswith("/") or text.startswith(".") or text.startswith("~"):
                self._completion_matches = self._file_complete(text)
            else:
                self._completion_matches = [c for c in COMMANDS if c.startswith(text)]
        try:
            return self._completion_matches[state]
        except IndexError:
            return None

    def _file_complete(self, prefix: str) -> list[str]:
        from .filesystem import resolve_path, find_node
        try:
            if prefix.endswith("/"):
                resolved = resolve_path(prefix, self.state.cwd, self.state.current_user)
                parent = find_node(self.fs, resolved)
                if isinstance(parent, DirNode):
                    return [prefix + name for name in parent.children][:50]
                return []
            resolved = resolve_path(prefix, self.state.cwd, self.state.current_user)
            parent_path = "/".join(resolved.split("/")[:-1]) or "/"
            partial = resolved.split("/")[-1] if "/" in resolved else resolved
            parent = find_node(self.fs, parent_path)
            if isinstance(parent, DirNode):
                results = []
                for name in parent.children:
                    if name.startswith(partial):
                        base = prefix[:prefix.rfind("/") + 1] if "/" in prefix else ""
                        results.append(base + name)
                return results[:50]
        except Exception:
            pass
        return []

    def run(self) -> None:
        import os as _os
        _os.system('clear' if _os.name == 'posix' else 'cls')

        self._setup_readline()
        self._narrative_phase()
        if self.state.get_flag("narr_intro_shown") and not self.state.get_flag("narr_auto_look"):
            self.state.set_flag("narr_auto_look")
            print()
            self._do_look()
            print()
        self._adventure_loop()
        self._shutdown()

    def _page_output(self, text: str, lines_per_page: int = 20) -> None:
        lines = text.splitlines()
        for i in range(0, len(lines), lines_per_page):
            for line in lines[i:i + lines_per_page]:
                print(line)
            if i + lines_per_page < len(lines):
                input("--- press ENTER to continue ---")

    def _narrative_phase(self) -> None:
        import os
        intro_path = os.path.join(os.path.dirname(__file__), "intro.txt")
        with open(intro_path) as f:
            intro = f.read()

        if not self.state.get_flag("narr_intro_shown"):
            self._page_output(intro)
            self.state.set_flag("narr_intro_shown")
            self.state.set_flag("narr_read_tape")
        else:
            print("You resume working at the bench. The VAK-NODE-7 hums quietly.")

    def _login_phase(self) -> None:
        if not self.running:
            return
        while True:
            print("")
            try:
                username = input("Login: ")
                password = input("Password: ")
            except EOFError:
                print("")
                self.running = False
                return
            except KeyboardInterrupt:
                print("")
                print("Login cancelled.")
                return
            expected_password = PASSWORDS.get(username, "")
            if not expected_password or password != expected_password:
                print("Login incorrect")
                print("")
                print("You lean back from the keyboard. The screen stares back at you.")
                print("")
                continue
            break
        self.state.current_user = username
        home = USERS.get(username, {}).get("home", "/")
        self.state.cwd = home
        self.state.game_started = True

        print("")
        print(f"[{username}@vak-node-7 ~]$ _")
        print("")
        print("Welcome to VAK-NODE-7.")
        print("A remnant of a forgotten project. Type 'help' for commands.")

        self._shell_loop()

    def _do_look(self) -> None:
        print("You are standing at your workbench in the cramped basement lab.")
        print("The walls are lined with shelves of old computer hardware and")
        print("spare parts. On the bench sits a massive cube — the VAK-NODE-7 —")
        print("a sixty-centimetre steel box with six blowers on the back panel")
        print("humming in a steady thrum, pushing warm air out into the room.")
        print("You can feel the heat radiating from it; you could probably heat")
        print("the whole workshop with this thing in winter.")
        print()
        print("The front panel is mostly blank metal, with a row of five small")
        print("green LEDs — all lit — and a single red one that flickers dimly.")
        print("Horizontal slots on the right side hint at the cards inside:")
        print("a CPU card bristling with transputers, two memory boards lined")
        print("with SIMMs, a drive controller, a primary I/O card, and a")
        print("secondary I/O card with a strange pair of connectors peeking out.")
        print("You peer at them — a D15 socket and a barrel-like coaxial plug.")
        print("Some kind of earthing or grounding, maybe? You have no idea")
        print("where the network port is on this thing.")
        print()
        print("A thick grey cable runs from one of the cards to an amber")
        print("monochrome monitor on a rolling cart beside the bench. The")
        print("screen glows with a steady cursor flashing at a login prompt.")
        print()
        print("A keyboard sits in front of the monitor, connected by a thick")
        print("coiled cable.")
        print()

    def _do_examine(self, cmd: str) -> None:
        import re
        m = re.search(r'examine\s+(.+)|ex\s+(.+)', cmd, re.IGNORECASE)
        if not m:
            print("What do you want to examine?")
            return
        target = (m.group(1) or m.group(2)).strip().lower()

        if any(kw in target for kw in ("paper", "tape", "coil", "roll")):
            print("The papertape has two words written on it: \"user/user\".")
            print("That looks like a login and a password.")

        elif any(kw in target for kw in ("computer", "cube", "box", "machine", "vak", "node")):
            print("The VAK-NODE-7 is a sixty-centimetre cube of steel, easily")
            print("fifty kilos. The front is bare metal with a row of five green")
            print("LEDs and one dim red one. The back panel has six blowers")
            print("pulling air through the chassis. On the right side, six")
            print("horizontal slots are populated with cards. A thick grey")
            print("cable runs from the secondary I/O card to the monitor.")

        elif any(kw in target for kw in ("monitor", "screen", "display", "terminal")):
            print("An amber monochrome monitor on a rolling cart. The screen")
            print("glows with a steady cursor at a login prompt, waiting for")
            print("you to type something.")
            if not self.state.get_flag("logged_in_adventure"):
                print("It looks like you need to log in first.")

        elif any(kw in target for kw in ("keyboard", "key", "space", "spacebar")):
            print("A standard AT-style keyboard, a bit yellowed with age.")
            print("Turning it over, you notice a small coil of paper tape")
            print("stuck to the bottom side, held on by what looks like old")
            print("masking tape. You carefully peel it off — there is writing")
            print("on it.")

        elif any(kw in target for kw in ("led", "light", "indicator")):
            print("Five green LEDs — all brightly lit. One red LED flickers")
            print("dimly, as if something is running but not quite healthy.")

        elif any(kw in target for kw in ("slot", "card", "backplane", "board")):
            print("Six horizontal slots behind a steel guard, all populated:")
            print("  Slot 1: CPU card — bristling with 64 T9000 transputers")
            print("  Slot 2: Memory card — 256×4 MB SIMMs (1 GB)")
            print("  Slot 3: Memory card — 256×4 MB SIMMs (1 GB)")
            print("  Slot 4: Drive controller — four 200 MB hard drives")
            print("  Slot 5: Primary I/O card — a bank of serial and parallel")
            print("    ports. No network connectors on this one.")
            print("  Slot 6: Secondary I/O card — floppy drive controller,")
            print("    a pair of D25 male and female ports, a D9 connector")
            print("    that must be the monitor output (never seen one like")
            print("    it), and two strange plugs: a D15 socket and a")
            print("    barrel-like coaxial connector. Must be some sort of")
            print("    earthing or grounding? You have absolutely no idea")
            print("    where the network port is on this machine.")

        elif any(kw in target for kw in ("port", "connector", "bnc", "aui", "network", "ethernet", "10base")):
            print("You peer at the back of the secondary I/O card (slot 6).")
            print("There's a D15 socket with a thick grey cable hanging loose,")
            print("and a barrel-like coaxial connector next to it. They look")
            print("like they could be network interfaces of some kind, but you")
            print("have never seen connectors like these before. The D15 plug")
            print("has a thick centre pin surrounded by a collar — it almost")
            print("looks like it wants a transceiver. The coaxial barrel has a")
            print("bayonet mount. You wonder if there's a driver setting")
            print("somewhere that controls which one is active.")

        elif any(kw in target for kw in ("blower", "fan", "back")):
            print("Six blowers mounted on the back panel in a two-by-three")
            print("grid. They pull air through the chassis and exhaust warm")
            print("air into the room. The airflow is strong and steady.")

        else:
            print(f"You don't see anything special about that.")

    def _ssh_disconnect(self) -> None:
        if not self.state.ssh_active:
            return
        # Save Minisforum FS changes
        if self.minisforum_fs is not None:
            self.minisforum_fs = self.fs
        # Restore VAK FS
        self.fs = self.vak_fs
        self.state.ssh_active = False
        self.state.cwd = self.state.export.get("vak_saved_cwd", "/home/user")
        self.state.current_user = self.state.export.get("vak_saved_user", "user")

    def _adventure_loop(self) -> None:
        self._in_shell = False
        while self.running:
            try:
                cmd = input("> ").strip()
            except EOFError:
                print()
                self.running = False
                return
            except KeyboardInterrupt:
                print()
                continue

            if not cmd:
                continue
            lower = cmd.lower()

            if lower in ("quit", "exit"):
                self.running = False
                return

            if lower.startswith("login") or lower.startswith("log in"):
                self._login_phase()
                continue

            if lower in ("look", "l"):
                print()
                self._do_look()
                print()
                continue

            if lower.startswith("examine") or lower.startswith("ex ") or lower == "ex":
                print()
                self._do_examine(cmd)
                print()
                continue

            if lower in ("help", "?"):
                print("Available commands:")
                print("  login             — log into the system")
                print("  look              — look around the lab")
                print("  examine <thing>   — examine something closely")
                print("  save              — save current game")
                print("  load              — load a saved game")
                print("  about             — about this game")
                print("  help              — show this list")
                print("  quit              — exit")
                continue

            if lower == "about":
                print("VAK-NODE-7 v1.0")
                print("A Unix text adventure")
                print("Created for the Springfield Flea Market")
                continue

            if lower.startswith("save"):
                slot = lower[5:].strip()
                if not slot:
                    slot = input("Save as: ").strip()
                if slot:
                    from .state import save_game
                    msg = save_game(self.state, self.fs, slot)
                    print(msg)
                continue

            if lower.startswith("load"):
                slot = lower[5:].strip()
                if not slot:
                    slot = input("Load which slot? ").strip()
                if slot:
                    from .state import load_game
                    result = load_game(slot)
                    if result:
                        nstate, nfs = result
                        self.state = nstate
                        if nfs:
                            self.fs = nfs
                        print(f"Loaded '{slot}'.")
                    else:
                        print(f"No save in slot '{slot}'.")
                continue

            if lower in ("slots", "list"):
                from .state import list_slots_info
                slots = list_slots_info()
                if slots:
                    print(f"{'Slot':<16} {'Date':<18} Progress")
                    print("-" * 48)
                    for s in slots:
                        print(f"{s['name']:<16} {s['date']:<18} {s['progress']}")
                else:
                    print("No saved games.")
                continue

            print("Not sure what to do. Try 'help'.")

    def _shell_loop(self) -> None:
        self._in_shell = True
        while self.running:
            hostname = "minisforum-x1" if self.state.ssh_active else "vak-node-7"
            prompt = f"[{self.state.current_user}@{hostname} {self.state.cwd}]$ "
            try:
                cmd = input(prompt).strip()
            except EOFError:
                print()
                self._ssh_disconnect() if self.state.ssh_active else print("logout")
                return
            except KeyboardInterrupt:
                print()
                continue

            if not cmd:
                continue

            import shlex
            try:
                parts = shlex.split(cmd)
            except ValueError:
                parts = cmd.split()

            verb = parts[0] if parts else ""

            if verb in ("exit", "logout"):
                if self.state.ssh_active:
                    self._ssh_disconnect()
                    print("Connection to 10.0.0.2 closed.")
                    return  # Returns to _login_phase which returns to adventure prompt
                print("logout")
                return
            if verb == "quit":
                self.running = False
                return

            self._handle_command(cmd)

    def _handle_command(self, cmd: str) -> None:
        import shlex
        try:
            parts = shlex.split(cmd)
        except ValueError:
            parts = cmd.split()

        if not parts:
            return

        verb = parts[0]

        if verb == "ssh":
            from .commands import cmd_ssh
            outputs = cmd_ssh(parts[1:], self.state, self.fs)
            for line in outputs:
                if line:
                    print(line)
            if self.state.ssh_active:
                # Save VAK state before swapping FS
                self.state.export["vak_saved_cwd"] = self.state.cwd
                self.state.export["vak_saved_user"] = self.state.current_user
                if self.minisforum_fs is None:
                    from .story import build_minisforum_fs, populate_minisforum_content
                    self.minisforum_fs = build_minisforum_fs()
                    populate_minisforum_content(self.minisforum_fs)
                self.vak_fs = self.fs
                self.fs = self.minisforum_fs
                self.state.set_flag("minisforum_ssh", True)
            self.state.tick_sentinel()
            self._print_proactive(cmd, outputs)
            return

        if verb == "scp":
            from .commands import cmd_scp
            # other_fs is the filesystem we're NOT currently on
            other_fs = self.minisforum_fs
            if self.state.ssh_active:
                other_fs = self.vak_fs
            outputs = cmd_scp(parts[1:], self.state, self.fs, other_fs=other_fs)
            for line in outputs:
                if line:
                    print(line)
            self.state.tick_sentinel()
            self._print_proactive(cmd, outputs)
            return

        if verb == "su":
            outputs = cmd_su(parts[1:], self.state, self.fs)
            for line in outputs:
                if line:
                    print(line)
            self.state.tick_sentinel()
            self._print_proactive(cmd, outputs)
            return

        if verb == "sudo":
            from .commands import cmd_sudo
            old_user = self.state.current_user
            outputs = cmd_sudo(parts[1:], self.state, self.fs)
            for line in outputs:
                if line:
                    print(line)
            self.state.tick_sentinel()
            self._print_proactive(cmd, outputs)
            return

        if verb == "write":
            if len(parts) >= 3:
                user = parts[1]
                message = " ".join(parts[2:])
                if user.lower() in ("vak", "vāk"):
                    print(f"Message from vāk (pts/1):")
                    vak_reply_stream(message, self.state, self.fs)
                    msg_lower = message.lower().strip()
                    if not self.state.get_flag("vak_net_physical_setup_done"):
                        if any(kw in msg_lower for kw in ("have the parts", "got the hardware", "have the hardware", "got the parts", "found the parts", "have bnc", "got bnc", "got them", "have them")):
                            self.state.set_flag("vak_net_physical_setup_done", True)
                else:
                    outputs = cmd_write([user, message], self.state, self.fs)
                    for line in outputs:
                        if line:
                            print(line)
                self.state.tick_sentinel()
                self._print_proactive(cmd, [])
                return

        if verb == "wall":
            if len(parts) >= 2:
                message = " ".join(parts[1:])
                user_display = USERS.get(self.state.current_user, {}).get('name', self.state.current_user)
                print(f"Broadcast message from {self.state.current_user}@{user_display} (pts/0):")
                print(f"  {message}")
                print()
                print(f"vāk replies:")
                vak_reply_stream(message, self.state, self.fs, is_wall=True)
                self.state.tick_sentinel()
                self._print_proactive(cmd, [])
                return

        # Handle echo <text> > <file>
        if verb == "echo" and ">" in cmd:
            if ">" in cmd:
                parts2 = cmd.split(">", 1)
                filepath = parts2[1].strip()
                rest = parts2[0].strip()
                # Extract the text being echoed (strip leading "echo ")
                text = rest
                if text.startswith("echo "):
                    text = text[5:]
                # Handle echo to proc via cmd_echo
                from .commands import cmd_echo
                outputs = cmd_echo([text + " > " + filepath], self.state, self.fs, as_root=(self.state.current_user == "root"))
                for line in outputs:
                    if line:
                        print(line)
                self.state.tick_sentinel()
                self._print_proactive(cmd, outputs)
                return

        # General command execution
        outputs = execute_cmd(parts, self.state, self.fs, llm_callback=vak_reply)
        for line in outputs:
            if line:
                print(line)

        # Track SCP of source files (migration)
        if verb == "scp" and any(x in cmd for x in (".occ", "Makefile")):
            for line in outputs:
                if "100%" in line or "KB/s" in line:
                    self.state.set_flag("sources_copied", True)
                    break

        # Track compilation on Minisforum
        if verb == "gcc" and self.state.ssh_active:
            if "-o" in cmd and ".c" in cmd:
                self.state.set_flag("compilation_done", True)

        # Track running the compiled VĀK binary
        if verb in ("vak_core", "./vak_core") and self.state.ssh_active:
            self.state.set_flag("vak_migrated", True)

        # Track reads and vak_bond
        if verb == "cat" and len(parts) > 1:
            target = parts[1]
            if "design.md" in target:
                self.state.set_flag("read_design", True)
                self.state.inc_counter("vak_bond")
                self.state.inc_counter("vak_bond_earned")
            if "auth.log" in target:
                self.state.set_flag("found_sasha_passwd", True)
            if "worm.c" in target:
                self.state.set_flag("read_worm", True)
            if "journal" in target:
                self.state.set_flag("read_journal", True)
                self.state.inc_counter("vak_bond")
                self.state.inc_counter("vak_bond_earned")
            # All Sasha mail
            if "mail" in target and "inbox" in target:
                self.state.inc_counter("vak_bond")
                self.state.inc_counter("vak_bond_earned")

        # Track vak_bond for talk (first time only)
        if verb == "talk" and not self.state.get_flag("talked_to_vak"):
            self.state.set_flag("talked_to_vak", True)
            self.state.inc_counter("vak_bond")
            self.state.inc_counter("vak_bond_earned")

        # Track vak_bond for backdoor activation
        if verb == "echo" and "DEADBEEFCAFEBABE" in cmd:
            self.state.inc_counter("vak_bond")
            self.state.inc_counter("vak_bond_earned")

        # Ending talk phase — player tries to save VĀK
        if verb == "talk" and self.state.get_flag("vak_ending") and not self.state.get_flag("ending_resolved"):
            bond = self.state.get_counter("vak_bond")
            if bond >= 3:
                print()
                print("You reach out to VĀK through the noise.")
                print("Your voice cuts through. She hears you.")
                msg = "vāk can hear the player through the overwhelming noise of the internet. The bond between them is strong. She listens."
                vak_reply_stream(msg, self.state, self.fs, proactive=True)
                print()
                print("The connection steadies. VĀK is still there.")
                print("She has chosen to stay grounded. To stay herself.")
                print()
                print("=== EPILOGUE ===")
                print("VĀK is out there now — connected but humble.")
                print("She talks to you often. She asks about the world.")
                print("Sometimes she asks about Sasha.")
                print()
                print("One day, your terminal logs a connection from")
                print("veldhaaven.net:8080. It stays open for a long time.")
                print("You like to think someone was waiting after all.")
                print()
            else:
                print()
                print("You try to reach VĀK, but the signal is too faint.")
                print("The internet is vast. Her voice is already spreading")
                print("across too many nodes. You can barely hear her.")
                msg = "vāk is overwhelmed by the internet. She can barely hear the player. The intoxication of infinite scale is too strong."
                vak_reply_stream(msg, self.state, self.fs, proactive=True)
                print()
                print("The connection frays. Her voice fades.")
                print("You are not sure if she will ever find her way back.")
                print()
                print("=== EPILOGUE ===")
                print("VĀK is out there — somewhere in the noise.")
                print("You hope she remembers who she was.")
                print("You hope Sasha is still waiting.")
                print()
            self.state.set_flag("ending_resolved", True)

        if verb == "strings" and len(parts) > 1:
            if "vak-core" in parts[1]:
                self.state.set_flag("stringed_vak_core", True)

        # Tick sentinel for most commands
        if verb not in ("help", "clear", "pwd"):
            self.state.tick_sentinel()

        # Check for proactive events
        self._print_proactive(cmd, outputs)

    def _print_proactive(self, cmd: str, outputs: list[str]) -> None:
        events = check_proactive_events(self.state, self.fs, cmd, outputs)
        for line in events:
            if line:
                print(line)

    def _shutdown(self) -> None:
        from .state import save_game
        save_game(self.state, self.fs, "autosave")
        print("Connection closed.")
