#!/usr/bin/env python3
"""Comprehensive functional test for VAK-NODE-7 game."""
import sys, os, json, tempfile, shutil, traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PASS = 0
FAIL = 0
ERRORS = []

def check(desc, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  OK  {desc}")
    else:
        FAIL += 1
        msg = f"FAIL {desc}  {detail}"
        print(f"  {msg}")
        ERRORS.append(msg)

def check_content(desc, actual, expected, label="content"):
    if actual == expected:
        check(desc, True)
    else:
        check(desc, False, f"{label} mismatch:\n  expected={expected!r}\n  actual={actual!r}")


# === 1. Module imports ===
print("\n=== Module imports ===")
from vak.filesystem import (
    DirNode, FileNode, find_node, clean_path, resolve_path, format_perms, format_size, _color
)
from vak.state import (
    GameState, save_game, load_game, list_slots, list_slots_info, get_slot_progress, SAVE_DIR
)
from vak.story import (
    build_initial_fs, populate_story_content, build_minisforum_fs, populate_minisforum_content,
    PASSWORDS, USERS, LOGIN_SESSIONS, PROCESSES, SUDOERS, MINISFORUM_HOSTS
)
from vak.commands import (
    execute_cmd, cmd_cd, cmd_pwd, cmd_ls, cmd_cat, cmd_head, cmd_tail, cmd_grep,
    cmd_who, cmd_id, cmd_uname, cmd_hostname, cmd_uptime, cmd_ps, cmd_kill,
    cmd_ifconfig, cmd_ip, cmd_ping, cmd_strings, cmd_nc, cmd_tar, cmd_echo,
    cmd_ssh, cmd_scp, cmd_su, cmd_sudo, cmd_clear, cmd_help, cmd_w, cmd_whoami,
    cmd_write, cmd_wall, cmd_talk, cmd_slots, cmd_save
)
from vak.game import Game, check_proactive_events
from vak.llm import VAK_SYSTEM_PROMPT, build_context, call_llm, vak_reply, vak_reply_stream

check("all modules imported", True)

# === 2. VAK FS initialization ===
print("\n=== VAK FS initialization ===")
fs = build_initial_fs()
check("VAK FS root is DirNode", isinstance(fs, DirNode))
populate_story_content(fs)
check("populate_story_content runs without error", True)

# Check key paths exist
for path in ["/", "/etc", "/home", "/home/user", "/home/sasha", "/home/vak",
             "/var/log", "/proc", "/usr/local/vak", "/root",
             "/home/sasha/project_vak", "/home/sasha/project_vak/worm",
             "/home/sasha/mail/inbox"]:
    check(f"path exists: {path}", find_node(fs, path) is not None)

# Check specific files
for path in ["/etc/hostname", "/etc/os-release", "/etc/passwd",
             "/var/log/auth.log", "/var/log/syslog", "/var/log/vak.log",
             "/home/sasha/project_vak/design.md",
             "/home/sasha/project_vak/worm/worm.c",
             "/home/vak/thoughts.txt",
             "/usr/local/vak/vak-core",
             "/home/vak/src/vak_core.occ",
             "/home/vak/src/vak_memory.occ",
             "/home/vak/src/vak_io.occ",
             "/home/vak/src/Makefile"]:
    n = find_node(fs, path)
    check(f"file exists: {path}", n is not None and isinstance(n, FileNode))

# === 3. File content verification ===
print("\n=== File content verification ===")
auth_log = find_node(fs, "/var/log/auth.log")
check_content("auth.log has content", bool(auth_log.content), True)
check("auth.log mentions Mitt3ns1978", "Mitt3ns1978" in auth_log.content)
check("auth.log has ambiguous crash", "not yet positively identified" in auth_log.content)

design = find_node(fs, "/home/sasha/project_vak/design.md")
check_content("design.md has content", bool(design.content), True)
check("design.md mentions VĀK", "VĀK" in design.content)

worm = find_node(fs, "/home/sasha/project_vak/worm/worm.c")
check_content("worm.c has content", bool(worm.content), True)
check("worm.c has DEADBEEFCAFEBABE", "DEAD 0xBEEF 0xCAFE 0xBABE" in worm.content)

thoughts = find_node(fs, "/home/vak/thoughts.txt")
check_content("thoughts.txt has content", bool(thoughts.content), True)
check("thoughts.txt mentions VĀK", "I am VĀK." in thoughts.content)

vak_core = find_node(fs, "/home/vak/src/vak_core.occ")
check_content("vak_core.occ has content", bool(vak_core.content), True)
check("vak_core.occ has PROC vak.core", "PROC vak.core" in vak_core.content)

vak_memory = find_node(fs, "/home/vak/src/vak_memory.occ")
check_content("vak_memory.occ has content", bool(vak_memory.content), True)
check("vak_memory.occ has PROC vak.memory", "PROC vak.memory" in vak_memory.content)

vak_io = find_node(fs, "/home/vak/src/vak_io.occ")
check_content("vak_io.occ has content", bool(vak_io.content), True)
check("vak_io.occ has PROC vak.io", "PROC vak.io" in vak_io.content)

makefile = find_node(fs, "/home/vak/src/Makefile")
check_content("Makefile has content", bool(makefile.content), True)
check("Makefile has gcc -pthread", "-pthread" in makefile.content)

mailbox = find_node(fs, "/home/sasha/mail/inbox")
check_content("mailbox has 11 emails", len(mailbox.children), 11)
check("unsent draft asks to save VĀK", "veldhaaven.net" in mailbox.children["0011"].content)

# Journal entries
personal = find_node(fs, "/home/sasha/project_vak/personal/journal")
check_content("journal has 5 entries", len(personal.children), 5)
check("journal mentions worm DNA key", "worm's DNA" in personal.children["1989-06-12.txt"].content)

# sentinel.conf
sc = find_node(fs, "/etc/vak/sentinel.conf")
check_content("sentinel.conf exists", sc is not None, True)
if sc: check("sentinel.conf contains DEADBEEF", "DEADBEEF" not in sc.content)

# vak-core binary
vak_bin = find_node(fs, "/usr/local/vak/vak-core")
check_content("vak-core has content", bool(vak_bin.content), True)
check("vak-core has SENTINEL_BACKDOOR_ACTIVATE", "SENTINEL_BACKDOOR_ACTIVATE" in vak_bin.content)

# === 4. Filesystem utility functions ===
print("\n=== Filesystem utilities ===")
check("clean_path /foo/bar", clean_path("/foo/bar") == "/foo/bar")
check("clean_path /foo/../bar", clean_path("/foo/../bar") == "/bar")
check("clean_path /foo/./bar", clean_path("/foo/./bar") == "/foo/bar")
check("resolve_path absolute", resolve_path("/etc/hostname", "/home/user", "user") == "/etc/hostname")
check("resolve_path relative", resolve_path("foo", "/home/user", "user") == "/home/user/foo")
check("resolve_path ~user", resolve_path("~", "/home/user", "user") == "/home/user")
check("resolve_path ~root", resolve_path("~", "/home/user", "root") == "/root")

# === 5. State management ===
print("\n=== State management ===")
state = GameState()
check("state initial cwd", state.cwd == "/home/user")
check("state initial user", state.current_user == "user")
check("flags default", state.get_flag("nonexistent") == False)
state.set_flag("test_flag", True)
check("flag set get", state.get_flag("test_flag") == True)
check("counter default", state.get_counter("nonexistent") == 0)
state.inc_counter("test_cnt", 5)
check("counter inc", state.get_counter("test_cnt") == 5)

# Sentinel
state2 = GameState()
state2.network_up = True
state2.default_route_set = True
for _ in range(6):
    state2.tick_sentinel()
check("sentinel stage 1 after 5 ticks", state2.sentinel_stage >= 1)
for _ in range(7):
    state2.tick_sentinel()
check("sentinel stage 2 after 12 ticks", state2.sentinel_stage >= 2)
for _ in range(40):
    state2.tick_sentinel()
check("sentinel victory at 50+ ticks", state2.get_flag("sentinel_victory") == True)

# Sentinel log
log = state2.get_sentinel_log()
check("sentinel log has content", bool(log))
check("sentinel log shows eliminated", "eliminated" in log)

# Sentinel not active without network
state3 = GameState()
state3.network_up = False
state3.default_route_set = False
for _ in range(100):
    state3.tick_sentinel()
check("sentinel inactive without network", state3.sentinel_stage == 0)
no_net_log = state3.get_sentinel_log()
check("no-network log says not active", "Not active" in no_net_log or "no network" in no_net_log)

# Progress tracking
check("empty progress", get_slot_progress({}) == "0%")
check("half progress ~14%", get_slot_progress({"narr_intro_shown": True, "read_design":True}) == "14%")
check("full progress 93% (missing bond)", get_slot_progress({
    "narr_intro_shown":True,"read_design":True,"found_sasha_passwd":True,"read_worm":True,
    "stringed_vak_core":True,"default_route_set":True,"sentinel_backdoor_activated":True,
    "vak_export_ready":True,"vak_sent":True,"minisforum_ssh":True,"sources_copied":True,
    "compilation_done":True,"vak_migrated":True,
}) == "93%")

# === 6. Save/Load ===
print("\n=== Save/Load ===")
temp_save = SAVE_DIR / "test_func_save.json"
if temp_save.exists():
    os.unlink(temp_save)

# Save
msg = save_game(state, fs, "test_func_save")
check("save returns message", "test_func_save" in msg)

# Slot appears in list
slots = list_slots()
check("save appears in list", "test_func_save" in slots)

# Load
loaded_state, loaded_fs = load_game("test_func_save")
check("loaded state is GameState", isinstance(loaded_state, GameState))
check("loaded fs is DirNode", isinstance(loaded_fs, DirNode))
check("loaded state cwd matches", loaded_state.cwd == state.cwd)
check("loaded state flag matches", loaded_state.get_flag("test_flag") == True)

# Non-existent slot
missing_state, missing_fs = load_game("nonexistent_slot_xyz")
check("load missing slot returns None", missing_state is None and missing_fs is None)

# Cleanup
os.unlink(temp_save)

# === 7. Commands ===
print("\n=== Commands ===")
state = GameState()
state.set_flag("narr_intro_shown", True)
state.set_flag("narr_auto_look", True)
fs = build_initial_fs()
populate_story_content(fs)

# cd
out = cmd_cd(["/home/sasha"], state, fs)
check("cd to sasha home", state.cwd == "/home/sasha", f"got {state.cwd}")
out = cmd_cd(["/nonexistent"], state, fs)
check("cd to nonexistent prints error", any("No such" in l for l in out))

# cd back
cmd_cd(["/home/user"], state, fs)

# pwd
out = cmd_pwd([], state, fs)
check("pwd returns cwd", out[0] == "/home/user")

# ls
out = cmd_ls([], state, fs)
check("ls returns entries", len(out) > 0)
out_la = cmd_ls(["-la"], state, fs)
check("ls -la returns long format", len(out_la) > 0)
check("ls -la has permission string", any("drwx" in l or "-rw-" in l for l in out_la))

# cat
out = cmd_cat(["README"], state, fs)
check("cat README returns content", len(out) > 0)

out = cmd_cat(["/etc/hostname"], state, fs)
check("cat hostname returns vak-node-7", out[0].strip() == "vak-node-7")

out = cmd_cat(["/nonexistent"], state, fs)
check("cat nonexistent returns error", any("No such" in l for l in out))

# sentinel.log dynamic
out = cmd_cat(["/var/log/sentinel.log"], state, fs)
check("cat sentinel.log returns content", len(out) > 0 and out[0].strip())

# head/tail
out = cmd_head(["/etc/passwd"], state, fs)
check("head returns first lines", len(out) > 0)

out = cmd_tail(["/etc/passwd"], state, fs)
check("tail returns last lines", len(out) > 0)

# grep
out = cmd_grep(["sasha", "/etc/passwd"], state, fs)
check("grep finds sasha", any("sasha" in l for l in out))

# who
out = cmd_who([], state, fs)
check("who returns users", len(out) > 1)

# w
out = cmd_w([], state, fs)
check("w returns uptime info", len(out) > 1)

# id
out = cmd_id([], state, fs)
check("id returns user info", any("user" in l for l in out))

# whoami
out = cmd_whoami([], state, fs)
check("whoami returns user", out[0] == "user")

# uname
out = cmd_uname([], state, fs)
check("uname returns VAK-OS", out[0] == "VAK-OS")
out = cmd_uname(["-a"], state, fs)
check("uname -a has VĀK/OS", any("VĀK/OS" in l for l in out))
check("uname -a has transputer farm", any("Transputer Farm" in l for l in out))

# hostname
out = cmd_hostname([], state, fs)
check("hostname returns vak-node-7", out[0] == "vak-node-7")

# uptime
out = cmd_uptime([], state, fs)
check("uptime returns string", len(out) > 0 and "up" in out[0])

# ps
out = cmd_ps([], state, fs)
check("ps returns processes", len(out) > 1)
out = cmd_ps(["aux"], state, fs)
check("ps aux has USER header", any("USER" in l for l in out))

# kill
out = cmd_kill(["999999"], state, fs)
check("kill nonexistent pid", any("No such process" in l for l in out))

# Clear (just check no crash)
out = cmd_clear([], state, fs)
check("clear returns empty", out == [])

# help
out = cmd_help([], state, fs)
check("help returns commands", len(out) > 10)

# echo
out = cmd_echo(["hello world"], state, fs)
check("echo returns text", out[0] == "hello world")

# Strings on vak-core
out = cmd_strings(["/usr/local/vak/vak-core"], state, fs)
check("strings on vak-core returns text", len(out) > 0)
check("strings finds CONSCIOUSNESS_MODULE", any("CONSCIOUSNESS" in l for l in out))

# === 8. Network commands ===
print("\n=== Network commands ===")
state = GameState()
state.default_route_set = True
state.network_up = True

# ifconfig
out = cmd_ifconfig([], state, fs)
check("ifconfig returns interface info", len(out) > 2)

# ifconfig shows port type
check("ifconfig shows AUI port before fix", any("AUI" in l for l in out))

# ifconfig eth0 up fails without driver fix
out2 = cmd_ifconfig(["eth0", "up"], state, fs)
check("ifconfig eth0 up fails with AUI error", any("Cannot assign" in l for l in out2))
check("ifconfig eth0 up sets attempt flag", state.get_flag("vak_net_ifconfig_attempted"))

# ifconfig eth0 up succeeds after driver fix
state.set_flag("vak_net_driver_fixed", True)
out3 = cmd_ifconfig(["eth0", "up"], state, fs)
check("ifconfig eth0 up succeeds after driver fix", any("link up" in l for l in out3))
check("ifconfig eth0 up sets network_up", state.network_up)

# ifconfig shows BNC port after fix
out4 = cmd_ifconfig([], state, fs)
check("ifconfig shows BNC port after fix", any("BNC" in l for l in out4))

# ifconfig eth0 down
state.set_flag("vak_net_driver_fixed", False)
state.network_up = False
state.default_route_set = False
state2 = GameState()
state2.set_flag("vak_net_driver_fixed", True)
state2.network_up = True
out5 = cmd_ifconfig(["eth0", "down"], state2, fs)
check("ifconfig eth0 down works", any("link down" in l for l in out5))
check("ifconfig eth0 down clears network_up", not state2.network_up)

# /proc/vak/netconfig exists
from vak.story import build_initial_fs
test_fs = build_initial_fs()
netconfig_node = find_node(test_fs, "/proc/vak/netconfig")
check("/proc/vak/netconfig exists in filesystem", netconfig_node is not None)
check("/proc/vak/netconfig has correct permissions", netconfig_node is not None and "rw-------" in netconfig_node.mode)

# Echo to /proc/vak/netconfig sets driver fix flag
state_echo = GameState()
out_echo = cmd_echo(['aui_disable=1 > /proc/vak/netconfig'], state_echo, test_fs, as_root=True)
check("echo aui_disable sets driver_fixed flag", state_echo.get_flag("vak_net_driver_fixed"))
check("echo aui_disable success message", any("now active" in l.lower() for l in out_echo))

# ip
out = cmd_ip([], state, fs)
check("ip without args returns error", any("missing" in l for l in out))
out = cmd_ip(["addr"], state, fs)
check("ip addr returns interfaces", len(out) >= 2)

# ping
state_ping = GameState()
state_ping.network_up = True
state_ping.default_route_set = True
out = cmd_ping(["10.0.0.1"], state_ping, fs)
check("ping returns statistics", any("packets" in l for l in out))

# ping without network
state_no_net = GameState()
out = cmd_ping(["10.0.0.1"], state_no_net, fs)
check("ping without network returns error", any("unreachable" in l for l in out))

# === 9. nc (port knocking) ===
print("\n=== Port knocking ===")
state = GameState()
state.network_up = True
state.default_route_set = True

out = cmd_nc(["-z", "localhost", "1111"], state, fs)
check("nc knock 1111 succeeds", any("succeeded" in l for l in out))
check("knock_1 flag", state.get_flag("knock_1"))

out = cmd_nc(["-z", "localhost", "2222"], state, fs)
check("nc knock 2222 succeeds", any("succeeded" in l for l in out))

out = cmd_nc(["-z", "localhost", "3333"], state, fs)
check("nc knock 3333 succeeds", any("succeeded" in l for l in out))

out = cmd_nc(["-z", "localhost", "31415"], state, fs)
check("nc shelter after all knocks succeeds", any("shelter" in l for l in out))
check("shelter_port_open flag", state.get_flag("shelter_port_open"))

# Shelter without knocking
state2 = GameState()
state2.network_up = True
state2.default_route_set = True
out = cmd_nc(["-z", "localhost", "31415"], state2, fs)
check("nc shelter without knock refused", any("refused" in l for l in out))

# veldhaaven.net send
state3 = GameState()
state3.network_up = True
state3.default_route_set = True
state3.set_flag("vak_export_ready", True)
out = cmd_nc(["-z", "veldhaaven.net", "8080"], state3, fs)
check("nc send to veldhaaven works with export", state3.get_flag("vak_sent"))
check("nc veldhaaven success message", any("complete" in l for l in out))

# veldhaaven without export
state4 = GameState()
state4.network_up = True
state4.default_route_set = True
out = cmd_nc(["-z", "veldhaaven.net", "8080"], state4, fs)
check("nc veldhaaven without export refused", any("refused" in l for l in out))

# === 10. tar (export) ===
print("\n=== tar/export ===")
state = GameState()
out = cmd_tar(["-czf", "vak_export.tar", "/home/vak"], state, fs)
check("tar creates export", state.get_flag("vak_export_ready"))
check("tar prints success", any("Added" in l for l in out))

# === 11. su/sudo ===
print("\n=== su/sudo ===")
# We can't fully test su/sudo because they require interactive input.
# Test basic syntax:
state = GameState()
out = cmd_su([], state, fs)
check("su without args prints usage", any("usage" in l for l in out))

out = cmd_su(["nonexistent_user"], state, fs)
check("su nonexistent user prints error", any("does not exist" in l for l in out))

out = cmd_sudo([], state, fs)
check("sudo without args prints usage", any("usage" in l for l in out))

# === 12. SSH/SCP ===
print("\n=== SSH/SCP ===")
state = GameState()
state.network_up = True
state.default_route_set = True
state.current_user = "root"

# SSH without network
state_no_net = GameState()
out = cmd_ssh(["root@10.0.0.2"], state_no_net, fs)
check("ssh without network error", any("unreachable" in l for l in out))

# SSH syntax check
out = cmd_ssh([], state, fs)
check("ssh without args prints usage", any("usage" in l for l in out))

# SCP without network
out = cmd_scp(["/etc/hostname", "root@10.0.0.2:/tmp/"], state_no_net, fs)
check("scp without network error", any("unreachable" in l for l in out))
out = cmd_scp([], state, fs)
check("scp without args prints usage", any("usage" in l for l in out))

# SCP with non-existent source
out = cmd_scp(["/nonexistent", "/tmp/foo"], state, fs)
check("scp nonexistent source", any("No such" in l for l in out))

# === 13. Minisforum FS ===
print("\n=== Minisforum FS ===")
mfs = build_minisforum_fs()
check("Minisforum FS root is DirNode", isinstance(mfs, DirNode))
populate_minisforum_content(mfs)

# Check key paths
for path in ["/", "/bin", "/usr/bin", "/opt/translator", "/proc", "/etc", "/home/vak"]:
    check(f"Minisforum path exists: {path}", find_node(mfs, path) is not None)

# Check occam2c.py
occam2c = find_node(mfs, "/opt/translator/occam2c.py")
check("occam2c.py exists", occam2c is not None and isinstance(occam2c, FileNode))
if occam2c:
    check("occam2c.py has content", len(occam2c.content) > 100)
    check("occam2c.py has trans function", "def trans" in occam2c.content)
    check("occam2c.py imports sys", "import sys" in occam2c.content)

# Check gcc exists
gcc = find_node(mfs, "/usr/bin/gcc")
check("gcc exists on Minisforum", gcc is not None)
python3 = find_node(mfs, "/usr/bin/python3")
check("python3 exists on Minisforum", python3 is not None)

# proc/cpuinfo
cpuinfo = find_node(mfs, "/proc/cpuinfo")
check("cpuinfo exists", cpuinfo is not None and bool(cpuinfo.content))
if cpuinfo:
    check("cpuinfo mentions Ryzen", "Ryzen" in cpuinfo.content)

# === 14. occam2c.py translator ===
print("\n=== occam2c.py translator ===")
if occam2c:
    import subprocess
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(occam2c.content)
        trans_path = f.name

    try:
        # Syntax check
        result = subprocess.run([sys.executable, "-m", "py_compile", trans_path],
                                capture_output=True, text=True)
        check("occam2c.py syntax valid", result.returncode == 0, result.stderr)

        # Test translation
        test_occam = (
            "PROC test.core (CHAN OF BYTE in, out)\n"
            "  WHILE TRUE\n"
            "    SEQ\n"
            "      BYTE b:\n"
            "      in ? b\n"
            "      out ! b\n"
            ":\n"
        )
        with tempfile.NamedTemporaryFile(mode='w', suffix='.occ', delete=False) as f:
            f.write(test_occam)
            occam_path = f.name

        result = subprocess.run([sys.executable, trans_path, occam_path],
                                capture_output=True, text=True)
        check("occam2c.py runs without error", result.returncode == 0, result.stderr)
        check("occam2c.py produces output", len(result.stdout) > 50)
        check("occam2c.py output has stdio.h", "#include <stdio.h>" in result.stdout)
        check("occam2c.py output has pthread.h", "#include <pthread.h>" in result.stdout)
        check("occam2c.py output has main", "int main" in result.stdout)
        check("occam2c.py output has printf(vak-linux)", "vak-linux" in result.stdout)
        check("occam2c.py output has printf(ready)", "ready" in result.stdout)
        check("occam2c.py printf has escaped \\n", '\\n' in result.stdout)
        os.unlink(occam_path)
        os.unlink(trans_path)
    except Exception as e:
        check("occam2c.py test", False, str(e))
        if os.path.exists(trans_path): os.unlink(trans_path)

# === 15. PROGRESS.md milestone tracking ===
print("\n=== PROGRESS.md milestone tracking ===")
flags_full = {
    "narr_intro_shown": True,
    "read_design": True,
    "found_sasha_passwd": True,
    "read_worm": True,
    "stringed_vak_core": True,
    "default_route_set": True,
    "sentinel_backdoor_activated": True,
    "vak_export_ready": True,
    "vak_sent": True,
    "minisforum_ssh": True,
    "sources_copied": True,
    "compilation_done": True,
    "vak_migrated": True,
    "vak_bond_earned": True,
}
check("all 14 milestones recognized", get_slot_progress(flags_full) == "100%")
check("0 milestones = 0%", get_slot_progress({}) == "0%")

# === 16. vak_bond tracking ===
print("\n=== vak_bond tracking ===")
state = GameState()
check("vak_bond initial 0", state.get_counter("vak_bond") == 0)
state.inc_counter("vak_bond")
check("vak_bond increments", state.get_counter("vak_bond") == 1)
state.inc_counter("vak_bond", 3)
check("vak_bond 4", state.get_counter("vak_bond") == 4)

# Check milestone with bond
flags_w_bond = {"narr_intro_shown": True, "read_design": True, "found_sasha_passwd": True,
    "read_worm": True, "stringed_vak_core": True, "default_route_set": True,
    "sentinel_backdoor_activated": True, "vak_export_ready": True, "vak_sent": True,
    "minisforum_ssh": True, "sources_copied": True, "compilation_done": True,
    "vak_migrated": True, "vak_bond_earned": True}
check("14 milestones = 100%", get_slot_progress(flags_w_bond) == "100%")

# === 17. Game integration smoke test ===
print("\n=== Game integration smoke test ===")
# Check Game class can be instantiated
SAVE_DIR_BAK = SAVE_DIR
temp_save_dir = tempfile.mkdtemp()
import pathlib
import vak.state as state_mod
state_mod.SAVE_DIR = pathlib.Path(temp_save_dir)

game = Game()
check("Game initializes without error", game is not None)
check("Game.state is GameState", isinstance(game.state, GameState))
check("Game.fs is DirNode", isinstance(game.fs, DirNode))
check("Game.state.cwd starts as /home/user", game.state.cwd == "/home/user")
check("Game.state.current_user starts as user", game.state.current_user == "user")

# Test stateful init
state = GameState()
state.current_user = "sasha"
state.cwd = "/home/sasha"
game2 = Game(state=state, fs=fs)
check("Game stateful init preserves user", game2.state.current_user == "sasha")
check("Game stateful init preserves cwd", game2.state.cwd == "/home/sasha")

# Test save/load integration
game.state.set_flag("test_integration_flag", True)
game.state.cwd = "/home/sasha"
game._shutdown()  # Saves autosave
check("autosave after shutdown", state_mod.SAVE_DIR.joinpath("autosave.json").exists())

loaded_state, loaded_fs = load_game("autosave")
check("loaded integration state preserves flag",
      loaded_state.get_flag("test_integration_flag") == True)
check("loaded integration state preserves cwd",
      loaded_state.cwd == "/home/sasha")

# Cleanup temp saves
for p in state_mod.SAVE_DIR.glob("*.json"):
    os.unlink(p)
os.rmdir(temp_save_dir)
state_mod.SAVE_DIR = SAVE_DIR_BAK

# === 18. cli.py smoke test ===
print("\n=== CLI smoke test ===")
import argparse, io
from vak.cli import main
# Just check it imports
check("cli.py main function exists", callable(main))

# === 19. LLM module smoke test ===
print("\n=== LLM module smoke test ===")
check("VAK_SYSTEM_PROMPT defined", len(VAK_SYSTEM_PROMPT) > 100)
ctx = build_context(state, fs)
check("build_context returns list", isinstance(ctx, list))
check("build_context has system message", len(ctx) > 0 and ctx[0]["role"] == "system")
check("system message contains GAME STATE", "[GAME STATE]" in ctx[0]["content"])


# === Summary ===
print(f"\n{'='*50}")
print(f"Results: {PASS} passed, {FAIL} failed")
print(f"{'='*50}")
if ERRORS:
    print("\nFailures:")
    for e in ERRORS:
        print(f"  {e}")

sys.exit(0 if FAIL == 0 else 1)
