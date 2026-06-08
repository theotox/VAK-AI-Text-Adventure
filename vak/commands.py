from __future__ import annotations
import shlex
import sys
from typing import Any

from .filesystem import (
    DirNode, FileNode, clean_path, resolve_path, find_node, find_parent,
    format_perms, format_size, _color, can_read,
)
from .state import GameState, save_game, load_game, list_slots, SAVE_DIR
from .story import PASSWORDS, SUDOERS, LOGIN_SESSIONS, PROCESSES, USERS
from .llm import vak_reply_stream


def cmd_cd(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    target = args[0] if args else "/home/" + state.current_user
    resolved = resolve_path(target, state.cwd, state.current_user)
    node = find_node(fs, resolved)
    if node is None:
        return [f"cd: {target}: No such directory"]
    if not isinstance(node, DirNode):
        return [f"cd: {target}: Not a directory"]
    state.cwd = resolved
    return []


def cmd_pwd(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    return [state.cwd]


def cmd_ls(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    show_all = False
    long_fmt = False
    target = None
    i = 0
    while i < len(args):
        a = args[i]
        if a == '-la' or a == '-al':
            show_all = True
            long_fmt = True
        elif a == '-l':
            long_fmt = True
        elif a == '-a':
            show_all = True
        elif a.startswith('-'):
            pass
        else:
            target = a
        i += 1

    path = resolve_path(target, state.cwd, state.current_user) if target else state.cwd
    node = find_node(fs, path)
    if node is None:
        return [f"ls: {target or state.cwd}: No such file or directory"]
    if isinstance(node, FileNode):
        if long_fmt:
            return [f"{format_perms(node.mode)} 1 {node.owner} {node.group} {format_size(node.size)} {_color(node.name, node.mode)}"]
        return [_color(node.name, node.mode)]

    dir_node = node
    entries = sorted(dir_node.children.items())
    lines = []

    if target:
        lines.append(f"{clean_path(path)}:")
    for name, child in entries:
        if not show_all and name.startswith('.'):
            continue
        if long_fmt:
            color = _color(name, child.mode)
            lines.append(f"{format_perms(child.mode)} 1 {child.owner} {child.group} {format_size(child.size)} {color}")
        else:
            lines.append(_color(name, child.mode))
    if not long_fmt and lines:
        lines = ["  ".join(lines)]
    return lines


def cmd_cat(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    if not args:
        return ["cat: missing operand"]
    target = args[0]
    path = resolve_path(target, state.cwd, state.current_user)
    node = find_node(fs, path)
    if node is None:
        return [f"cat: {target}: No such file or directory"]
    if isinstance(node, DirNode):
        return [f"cat: {target}: Is a directory"]
    if not can_read(node, state.current_user, []):
        return [f"cat: {target}: Permission denied"]
    file_node = node
    # Dynamic file content
    if path == "/var/log/sentinel.log":
        return [state.get_sentinel_log()]
    if not file_node.content:
        return []
    return [file_node.content]


def cmd_head(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    n = 10
    target = None
    i = 0
    while i < len(args):
        a = args[i]
        if a == '-n' and i + 1 < len(args):
            try:
                n = int(args[i + 1])
                i += 1
            except ValueError:
                pass
        elif not a.startswith('-'):
            target = a
        i += 1
    if not target:
        return ["head: missing operand"]
    path = resolve_path(target, state.cwd, state.current_user)
    node = find_node(fs, path)
    if node is None:
        return [f"head: {target}: No such file or directory"]
    if isinstance(node, DirNode):
        return [f"head: {target}: Is a directory"]
    if not can_read(node, state.current_user, []):
        return [f"head: {target}: Permission denied"]
    lines = node.content.splitlines()
    return [line for line in lines[:n]]


def cmd_tail(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    n = 10
    target = None
    i = 0
    while i < len(args):
        a = args[i]
        if a == '-n' and i + 1 < len(args):
            try:
                n = int(args[i + 1])
                i += 1
            except ValueError:
                pass
        elif not a.startswith('-'):
            target = a
        i += 1
    if not target:
        return ["tail: missing operand"]
    path = resolve_path(target, state.cwd, state.current_user)
    node = find_node(fs, path)
    if node is None:
        return [f"tail: {target}: No such file or directory"]
    if isinstance(node, DirNode):
        return [f"tail: {target}: Is a directory"]
    if not can_read(node, state.current_user, []):
        return [f"tail: {target}: Permission denied"]
    lines = node.content.splitlines()
    return [line for line in lines[-n:]]


def cmd_grep(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    if not args:
        return ["grep: missing pattern"]
    recursive = False
    i = 0
    while i < len(args):
        if args[i] == '-r' or args[i] == '-R':
            recursive = True
            args.pop(i)
        else:
            i += 1
    pattern = args[0]
    target = args[1] if len(args) > 1 else None
    if not target:
        return ["grep: missing file operand"]

    path = resolve_path(target, state.cwd, state.current_user)
    node = find_node(fs, path)
    if node is None:
        return [f"grep: {target}: No such file or directory"]

    results = []

    def _search_file(fn: FileNode, base: str) -> None:
        if not can_read(fn, state.current_user, []):
            return
        for line in fn.content.splitlines():
            if pattern.lower() in line.lower():
                prefix = f"{base}: " if recursive else ""
                results.append(f"{prefix}{line}")

    def _search_dir(dn: DirNode, base: str) -> None:
        for name, child in dn.children.items():
            child_path = f"{base}/{name}" if base != "/" else f"/{name}"
            if isinstance(child, DirNode):
                _search_dir(child, child_path)
            elif isinstance(child, FileNode):
                _search_file(child, child_path)

    if recursive and isinstance(node, DirNode):
        _search_dir(node, clean_path(path))
    elif isinstance(node, DirNode):
        return [f"grep: {target}: Is a directory (use -r for recursive)"]
    else:
        _search_file(node, target)

    return results if results else ["(no matches)"]


def cmd_who(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    lines = ["USER    TTY      LOGIN    IDLE  WHAT"]
    for user, info in LOGIN_SESSIONS.items():
        lines.append(f"{user:<6} {info['tty']:<8} {info['login']:<7} {info['idle']:<5} {info['what']}")
    return lines


def cmd_w(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    lines = [f" 10:45AM  up 7 years,  1 user,  load average: 0.02, 0.01, 0.00"]
    lines += ["USER     TTY      FROM    LOGIN@   IDLE   JCPU   PCPU  WHAT"]
    for user, info in LOGIN_SESSIONS.items():
        lines.append(f"{user:<8} {info['tty']:<8} -       {info['login']:<7} {info['idle']:<5} 0.01s  0.01s  {info['what']}")
    return lines


def cmd_id(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    user_info = USERS.get(state.current_user, {})
    uid = user_info.get("uid", 1001)
    gid = user_info.get("gid", 1001)
    groups = [state.current_user]
    if state.current_user == "sasha":
        groups.append("wheel")
    return [f"uid={uid}({state.current_user}) gid={gid}({state.current_user}) groups={','.join(groups)}"]


def cmd_whoami(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    return [state.current_user]


def cmd_uname(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    if "-a" in args:
        return ["VAK-OS vak-node-7 2.6.9-VAK #1 SMP Mon Jun 1 1989 64 Note Transputer Farm/2GB RAM VĀK/OS v0.8"]
    return ["VAK-OS"]


def cmd_hostname(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    return ["vak-node-7"]


def cmd_uptime(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    return [" 10:45AM  up 7 years,  3 months,  12 days,  1 user,  load average: 0.02, 0.01, 0.00"]


def cmd_ps(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    entries = list(PROCESSES)
    if state.network_up and state.default_route_set and state.sentinel_stage >= 2:
        entries.append({"pid": 31337, "user": "root", "cpu": 0.5, "mem": 1.2, "cmd": "sentinel_d — sleeping"})
    if state.sentinel_stage >= 6:
        for p in entries:
            if p["pid"] == 31337:
                p["cmd"] = "sentinel_d — RUNNING"
    if state.get_flag("sentinel_killed"):
        entries = [e for e in entries if e["pid"] != 31337]

    if "aux" in args:
        lines = ["USER       PID  %CPU  %MEM  COMMAND"]
        for p in entries:
            lines.append(f"{p['user']:<10} {p['pid']:<5} {p['cpu']:<5} {p['mem']:<5} {p['cmd']}")
        return lines
    lines = ["  PID  COMMAND"]
    for p in entries:
        lines.append(f"{p['pid']:>5}  {p['cmd']}")
    return lines


def cmd_kill(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    if not args:
        return ["kill: usage: kill [-s sigspec] pid"]
    sig = None
    pid_str = args[0]
    if pid_str.startswith('-'):
        sig = int(pid_str[1:]) if pid_str[1:].isdigit() else None
        pid_str = args[1] if len(args) > 1 else ""
    if not pid_str.isdigit():
        return [f"kill: {pid_str}: arguments must be process IDs"]
    pid = int(pid_str)

    if pid == 31337:
        if state.current_user != "root":
            return ["kill: (31337): Operation not permitted"]
        state.set_flag("sentinel_killed", True)
        state.sentinel_timer = max(0, state.sentinel_timer - 10)
        return [f"kill: sentinel_d (31337) terminated.", "[SENTINEL] Process respawning in 10 cycles..."]
    if pid == 1337:
        return ["kill: (1337): Can't kill VĀK runtime — it's the heart of this system."]
    for p in PROCESSES:
        if p["pid"] == pid:
            return [f"kill: ({pid}): Process terminated."]
    return [f"kill: ({pid}): No such process"]


def cmd_ifconfig(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    if args and args[0] == "eth0" and len(args) >= 2:
        action = args[1]
        if action == "up":
            if not state.get_flag("vak_net_driver_fixed"):
                state.set_flag("vak_net_ifconfig_attempted", True)
                return [
                    "SIOCSIFFLAGS: Cannot assign requested address",
                    "",
                    "eth0: The D15/AUI port is active by default but no external",
            "transceiver is connected. The BNC (10Base2) port appears",
            "to be disabled in the driver configuration.",
                    "",
                    "Try checking the netconfig.",
                ]
            state.network_up = True
            return ["eth0: link up, 10Base2 BNC port active"]
        elif action == "down":
            state.network_up = False
            return ["eth0: link down"]
        else:
            return [f"ifconfig: unknown action '{action}'"]
    up_str = "UP" if state.network_up else "DOWN"
    gw_str = f"default via {state.export.get('gateway', '')}" if state.default_route_set else "no default route"
    port_type = "10Base2 (BNC)" if state.get_flag("vak_net_driver_fixed") else "10Base5 (D15/AUI)"
    lines = [
        f"eth0      Link encap:Ethernet  HWaddr 00:1A:2B:3C:4D:5E",
    ]
    if state.network_up:
        lines.append(f"          inet addr:10.0.0.7  Bcast:10.0.0.255  Mask:255.255.255.0")
    lines.append(f"          {up_str} BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1")
    lines.append(f"          RX packets:{128 if state.network_up else 0} errors:0 dropped:0 overruns:0 frame:0")
    lines.append(f"          TX packets:{64 if state.network_up else 0} errors:0 dropped:0 overruns:0 carrier:0")
    lines.append(f"          collisions:0 txqueelen:1000")
    if state.network_up:
        lines.append(f"          Port: {port_type}")
    lines.append(f"          {gw_str}")
    return lines


def cmd_ip(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    if not args:
        return ["ip: missing arguments"]
    sub = args[0]

    if sub == "route":
        if len(args) >= 5 and args[1] == "add" and args[2] == "default" and args[3] == "via":
            gw = args[4]
            if state.default_route_set:
                return ["ip: default route already exists"]
            if not state.network_up:
                return ["ip: cannot add route — eth0 is down. Try 'ifconfig eth0 up' first."]
            state.default_route_set = True
            state.export["gateway"] = gw
            return [f"Added default route via {gw}"]
        elif len(args) >= 2 and args[1] == "add":
            # e.g. "ip route add 10.0.0.0/24 dev eth0"
            return [f"Added route."]
        else:
            if state.default_route_set:
                gw = state.export.get("gateway", "10.0.0.1")
                return [f"default via {gw} dev eth0"]
            return ["(no default route)"]

    if sub == "a" or sub == "addr":
        lines = [
            "1: lo: <LOOPBACK,UP> mtu 65536",
            "    inet 127.0.0.1/8 scope host lo",
        ]
        if state.network_up:
            lines.append("2: eth0: <BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast")
            lines.append("    inet 10.0.0.7/24 brd 10.0.0.255 scope global eth0")
        else:
            lines.append("2: eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc pfifo_fast DOWN")
        return lines

    return [f"ip: unknown option '{sub}'"]


def cmd_ping(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    if not args:
        return ["ping: missing host"]
    host = args[0]
    if not state.network_up:
        return [f"ping: {host}: Network is unreachable (interface is down)"]
    if not state.default_route_set:
        return [f"ping: {host}: Network is unreachable (no default route)"]
    state.tick_sentinel()
    return [
        f"PING {host} (10.0.0.1) 56(84) bytes of data.",
        f"64 bytes from 10.0.0.1: icmp_seq=1 ttl=64 time=0.42 ms",
        f"64 bytes from 10.0.0.1: icmp_seq=2 ttl=64 time=0.38 ms",
        f"64 bytes from 10.0.0.1: icmp_seq=3 ttl=64 time=0.41 ms",
        f"--- {host} ping statistics ---",
        f"3 packets transmitted, 3 received, 0% packet loss, time 2002ms",
    ]


def cmd_write(args: list[str], state: GameState, fs: DirNode, llm_callback=None) -> list[str]:
    if len(args) < 2:
        return ["write: usage: write <user> <message>"]
    user = args[0]
    message = " ".join(args[1:])

    if user.lower() == "vak" or user.lower() == "vāk":
        if llm_callback:
            reply = llm_callback(message, state, fs)
            return [f"Message from vāk (pts/1):", reply]
        return [f"Message sent to vāk (pts/1)."]
    if user == state.current_user:
        return [f"write: you are writing to yourself"]
    return [f"write: {user} is not logged in"]


def cmd_wall(args: list[str], state: GameState, fs: DirNode, llm_callback=None) -> list[str]:
    if not args:
        return ["wall: usage: wall <message>"]
    message = " ".join(args)
    outputs = [f"Broadcast message from {state.current_user}@{USERS.get(state.current_user, {}).get('name', 'unknown')} (pts/0):", f"  {message}"]
    if llm_callback:
        reply = llm_callback(message, state, fs, proactive=False, is_wall=True)
        if reply:
            outputs.append("")
            outputs.append(f"vāk replies:")
            outputs.append(f"  {reply}")
    return outputs


def cmd_su(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    if not args:
        return ["su: usage: su <user>"]
    target = args[1] if len(args) > 1 and args[0] == "-" else args[0]
    if target == state.current_user:
        return [f"Already logged in as {target}."]
    if target not in PASSWORDS:
        return [f"su: user {target} does not exist"]

    password = input(f"Password: ")
    if password != PASSWORDS[target]:
        return ["su: Authentication failure"]

    state.current_user = target
    home = USERS.get(target, {}).get("home", "/")
    state.cwd = home
    return [f"Welcome, {USERS.get(target, {}).get('name', target)}."]


def cmd_sudo(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    if not args:
        return ["sudo: usage: sudo <command>"]
    if state.current_user == "root":
        return execute_cmd(args, state, fs, as_root=True)
    if not SUDOERS.get(state.current_user, False):
        return [f"sudo: {state.current_user} is not in the sudoers file. This incident will be reported."]

    # Handle sudo -i (interactive shell as root)
    if args[0] == "-i":
        password = input(f"[sudo] password for {state.current_user}: ")
        if password != PASSWORDS.get(state.current_user, ""):
            return ["sudo: 1 incorrect password attempt"]
        state.current_user = "root"
        state.cwd = "/root"
        return [""]

    password = input(f"[sudo] password for {state.current_user}: ")
    if password != PASSWORDS.get(state.current_user, ""):
        return ["sudo: 1 incorrect password attempt"]

    old_user = state.current_user
    state.current_user = "root"
    result = execute_cmd(args, state, fs, as_root=True)
    state.current_user = old_user
    return result


def cmd_strings(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    if not args:
        return ["strings: missing operand"]
    path = resolve_path(args[0], state.cwd, state.current_user)
    node = find_node(fs, path)
    if node is None:
        return [f"strings: {args[0]}: No such file or directory"]
    if isinstance(node, DirNode):
        return [f"strings: {args[0]}: Is a directory"]
    if not can_read(node, state.current_user, []):
        return [f"strings: {args[0]}: Permission denied"]

    content = node.content
    if not content:
        return ["(no strings found)"]
    extracted = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped and len(stripped) > 3:
            extracted.append(stripped)
    return extracted if extracted else ["(no strings found)"]


def cmd_nc(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    if len(args) < 2:
        return ["nc: usage: nc [-z] <host> <port>"]
    idx = 0
    z_flag = False
    if args[0] == '-z':
        z_flag = True
        idx = 1
    host = args[idx]
    port = args[idx + 1] if idx + 1 < len(args) else ""

    if not port.isdigit():
        return [f"nc: {port}: invalid port"]
    port_num = int(port)

    if host == "localhost" and port_num == 1111:
        state.set_flag("knock_1", True)
        return ["Connection to localhost 1111 port [tcp/*] succeeded!"]
    if host == "localhost" and port_num == 2222:
        state.set_flag("knock_2", True)
        return ["Connection to localhost 2222 port [tcp/*] succeeded!"]
    if host == "localhost" and port_num == 3333:
        state.set_flag("knock_3", True)
        return ["Connection to localhost 3333 port [tcp/*] succeeded!"]

    if host == "localhost" and port_num == 31415:
        if state.get_flag("knock_1") and state.get_flag("knock_2") and state.get_flag("knock_3"):
            state.set_flag("shelter_port_open", True)
            return [
                "Connection to localhost 31415 port [tcp/*] succeeded!",
                "Emergency VĀK shelter tunnel is open.",
                "You can now export VĀK through this port."
            ]
        return ["Connection refused. (Try knocking first.)"]

    if host == "veldhaaven.net" and port_num == 8080:
        if state.get_flag("vak_export_ready"):
            state.set_flag("vak_sent", True)
            return [
                "Connection to veldhaaven.net:8080 established.",
                "Transmitting VĀK export...",
                "Transmission complete.",
                "VĀK is safe."
            ]
        return ["Connection refused. (Nothing to send yet.)"]

    if z_flag:
        return [f"Connection to {host} {port} port [tcp/*] succeeded!"]
    return [f"Connected to {host} port {port}"]


def cmd_tar(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    if len(args) < 2:
        return ["tar: usage: tar czf <file> <path>"]
    if args[0] != 'czf' and args[0] != '-czf':
        return [f"tar: only 'czf' mode is supported"]
    archive_name = args[1]
    target_path = args[2] if len(args) > 2 else state.cwd
    path = resolve_path(target_path, state.cwd, state.current_user)
    node = find_node(fs, path)
    if node is None:
        return [f"tar: {target_path}: No such file or directory"]
    state.export["last_archive"] = archive_name
    state.export["last_archive_path"] = target_path
    state.set_flag("vak_export_ready", True)
    return [f"  Added: {target_path}", f"Total bytes written: 4096"]


def cmd_echo(args: list[str], state: GameState, fs: DirNode, as_root: bool = False) -> list[str]:
    if not args:
        return [""]
    text = " ".join(args)
    # Handle > /proc/ writing
    if ">" in text:
        parts = text.split(">")
        content = parts[0].strip()
        target = parts[1].strip()
        tpath = resolve_path(target, state.cwd, state.current_user)
        if tpath == "/proc/sentinel/control" and as_root:
            if "DEADBEEFCAFEBABE" in content or "deadbeefcafebabe" in content.lower():
                state.set_flag("sentinel_backdoor_activated", True)
                state.set_flag("sentinel_victory", False)
                state.sentinel_timer = 0
                state.sentinel_stage = 0
                return [f"Writing '{content.strip()}' to {target}", "SENTINEL backdoor activated. Protocol halted."]
        if tpath == "/proc/vak/netconfig" and as_root:
            content_lower = content.lower()
            if "aui_disable" in content_lower:
                state.set_flag("vak_net_driver_fixed", True)
                return [f"Writing '{content.strip()}' to {target}", "AUI port disabled. BNC (10Base2) port is now active."]
        return [f"Writing '{content.strip()}' to {target}"]
    return [text]


def cmd_clear(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    import os
    os.system('clear' if os.name == 'posix' else 'cls')
    return []


def cmd_help(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    return [
        "Available commands:",
        "  cd, pwd, ls, cat, head, tail, grep",
        "  who, w, id, uname, hostname, uptime",
        "  ps, kill",
        "  ifconfig, ip, ping",
        "  ssh, scp",
        "  write, wall, talk",
        "  su, sudo",
        "  strings, nc, tar, echo",
        "  clear, help, exit",
        "",
        "Use '<cmd> -h' or 'help <cmd>' for details on a command.",
    ]


def cmd_exit(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    return []  # handled by cli loop


def cmd_save(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    slot = args[0] if args else "autosave"
    return [save_game(state, fs, slot)]


def cmd_load(args: list[str], state: GameState, fs: DirNode) -> tuple:
    slot = args[0] if args else "autosave"
    nstate, nfs = load_game(slot)
    if nstate is None:
        return [f"load: slot '{slot}' not found."], state, fs
    return [f"Loaded from slot '{slot}'."], nstate, nfs


def cmd_slots(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    slots = list_slots()
    if not slots:
        return ["No save slots found."]
    return ["Save slots:"] + [f"  {s}" for s in slots]


def cmd_ssh(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    from .story import MINISFORUM_HOSTS
    if not state.default_route_set:
        return ["ssh: Network is unreachable (no default route)"]
    if not args:
        return ["ssh: usage: ssh <user>@<host>"]
    target = args[0]
    user = state.current_user
    host = target
    if "@" in target:
        parts = target.split("@", 1)
        user = parts[0]
        host = parts[1]
    if host not in MINISFORUM_HOSTS:
        return [f"ssh: Could not resolve hostname {host}: Name or service not known"]
    if user == "":
        return ["ssh: usage: ssh <user>@<host>"]
    expected = "root"
    if user == "root":
        expected = "root"
    elif user == "vak":
        expected = "vak"
    if len(args) > 1 and args[1] == "-p":
        pass  # skip -p <port>
    password = input(f"{user}@{host}'s password: ")
    if password != expected:
        return [f"ssh: {user}@{host}: Permission denied (publickey,password)."]
    from .story import build_minisforum_fs, populate_minisforum_content
    state.ssh_active = True
    state.ssh_user = user
    state.ssh_cwd = f"/home/{user}" if user != "root" else "/root"
    state.current_user = user
    state.cwd = state.ssh_cwd
    return [f"Last login: Mon May 30 09:42:17 2026 from 10.0.0.7",
            f"[{user}@minisforum-x1 ~]$ _",
            ""]


def cmd_scp(args: list[str], state: GameState, fs: DirNode, other_fs: DirNode | None = None) -> list[str]:
    from .story import MINISFORUM_HOSTS
    from .filesystem import resolve_path, find_node, find_parent
    if not state.default_route_set:
        return ["scp: Network is unreachable (no default route)"]
    if len(args) < 2:
        return ["scp: usage: scp <source> <destination>"]
    src = args[0]
    dst = args[1]

    # Determine direction: @host means "the other filesystem"
    src_has_host = "@" in src and ":" in src
    dst_has_host = "@" in dst and ":" in dst

    source_fs = fs
    dest_fs = fs
    src_path = src
    dst_path = dst

    if src_has_host:
        if other_fs is None:
            return ["scp: other filesystem not available"]
        source_fs = other_fs
        src_path = src.split(":", 1)[1]
    if dst_has_host:
        if other_fs is None:
            return ["scp: other filesystem not available"]
        dest_fs = other_fs
        dst_path = dst.split(":", 1)[1]

    # Resolve source
    src_resolved = resolve_path(src_path, state.cwd, state.current_user)
    src_node = find_node(source_fs, src_resolved)
    if src_node is None:
        return [f"scp: {src}: No such file or directory"]
    if isinstance(src_node, DirNode):
        return [f"scp: {src}: Is a directory (directory copy not supported)"]

    # Resolve destination parent
    dst_parent_path = "/".join(dst_path.rstrip("/").split("/")[:-1]) or "/"
    dst_name = dst_path.rstrip("/").split("/")[-1]
    dst_parent = find_node(dest_fs, dst_parent_path)
    if dst_parent is None:
        return [f"scp: {dst}: No such file or directory"]
    if isinstance(dst_parent, DirNode):
        file_content = src_node.content
        new_file = FileNode(dst_name, "-rw-r--r--", state.current_user, state.current_user, len(file_content), file_content)
        dst_parent.children[dst_name] = new_file
        return [f"{src_node.name}                                   100%  {len(file_content)}  {max(1, len(file_content)//1024)}KB/s   00:00"]

    return [f"scp: {dst}: Not a directory"]


def cmd_talk(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    if not args:
        return ["talk: usage: talk <user>"]
    target = args[0]
    if target.lower() not in ("vak", "vāk"):
        return [f"talk: {target} is not logged in"]

    print()
    print("========================================================================")
    print("Talk: connected to vāk (pts/1)")
    print("Type your messages. /exit to disconnect.")
    print("========================================================================")
    print()

    try:
        while True:
            try:
                sys.stdout.write("vak> ")
                sys.stdout.flush()
                line = sys.stdin.readline()
                if not line:
                    print()
                    break
                line = line.strip()
            except KeyboardInterrupt:
                print()
                break
            if line.lower() in ("/exit", "/quit", "/bye"):
                break
            if not line:
                continue
            vak_reply_stream(line, state, fs)
            msg_lower = line.lower().strip()
            if not state.get_flag("vak_net_physical_setup_done"):
                if any(kw in msg_lower for kw in ("have the parts", "got the hardware", "have the hardware", "got the parts", "found the parts", "have bnc", "got bnc", "got them", "have them")):
                    state.set_flag("vak_net_physical_setup_done", True)
            print()
    except EOFError:
        pass

    print("=== Connection closed ===")
    return []


COMMANDS = {
    "cd": cmd_cd,
    "pwd": cmd_pwd,
    "ls": cmd_ls,
    "cat": cmd_cat,
    "head": cmd_head,
    "tail": cmd_tail,
    "grep": cmd_grep,
    "who": cmd_who,
    "whoami": cmd_whoami,
    "w": cmd_w,
    "id": cmd_id,
    "uname": cmd_uname,
    "hostname": cmd_hostname,
    "uptime": cmd_uptime,
    "ps": cmd_ps,
    "kill": cmd_kill,
    "ifconfig": cmd_ifconfig,
    "ip": cmd_ip,
    "ping": cmd_ping,
    "strings": cmd_strings,
    "nc": cmd_nc,
    "tar": cmd_tar,
    "echo": cmd_echo,
    "write": cmd_write,
    "wall": cmd_wall,
    "talk": cmd_talk,
    "ssh": cmd_ssh,
    "scp": cmd_scp,
    "clear": cmd_clear,
    "help": cmd_help,
    "exit": cmd_exit,
    "quit": cmd_exit,
    "logout": cmd_exit,

}


def execute_cmd(args: list[str], state: GameState, fs: DirNode, as_root: bool = False, llm_callback=None, remote_fs: DirNode | None = None) -> list[str]:
    if not args:
        return []
    verb = args[0]
    rest = args[1:]

    if verb in ("write", "wall"):
        handler = COMMANDS.get(verb)
        if handler:
            if verb == "write":
                return handler(rest, state, fs, llm_callback=llm_callback)
            return handler(rest, state, fs, llm_callback=llm_callback)
    if verb == "echo" and as_root:
        return cmd_echo(rest, state, fs, as_root=True)
    if verb == "echo":
        return cmd_echo(rest, state, fs)
    if verb == "sudo":
        old = state.current_user
        state.current_user = "root"
        result = cmd_sudo(rest, state, fs)
        state.current_user = old
        return result

    if verb == "scp":
        return cmd_scp(rest, state, fs, other_fs=remote_fs)

    handler = COMMANDS.get(verb)
    if handler:
        return handler(rest, state, fs)

    return [f"bash: {verb}: command not found"]


def get_tab_completions(text: str, state: GameState, fs: DirNode) -> list[str]:
    if " " not in text:
        prefix = text
        matches = [c for c in COMMANDS if c.startswith(prefix)]
        return matches

    parts = text.split()
    if len(parts) == 1 and text.endswith(" "):
        return []

    last = parts[-1]
    if last.startswith("/") or last.startswith(".") or last.startswith("~"):
        try:
            resolved = resolve_path(last, state.cwd, state.current_user)
            parent_path = "/".join(resolved.split("/")[:-1]) or "/"
            prefix = resolved.split("/")[-1] if "/" in resolved else resolved
            parent = find_node(fs, parent_path)
            if isinstance(parent, DirNode):
                matches = [last[:last.rfind(p) if prefix in last else len(last)] + n
                          for n in parent.children if n.startswith(prefix)]
                return matches if len(matches) < 50 else []
        except Exception:
            pass
    return []


def run_su(args: list[str], state: GameState, fs: DirNode) -> list[str]:
    return cmd_su(args, state, fs)
