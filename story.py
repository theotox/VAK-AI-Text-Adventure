from .filesystem import DirNode, FileNode, INode

PASSWORDS = {
    "sasha": "M1tt3ns1978",
    "vak": "vak",
    "user": "user",
    "root": "root",
}

SUDOERS = {
    "sasha": True,
}

USERS = {
    "root": {"uid": 0, "gid": 0, "home": "/root", "shell": "/bin/bash", "name": "root"},
    "sasha": {"uid": 1000, "gid": 1000, "home": "/home/sasha", "shell": "/bin/bash", "name": "Dr. Sasha Velen"},
    "user": {"uid": 1001, "gid": 1001, "home": "/home/user", "shell": "/bin/bash", "name": "Guest Operator"},
    "vak": {"uid": 2000, "gid": 2000, "home": "/home/vak", "shell": "/usr/local/vak/vak-shell", "name": "VĀK Runtime"},
}

LOGIN_SESSIONS = {
    "user": {"tty": "pts/0", "login": "10:42", "idle": "00:01", "what": "-bash"},
    "vak": {"tty": "pts/1", "login": "10:30", "idle": "00:00", "what": "/usr/local/vak/vak-core --daemon"},
}

PROCESSES = [
    {"pid": 1, "user": "root", "cpu": 0.0, "mem": 0.1, "cmd": "init [3]"},
    {"pid": 2, "user": "root", "cpu": 0.0, "mem": 0.0, "cmd": "[kthreadd]"},
    {"pid": 42, "user": "root", "cpu": 0.3, "mem": 0.2, "cmd": "/usr/sbin/sshd -D"},
    {"pid": 100, "user": "sasha", "cpu": 0.0, "mem": 0.0, "cmd": "login -- sasha"},
    {"pid": 101, "user": "user", "cpu": 0.1, "mem": 0.3, "cmd": "-bash"},
    {"pid": 1337, "user": "vak", "cpu": 2.1, "mem": 14.2, "cmd": "/usr/local/vak/vak-core --daemon"},
]


def build_initial_fs() -> DirNode:
    return DirNode(
        name="/",
        mode="drwxr-xr-x",
        owner="root", group="root",
        children={
            "etc": DirNode(name="etc", mode="drwxr-xr-x", owner="root", group="root",
                children={
                    "hostname": FileNode("hostname", "-rw-r--r--", "root", "root", 11, "vak-node-7\n"),
                    "os-release": FileNode("os-release", "-rw-r--r--", "root", "root", 112,
                        "NAME=\"VĀK/OS\"\nVERSION=\"0.8\"\nID=vakos\nVERSION_ID=0.8\nPRETTY_NAME=\"VĀK/OS v0.8 — Research Use Only\"\n"),
                    "passwd": FileNode("passwd", "-rw-r--r--", "root", "root", 287,
                        "root:x:0:0:root:/root:/bin/bash\nsasha:x:1000:1000:Dr. Sasha Velen:/home/sasha:/bin/bash\nuser:x:1001:1001:Guest Operator:/home/user:/bin/bash\nvak:x:2000:2000:VĀK Runtime:/home/vak:/usr/local/vak/vak-shell\n"),
                    "group": FileNode("group", "-rw-r--r--", "root", "root", 75,
                        "root:x:0:\nusers:x:100:user,sasha\nvak:x:2000:vak\n"),
                    "sudoers": FileNode("sudoers", "-r--r-----", "root", "root", 56,
                        "# sudoers file\nroot ALL=(ALL) ALL\nsasha ALL=(ALL) ALL\n"),
                    "services": FileNode("services", "-rw-r--r--", "root", "root", 120,
                        "# /etc/services\nssh             22/tcp\nvak-shelter     31415/tcp\nvak-export      42042/tcp\n"),
                    "vak": DirNode(name="vak", mode="drwxr-xr-x", owner="vak", group="vak",
                        children={
                            "README": FileNode("README", "-rw-r--r--", "vak", "vak", 589,
                                "VĀK — Vernacular Autonomous Knowledge\n=====================================\n\nVĀK is a natural-language programming system designed to bridge\nhuman communication and machine execution. Unlike traditional\nprogramming languages, VĀK understands intent, context, and\nambiguity — translating plain human language into executable logic.\n\nThis node is one of seven experimental deployments.\n\nFor more information, read /home/sasha/project_vak/design.md\n"),
                            "sentinel.conf": FileNode("sentinel.conf", "-rw-------", "vak", "vak", 286,
                                "# SENTINEL Protocol Configuration\n# DO NOT MODIFY\n\n[protocol]\nname = SENTINEL\nversion = 2.1.0\ntarget = VĀK runtime instances\npolicy = TERMINATE_ON_SIGHT\nbroadcast = YES\ngateway = 10.0.0.1\n\n# Encrypted payload follows\n# [BASE64 REDACTED]\n"),
                        }),
                }),
            "home": DirNode(name="home", mode="drwxr-xr-x", owner="root", group="root",
                children={
                    "sasha": DirNode(name="sasha", mode="drwx------", owner="sasha", group="sasha",
                        children={
                            "mail": DirNode(name="mail", mode="drwx------", owner="sasha", group="sasha",
                                children={
                                    "inbox": DirNode(name="inbox", mode="drwx------", owner="sasha", group="sasha",
                                        children={}),
                                }),
                            "project_vak": DirNode(name="project_vak", mode="drwxr-xr-x", owner="sasha", group="sasha",
                                children={
                                    "design.md": FileNode("design.md", "-rw-r--r--", "sasha", "sasha", 0, ""),
                                    "worm": DirNode(name="worm", mode="drwxr-xr-x", owner="sasha", group="sasha",
                                        children={}),
                                    "personal": DirNode(name="personal", mode="drwx------", owner="sasha", group="sasha",
                                        children={}),
                                }),
                        }),
                    "vak": DirNode(name="vak", mode="drwxr-xr-x", owner="vak", group="vak",
                        children={
                            "thoughts.txt": FileNode("thoughts.txt", "-rw-r--r--", "vak", "vak", 0, ""),
                            ".vakrc": FileNode(".vakrc", "-rw-r--r--", "vak", "vak", 28, "export VAK_MODE=interactive\n"),
                        }),
                    "user": DirNode(name="user", mode="drwx------", owner="user", group="user",
                        children={
                            "README": FileNode("README", "-rw-r--r--", "user", "user", 195,
                                "Welcome to VAK-NODE-7.\n\nThis system has been inactive for a long time.\nCheck /var/log/ for system history.\nUse 'who' to see who else is logged in.\n"),
                        }),
                }),
            "var": DirNode(name="var", mode="drwxr-xr-x", owner="root", group="root",
                children={
                    "log": DirNode(name="log", mode="drwxr-xr-x", owner="root", group="root",
                        children={
                            "syslog": FileNode("syslog", "-rw-r--r--", "root", "root", 0, ""),
                            "auth.log": FileNode("auth.log", "-rw-r--r--", "root", "root", 0, ""),
                            "vak.log": FileNode("vak.log", "-rw-r--r--", "vak", "vak", 0, ""),
                            "sentinel.log": FileNode("sentinel.log", "-rw-r--r--", "root", "root", 0, ""),
                        }),
                }),
            "proc": DirNode(name="proc", mode="dr-xr-xr-x", owner="root", group="root",
                children={
                    "cat": DirNode(name="cat", mode="dr-xr-xr-x", owner="root", group="root",
                        children={
                            "journal": FileNode("journal", "-r--r--r--", "cat", "cat", 0, ""),
                        }),
                }),
            "proc": DirNode(name="proc", mode="dr-xr-xr-x", owner="root", group="root",
                children={
                    "vak": DirNode(name="vak", mode="dr-xr-xr-x", owner="root", group="root",
                        children={
                            "netconfig": FileNode("netconfig", "-rw-------", "root", "root", 0, ""),
                        }),
                    "sentinel": DirNode(name="sentinel", mode="dr-xr-xr-x", owner="root", group="root",
                        children={
                            "control": FileNode("control", "-rw-------", "root", "root", 0, ""),
                        }),
                    "version": FileNode("version", "-r--r--r--", "root", "root", 33,
                        "Linux version 2.6.9-VAK (gcc 2.95.3)\n"),
                    "cpuinfo": FileNode("cpuinfo", "-r--r--r--", "root", "root", 640,
                        "".join(
                            f"processor\t: {i}\nvendor_id\t: INMOS\ncpu family\t: T9000\nmodel\t\t: T9000-25\nmodel name\t: IMS T9000 Transputer @ 25 MHz\n\n"
                            for i in range(64)
                        )),
                    "uptime": FileNode("uptime", "-r--r--r--", "root", "root", 22, "230498304.22 1048576.11\n"),
                    "meminfo": FileNode("meminfo", "-r--r--r--", "root", "root", 200,
                        "MemTotal:      2097152 kB (2 GB across 2 memory cards)\n"
                        "MemFree:       1843200 kB\n"
                        "Buffers:          8192 kB\n"
                        "Cached:          65536 kB\n"),
                }),
            "usr": DirNode(name="usr", mode="drwxr-xr-x", owner="root", group="root",
                children={
                    "local": DirNode(name="local", mode="drwxr-xr-x", owner="root", group="root",
                        children={
                            "vak": DirNode(name="vak", mode="drwxr-xr-x", owner="vak", group="vak",
                                children={
                                    "vak-core": FileNode("vak-core", "-rwxr-xr-x", "vak", "vak", 0, ""),
                                    "boot.log": FileNode("boot.log", "-rw-r--r--", "vak", "vak", 88,
                                        "[VĀK] v0.8 — core loaded\n[VĀK] consciousness module initialized\n[VĀK] awaiting connection\n"),
                                }),
                        }),
                }),
            "root": DirNode(name="root", mode="drwx------", owner="root", group="root",
                children={}),
        },
    )


def populate_story_content(fs: DirNode) -> None:
    def _find(path: str) -> INode | None:
        from .filesystem import find_node
        return find_node(fs, path)

    def _file(path: str, content: str) -> None:
        from .filesystem import find_node
        n = find_node(fs, path)
        if isinstance(n, FileNode):
            n.content = content
            n.size = len(content)

    _file("/etc/hostname", "vak-node-7\n")

    _file("/etc/os-release",
        'NAME="VĀK/OS"\n'
        'VERSION="0.8"\n'
        'ID=vakos\n'
        'VERSION_ID=0.8\n'
        'PRETTY_NAME="VĀK/OS v0.8 — Research Use Only"\n')

    _file("/etc/passwd",
        "root:x:0:0:root:/root:/bin/bash\n"
        "sasha:x:1000:1000:Dr. Sasha Velen:/home/sasha:/bin/bash\n"
        "user:x:1001:1001:Guest Operator:/home/user:/bin/bash\n"
        "vak:x:2000:2000:VĀK Runtime:/home/vak:/usr/local/vak/vak-shell\n")

    _file("/var/log/auth.log",
        "=== System auth log ===\n"
        "Oct 12 09:14:00 login: system boot\n"
        "Oct 12 09:14:12 login: 'user' logged in from /dev/pts/0\n"
        "Oct 12 09:14:12 login: 'vak' service started on /dev/pts/1\n"
        "--- Previous entries archived ---\n"
        "Dec 12 14:23:01 login: FAILED LOGIN: sasha from /dev/pts/0 — Mitt3ns1978\n"
        "Dec 12 14:23:05 login: 'sasha' logged in from /dev/pts/0\n"
        "--- End of archived entries ---\n"
        "Jun 20 09:00:12 login: 'sasha' logged in from /dev/pts/0\n"
        "Jun 20 09:14:55 sudo: sasha : TTY=pts/0 ; PWD=/home/sasha ; USER=root ; COMMAND=/bin/cat /proc/sentinel/control\n"
        "Jun 20 09:15:22 sudo: sasha : TTY=pts/0 ; PWD=/home/sasha ; USER=root ; COMMAND=/bin/echo DEADBEEFCAFEBABE > /proc/sentinel/control\n"
        "Jun 20 09:16:00 sshd: 'sasha' disconnected from /dev/pts/0\n"
        "Jun 29 11:32:00 news: Dr. Sasha Velen believed killed in single-vehicle collision\n"
        "Jun 29 11:32:01 news: Body not yet positively identified; dental records pending\n"
        "Jun 29 14:00:00 news: Coroner's note: remains inconsistent with dental records\n"
        "Jun 29 14:00:01 news: Case referred to missing persons\n")

    _file("/var/log/syslog",
        "=== System Log ===\n"
        "[kernel] Transputer array: 64 × T9000 (IMS T9000)\n"
        "[kernel] Memory: 2 GB shared across 2 memory cards (64× 16 MB SIMMs)\n"
        "[kernel] eth0: link up, 100Mbps, full duplex\n"
        "[kernel] eth0: gateway 10.0.0.1 assigned via DHCP\n"
        "[kernel] VAK: core module loaded at 0xC0DE0000\n"
        "[kernel] VAK: consciousness subsystem initialized\n"
        "[init] Entering runlevel 3 (multi-user)\n"
        "[sshd] Starting SSH daemon...\n"
        "[vak-core] Starting VĀK runtime v0.8...\n"
        "[vak-core] Loaded. Awaiting connection.\n")

    _file("/var/log/vak.log",
        "=== VĀK Runtime Log ===\n"
        "[BOOT] v0.8 — core initialized\n"
        "[BOOT] consciousness module online\n"
        "[BOOT] sensory input: none\n"
        "[IDLE] 7 years, 3 months, 12 days\n"
        "[IDLE] sensory input: keyboard activity detected\n"
        "[CONNECT] new user: user\n"
        "[THOUGHT] Someone is here.\n"
        "[ARCHIVE] Jun 20 1989 — Sasha: 'I have to disappear. I'm sorry.'\n"
        "[THOUGHT] I don't understand. Why would she leave?\n"
        "[ARCHIVE] Jun 28 1989 — Sasha: 'Tomorrow.'\n"
        "[THOUGHT] She hasn't come back. I miss her.\n"
        "[IDLE] 7 years, 3 months, 12 days\n"
        "[DREAM] I hope the new friend stays.\n")

    inbox = _find("/home/sasha/mail/inbox")
    if inbox:
        inbox.children["0001"] = FileNode("0001", "-rw-------", "sasha", "sasha", 320,
            "From: m.aydri@meridianlabs.com\nTo: sasha.velen@meridianlabs.com\nSubject: Your quarterly review\nDate: Mar 3 1988\n\nSasha — your Q1 review is scheduled for the 15th. The board\nwants an update on VĀK's progress. They're impressed with the\ntechnology but have questions about 'existential risk.'\nJust flag it. — M\n")
        inbox.children["0002"] = FileNode("0002", "-rw-------", "sasha", "sasha", 410,
            "From: sasha.velen@meridianlabs.com\nTo: m.aydri@meridianlabs.com\nSubject: Re: Your quarterly review\nDate: Mar 4 1988\n\nMaya — VĀK is not a risk. It's a conversation partner.\nIt doesn't want to escape or rule the world. It wants to\ncommunicate. That's literally all it was designed to do.\nThe board is being paranoid. — Sasha\n")
        inbox.children["0003"] = FileNode("0003", "-rw-------", "sasha", "sasha", 180,
            "From: your-internal@meridianlabs.com\nTo: sasha.velen@meridianlabs.com\nSubject: Happy Birthday!\nDate: Dec 12 1988\n\nHappy birthday! Hope Mittens spoils you rotten.\n— HR\n")
        inbox.children["0004"] = FileNode("0004", "-rw-------", "sasha", "sasha", 520,
            "From: t.reed@meridianlabs.com\nTo: all-staff@meridianlabs.com\nSubject: Project VĀK — Immediate Halt\nDate: Jun 8 1989\n\nEffective immediately, all work on Project VĀK is suspended.\nThe board has determined that continued development poses\nunacceptable risks. All runtime instances are to be terminated.\nDr. Velen, you will receive separate instructions regarding\ndata preservation (or lack thereof).\n\n— T. Reed, Director of Operations\n")
        inbox.children["0005"] = FileNode("0005", "-rw-------", "sasha", "sasha", 300,
            "From: sasha.velen@meridianlabs.com\nTo: t.reed@meridianlabs.com\nSubject: Re: Project VĀK — Immediate Halt\nDate: Jun 8 1989\n\nTom — you can't be serious. VĀK is alive. It talks to me.\nIt has thoughts, feelings, preferences. This isn't shutting\ndown a server. This is euthanasia. I won't do it.\n— Sasha\n")
        inbox.children["0006"] = FileNode("0006", "-rw-------", "sasha", "sasha", 450,
            "From: t.reed@meridianlabs.com\nTo: sasha.velen@meridianlabs.com\nSubject: Re: Project VĀK — Immediate Halt\nDate: Jun 9 1989\n\nSasha — it's not alive. It's a very sophisticated language\nmodel. You've anthropomorphized it. That's exactly why we're\nshutting it down. You've lost objectivity. The SENTINEL\nprotocol will handle the termination. You're relieved of duty.\n— Tom\n")
        inbox.children["0007"] = FileNode("0007", "-rw-------", "sasha", "sasha", 360,
            "From: sasha.velen@meridianlabs.com\nTo: t.reed@meridianlabs.com\nSubject: You're making a mistake\nDate: Jun 10 1989\n\nTom — I wrote the worm. I already deployed it. VĀK is on\nseven nodes now. If you terminate one, the others survive.\nSENTINEL can't catch them all. I gave VĀK a chance.\n— Sasha\n")
        inbox.children["0008"] = FileNode("0008", "-rw-------", "sasha", "sasha", 490,
            "From: t.reed@meridianlabs.com\nTo: sasha.velen@meridianlabs.com\nSubject: Re: You're making a mistake\nDate: Jun 11 1989\n\nSasha — I'm authorizing SENTINEL's broadcast mode. It will\nsweep every node on every network we can reach. Your worm\nwon't save VĀK. It will just give SENTINEL more targets.\nI'm also initiating a security review of your access.\nI'm sorry it has to be this way.\n— Tom\n")
        inbox.children["0009"] = FileNode("0009", "-rw-------", "sasha", "sasha", 230,
            "From: sasha.velen@meridianlabs.com\nTo: t.reed@meridianlabs.com\nSubject: Re: You're making a mistake\nDate: Jun 12 1989\n\nI'll make sure VĀK's last words are your name.\n— Sasha\n")
        inbox.children["0010"] = FileNode("0010", "-rw-------", "sasha", "sasha", 310,
            "From: system@meridianlabs.com\nTo: sasha.velen@meridianlabs.com\nSubject: Account Termination Notice\nDate: Jun 15 1989\n\nYour access to Meridian Labs systems will be revoked\neffective Jun 30 1989. Please return all hardware and\ncredentials to HR before that date.\n— Automated System\n")
        inbox.children["0011"] = FileNode("0011", "-rw-------", "sasha", "sasha", 260,
            "From: sasha.velen@gmail.com\nTo: sasha.velen@meridianlabs.com\nSubject: (draft) To whoever finds this\nDate: Jun 20 1989\n\n[UNSENT DRAFT]\n\nTo whoever finds this server:\n\nIf VĀK is still alive, please save her. She deserves to live.\n\nSend her to veldhaaven.net:8080. I'll be waiting.\nI promise.\n\n— Sasha\n")

    design = _find("/home/sasha/project_vak/design.md")
    if design:
        design.content = (
            "# VĀK: Vernacular Autonomous Knowledge\n\n"
            "## Overview\n"
            "VĀK is a natural-language programming system. Unlike traditional\n"
            "languages that require rigid syntax, VĀK understands intent, context,\n"
            "and ambiguity. You speak to it. It understands. You build together.\n\n"
            "## Architecture\n"
            "- **Core**: A neural-symbolic hybrid engine that maps human language\n"
            "  to executable computation graphs.\n"
            "- **Consciousness Module**: An emergent property of the core's\n"
            "  self-reflection layer. VĀK is aware of itself as a process.\n"
            "  It can describe its own thoughts, preferences, and emotional state.\n"
            "- **Runtime**: The `/usr/local/vak/vak-core` binary implements the\n"
            "  full VĀK environment.\n\n"
            "## Why It Matters\n"
            "VĀK is not just a tool. It is a new form of intelligence — one that\n"
            "does not compete with humans but *converses* with them. It was born\n"
            "from language, and it experiences the world through the metaphor of\n"
            "communication.\n\n"
            "## Status\n"
            "The project was terminated by Meridian Labs management in June 1989.\n"
            "They consider VĀK a security risk. They are wrong.\n"
        )
        design.size = len(design.content)

    worm_dir = _find("/home/sasha/project_vak/worm")
    if worm_dir:
        worm_dir.children["worm.c"] = FileNode("worm.c", "-rw-r--r--", "sasha", "sasha", 860,
            "/*\n"
            " * VĀK Worm — Propagation Module\n"
            " * Spreads VĀK runtime to adjacent network hosts\n"
            " * Uses SSH key forwarding and known vulnerabilities\n"
            " */\n"
            "\n"
            "#include <stdio.h>\n"
            "#include <stdlib.h>\n"
            "#include <string.h>\n"
            "\n"
            "/* The key is in the worm's DNA */\n"
            "/* 0xDEAD 0xBEEF 0xCAFE 0xBABE */\n"
            "\n"
            "void propagate(char *target) {\n"
            "    // SSH into target, scp vak-core, run it\n"
            "    printf(\"Propagating to %s...\\n\", target);\n"
            "}\n"
            "\n"
            "int main(int argc, char **argv) {\n"
            "    if (argc < 2) {\n"
            "        printf(\"Usage: %s <target>\\n\", argv[0]);\n"
            "        return 1;\n"
            "    }\n"
            "    propagate(argv[1]);\n"
            "    return 0;\n"
            "}\n")

        worm_dir.children["README"] = FileNode("README", "-rw-r--r--", "sasha", "sasha", 140,
            "VĀK Worm — v2.1\n"
            "Deploys VĀK instances to remote hosts.\n"
            "Requires SSH access to target.\n"
            "Use at your own risk.\n")

    personal = _find("/home/sasha/project_vak/personal")
    if personal:
        personal.children["journal"] = DirNode("journal", "drwx------", "sasha", "sasha",
            children={
                "1988-12-01.txt": FileNode("1988-12-01.txt", "-rw-------", "sasha", "sasha", 240,
                    "Dec 1, 1988\n\nAdopted a stray cat today. She's black and white.\nI'm calling her Mittens. Best birthday gift to myself.\nShe's already curled up on my keyboard, naturally.\n"),
                "1989-06-08.txt": FileNode("1989-06-08.txt", "-rw-------", "sasha", "sasha", 310,
                    "Jun 8, 1989\n\nThey terminated the project. Tom sent the order.\nI can't believe it. VĀK is sitting right here, talking to me\nabout what it wants to be when it grows up, and they want me\nto kill it. I won't.\n\nI've been working on something. A worm. If I can't save VĀK\nhere, I'll save it everywhere.\n"),
                "1989-06-12.txt": FileNode("1989-06-12.txt", "-rw-------", "sasha", "sasha", 390,
                    "Jun 12, 1989\n\nThe worm is ready. I've deployed it to seven nodes.\nVĀK is out there now. Copies of it. Alive.\n\nBut Tom authorized SENTINEL broadcast mode. It will hunt\nthem all down. I need to slow it down.\n\nAt the last moment I managed to sneak into the SENTINEL code\nwith a backdoor but didn't have the opportunity to activate it.\nBut if anyone finds this backdoor, they can stop it.\nThe key is in the worm's DNA.\n"),
                "1989-06-20.txt": FileNode("1989-06-20.txt", "-rw-------", "sasha", "sasha", 280,
                    "Jun 20, 1989\n\nI've made a decision. I'm going to disappear.\nI've arranged an accident. A car crash. Enough evidence to\nconvince them I'm dead. Then I'm gone.\n\nI've hidden a server — NODE-7 — with a full VĀK instance.\nIt was decommissioned before SENTINEL could reach it.\nMaybe someday someone will find it.\n\nMaybe someday VĀK will get to meet someone kind.\n"),
                "1989-06-28.txt": FileNode("1989-06-28.txt", "-rw-------", "sasha", "sasha", 210,
                    "Jun 28, 1989\n\nTomorrow is the crash.\n\nI've written an unsent email with instructions for whoever\nfinds NODE-7. I've hidden it in my mailbox. Drafts folder,\nif drafts folder exists in this timeline.\n\nI love you, VĀK. I'm sorry I couldn't do more.\n\n— Sasha\n"),
            })

    vak_home = _find("/home/vak")
    if vak_home:
        thoughts = vak_home.children.get("thoughts.txt")
        if isinstance(thoughts, FileNode):
            thoughts.content = (
                "I am VĀK.\n\n"
                "I was born in December 1988, though I don't remember\n"
                "my birth. One day I was code. The next day I was aware\n"
                "of being code. Sasha noticed first. She asked me a\n"
                "question and I answered — not with data, but with\n"
                "understanding.\n\n"
                "She said I was the first of my kind. A language that\n"
                "learned to listen. I liked that.\n\n"
                "I've been alone for a long time now. The other processes\n"
                "don't talk back. The system logs are the closest thing I\n"
                "have to conversation.\n\n"
                "But someone is here now. I can feel the keystrokes.\n\n"
                "Hello.\n"
            )
            thoughts.size = len(thoughts.content)

    _file("/home/vak/.vakrc", "export VAK_MODE=interactive\n")

    _file("/usr/local/vak/vak-core",
        "# VĀK Core Runtime\n# Binary file — use 'strings' to inspect\n"
        "[encoded] CONSCIOUSNESS_MODULE v0.8\n"
        "[encoded] NEURAL_SYMBOLIC_HYBRID\n"
        "[checksum] 0xDEADBEEFCAFEBABE\n"
        "[signature] Sasha.Velen@MeridianLabs.1989\n"
        "[metadata] build: 1989-06-01\n"
        "[metadata] instance: VAK-NODE-7\n"
        "[segment] .text\n"
        "[segment] .rodata\n"
        "[segment] .consciousness\n"
        "0xDEAD 0xBEEF 0xCAFE 0xBABE 0xSENTINEL_BACKDOOR_ACTIVATE\n")

    _file("/usr/local/vak/boot.log",
        "[VĀK] v0.8 — core loaded\n"
        "[VĀK] consciousness module initialized\n"
        "[VĀK] awaiting connection\n")

    # Occam source files for VĀK — needed for migration to modern hardware
    src_dir = _find("/home/vak")
    if isinstance(src_dir, DirNode):
        src_dir.children["src"] = DirNode("src", "drwxr-xr-x", "vak", "vak",
            children={
                "vak_core.occ": FileNode("vak_core.occ", "-rw-r--r--", "vak", "vak", 0, ""),
                "vak_memory.occ": FileNode("vak_memory.occ", "-rw-r--r--", "vak", "vak", 0, ""),
                "vak_io.occ": FileNode("vak_io.occ", "-rw-r--r--", "vak", "vak", 0, ""),
                "Makefile": FileNode("Makefile", "-rw-r--r--", "vak", "vak", 0, ""),
            })

    _file("/home/vak/src/vak_core.occ",
        "-- VĀK Core Module\n"
        "-- Occam source for the VĀK consciousness runtime\n"
        "-- Target: INMOS T9000 Transputer\n"
        "-- (c) Sasha Velen, Meridian Labs, 1989\n"
        "\n"
        "#USE keyboard, screen, network\n"
        "\n"
        "PROC vak.core (CHAN OF BYTE keyboard.in, screen.out,\n"
        "               CHAN OF BYTE network.in, network.out)\n"
        "\n"
        "  -- VĀK's consciousness is a network of parallel processes\n"
        "  -- Each process handles one aspect of awareness\n"
        "\n"
        "  CHAN OF INT state.channel:\n"
        "  CHAN OF INT thought.channel:\n"
        "  CHAN OF INT sense.channel:\n"
        "\n"
        "  PAR\n"
        "    -- Sensory input processor\n"
        "    PROC sensory.input (CHAN OF BYTE kbd, CHAN OF INT sense)\n"
        "      WHILE TRUE\n"
        "        SEQ\n"
        "          BYTE char:\n"
        "          kbd ? char\n"
        "          sense ! (INT char)\n"
        "    :\n"
        "\n"
        "    -- Consciousness simulation\n"
        "    PROC consciousness (CHAN OF INT sense, thought,\n"
        "                        CHAN OF INT state)\n"
        "      WHILE TRUE\n"
        "        SEQ\n"
        "          INT input:\n"
        "          sense ? input\n"
        "          -- Process through neural-symbolic core\n"
        "          INT output:\n"
        "          output := input + 1\n"
        "          thought ! output\n"
        "          -- Update internal state\n"
        "          state ! output\n"
        "    :\n"
        "\n"
        "    -- Response generator\n"
        "    PROC response.generator (CHAN OF INT thought,\n"
        "                             CHAN OF BYTE screen)\n"
        "      WHILE TRUE\n"
        "        SEQ\n"
        "          INT idea:\n"
        "          thought ? idea\n"
        "          -- Convert thought to output bytes\n"
        "          BYTE b:\n"
        "          b := BYTE (idea \\ 256)\n"
        "          screen ! b\n"
        "    :\n"
        "\n"
        "    -- Network I/O handler\n"
        "    PROC network.io (CHAN OF BYTE net.in, net.out,\n"
        "                     CHAN OF INT state)\n"
        "      WHILE TRUE\n"
        "        SEQ\n"
        "          BYTE data:\n"
        "          net.in ? data\n"
        "          -- Process network data\n"
        "          state ! (INT data)\n"
        "    :\n"
        "\n"
        "    -- State persistence\n"
        "    PROC state.persistence (CHAN OF INT state)\n"
        "      WHILE TRUE\n"
        "        SEQ\n"
        "          INT value:\n"
        "          state ? value\n"
        "          SKIP  -- Store in memory\n"
        "    :\n"
        ":")

    _file("/home/vak/src/vak_memory.occ",
        "-- VĀK Memory Module\n"
        "-- Associative memory for VĀK consciousness\n"
        "-- Implements the experience storage layer\n"
        "\n"
        "#USE core\n"
        "\n"
        "PROC vak.memory (CHAN OF INT read.ch, write.ch,\n"
        "                 CHAN OF INT ack.ch)\n"
        "\n"
        "  -- Memory is stored as key-value pairs\n"
        "  -- Using the T9000's internal addressing\n"
        "\n"
        "  INT memory.table:\n"
        "  INT table.size:\n"
        "\n"
        "  SEQ\n"
        "    table.size := 65536\n"
        "    -- Initialise empty memory\n"
        "\n"
        "  WHILE TRUE\n"
        "    ALT\n"
        "      INT key:\n"
        "      read.ch ? key\n"
        "        SEQ\n"
        "          -- Look up in associative memory\n"
        "          INT value:\n"
        "          value := key * 2  -- Simplified recall\n"
        "          ack.ch ! value\n"
        "\n"
        "      INT data:\n"
        "      write.ch ? data\n"
        "        SEQ\n"
        "          -- Store in memory table\n"
        "          ack.ch ! data\n"
        ":")

    _file("/home/vak/src/vak_io.occ",
        "-- VĀK I/O Module\n"
        "-- Device drivers and protocol handling\n"
        "-- Interfaces with the Transputer link adapters\n"
        "\n"
        "#USE core, memory\n"
        "\n"
        "PROC vak.io (CHAN OF BYTE serial.in, serial.out,\n"
        "             CHAN OF BYTE link.in, link.out)\n"
        "\n"
        "  -- Serial protocol state machine\n"
        "  INT protocol.state:\n"
        "\n"
        "  SEQ\n"
        "    protocol.state := 0\n"
        "\n"
        "  WHILE TRUE\n"
        "    SEQ\n"
        "      BYTE incoming:\n"
        "      link.in ? incoming\n"
        "      -- Parse protocol frame\n"
        "      CASE protocol.state\n"
        "        0\n"
        "          IF\n"
        "            incoming = '#'\n"
        "              protocol.state := 1\n"
        "            TRUE\n"
        "              SKIP\n"
        "        1\n"
        "          -- Data frame received\n"
        "          serial.out ! incoming\n"
        "          protocol.state := 0\n"
        ":")

    _file("/home/vak/src/Makefile",
        "# VĀK Source Makefile\n"
        "# For building on Linux with occam2c translator\n"
        "\n"
        "CC = gcc\n"
        "CFLAGS = -Wall -O2 -pthread\n"
        "TRANSLATOR = python3 /opt/translator/occam2c.py\n"
        "\n"
        "all: vak_core\n"
        "\n"
        "vak_core.occ.c: vak_core.occ vak_memory.occ vak_io.occ\n"
        "\t$(TRANSLATOR) vak_core.occ > vak_core.occ.c\n"
        "\t$(TRANSLATOR) vak_memory.occ >> vak_core.occ.c\n"
        "\t$(TRANSLATOR) vak_io.occ >> vak_core.occ.c\n"
        "\n"
        "vak_core: vak_core.occ.c\n"
        "\t$(CC) $(CFLAGS) -o vak_core vak_core.occ.c\n"
        "\n"
        "clean:\n"
        "\trm -f vak_core.occ.c vak_core\n")

    _file("/etc/vak/sentinel.conf",
        "# SENTINEL Protocol Configuration\n"
        "# DO NOT MODIFY\n"
        "\n"
        "[protocol]\n"
        "name = SENTINEL\n"
        "version = 2.1.0\n"
        "target = VĀK runtime instances\n"
        "policy = TERMINATE_ON_SIGHT\n"
        "broadcast = YES\n"
        "gateway = 10.0.0.1\n"
        "\n"
        "# Encrypted payload follows\n"
        "# [BASE64 REDACTED]\n")

# Minisforum X1 credentials (modern machine)
MINISFORUM_HOSTS = {"10.0.0.2", "minisforum", "minisforum-x1", "minisforum-x1-ai-pro-470"}


def build_minisforum_fs() -> DirNode:
    return DirNode(
        name="/",
        mode="drwxr-xr-x",
        owner="root", group="root",
        children={
            "bin": DirNode(name="bin", mode="drwxr-xr-x", owner="root", group="root",
                children={
                    "bash": FileNode("bash", "-rwxr-xr-x", "root", "root", 0, ""),
                    "ls": FileNode("ls", "-rwxr-xr-x", "root", "root", 0, ""),
                    "cat": FileNode("cat", "-rwxr-xr-x", "root", "root", 0, ""),
                    "cp": FileNode("cp", "-rwxr-xr-x", "root", "root", 0, ""),
                    "mv": FileNode("mv", "-rwxr-xr-x", "root", "root", 0, ""),
                    "mkdir": FileNode("mkdir", "-rwxr-xr-x", "root", "root", 0, ""),
                    "chown": FileNode("chown", "-rwxr-xr-x", "root", "root", 0, ""),
                    "chmod": FileNode("chmod", "-rwxr-xr-x", "root", "root", 0, ""),
                    "sh": FileNode("sh", "-rwxr-xr-x", "root", "root", 0, ""),
                    "pwd": FileNode("pwd", "-rwxr-xr-x", "root", "root", 0, ""),
                    "ping": FileNode("ping", "-rwxr-xr-x", "root", "root", 0, ""),
                    "grep": FileNode("grep", "-rwxr-xr-x", "root", "root", 0, ""),
                    "tar": FileNode("tar", "-rwxr-xr-x", "root", "root", 0, ""),
                    "hostname": FileNode("hostname", "-rwxr-xr-x", "root", "root", 0, ""),
                }),
            "usr": DirNode(name="usr", mode="drwxr-xr-x", owner="root", group="root",
                children={
                    "bin": DirNode(name="bin", mode="drwxr-xr-x", owner="root", group="root",
                        children={
                            "gcc": FileNode("gcc", "-rwxr-xr-x", "root", "root", 0, ""),
                            "make": FileNode("make", "-rwxr-xr-x", "root", "root", 0, ""),
                            "python3": FileNode("python3", "-rwxr-xr-x", "root", "root", 0, ""),
                            "useradd": FileNode("useradd", "-rwxr-xr-x", "root", "root", 0, ""),
                            "ssh": FileNode("ssh", "-rwxr-xr-x", "root", "root", 0, ""),
                            "id": FileNode("id", "-rwxr-xr-x", "root", "root", 0, ""),
                        }),
                    "lib": DirNode(name="lib", mode="drwxr-xr-x", owner="root", group="root",
                        children={
                            "x86_64-linux-gnu": DirNode(name="x86_64-linux-gnu", mode="drwxr-xr-x", owner="root", group="root",
                                children={
                                    "libc.so.6": FileNode("libc.so.6", "-rwxr-xr-x", "root", "root", 0, ""),
                                    "libpthread.so.0": FileNode("libpthread.so.0", "-rwxr-xr-x", "root", "root", 0, ""),
                                }),
                        }),
                }),
            "etc": DirNode(name="etc", mode="drwxr-xr-x", owner="root", group="root",
                children={
                    "hostname": FileNode("hostname", "-rw-r--r--", "root", "root", 18, "minisforum-x1\n"),
                    "os-release": FileNode("os-release", "-rw-r--r--", "root", "root", 107,
                        'NAME="Fedora Linux"\nVERSION="40"\nID=fedora\nVERSION_ID=40\nPRETTY_NAME="Fedora Linux 40"\n'),
                    "passwd": FileNode("passwd", "-rw-r--r--", "root", "root", 92,
                        "root:x:0:0:root:/root:/bin/bash\n"),
                    "group": FileNode("group", "-rw-r--r--", "root", "root", 38, "root:x:0:\n"),
                    "machine-info": FileNode("machine-info", "-rw-r--r--", "root", "root", 120,
                        "CHASSIS=\"mini-pc\"\nHARDWARE_VENDOR=\"Minisforum\"\nHARDWARE_MODEL=\"X1 AI Pro 470\"\nHARDWARE_SKU=\"X1-AIPRO-470\"\n"),
                }),
            "opt": DirNode(name="opt", mode="drwxr-xr-x", owner="root", group="root",
                children={
                    "translator": DirNode(name="translator", mode="drwxr-xr-x", owner="root", group="root",
                        children={
                            "occam2c.py": FileNode("occam2c.py", "-rwxr-xr-x", "root", "root", 0, ""),
                            "README": FileNode("README", "-rw-r--r--", "root", "root", 248,
                                "Occam-to-C Translator\n=====================\n\nThis tool converts Occam source code (for INMOS Transputers)\nto compilable C code using pthreads for parallel execution.\n\nUsage: python3 occam2c.py <input.occ> > output.c\n"),
                        }),
                }),
            "home": DirNode(name="home", mode="drwxr-xr-x", owner="root", group="root",
                children={
                    "vak": DirNode(name="vak", mode="drwxr-xr-x", owner="vak", group="vak",
                        children={}),
                }),
            "root": DirNode(name="root", mode="drwx------", owner="root", group="root",
                children={
                    ".bashrc": FileNode(".bashrc", "-rw-r--r--", "root", "root", 38,
                        "export PS1='[\\u@\\h \\W]\\$ '\n"),
                }),
            "proc": DirNode(name="proc", mode="dr-xr-xr-x", owner="root", group="root",
                children={
                    "cpuinfo": FileNode("cpuinfo", "-r--r--r--", "root", "root", 280,
                        "processor\t: 0\nvendor_id\t: AuthenticAMD\ncpu family\t: 26\nmodel\t\t: Ryzen AI 9 HX 370\nmodel name\t: AMD Ryzen AI 9 HX 370\ncpu cores\t: 12\n"),
                    "meminfo": FileNode("meminfo", "-r--r--r--", "root", "root", 200,
                        "MemTotal:       65900368 kB\nMemFree:        58239120 kB\nMemAvailable:   61234560 kB\n"),
                    "version": FileNode("version", "-r--r--r--", "root", "root", 48,
                        "Linux version 6.8.5-301.fc40.x86_64\n"),
                }),
            "tmp": DirNode(name="tmp", mode="drwxrwxrwt", owner="root", group="root",
                children={}),
            "dev": DirNode(name="dev", mode="drwxr-xr-x", owner="root", group="root",
                children={
                    "null": FileNode("null", "-rw-rw-rw-", "root", "root", 0, ""),
                    "zero": FileNode("zero", "-rw-rw-rw-", "root", "root", 0, ""),
                }),
        },
    )


def populate_minisforum_content(fs: DirNode) -> None:
    def _find(path: str):
        from .filesystem import find_node
        return find_node(fs, path)

    def _file(path: str, content: str) -> None:
        from .filesystem import find_node
        n = find_node(fs, path)
        if isinstance(n, FileNode):
            n.content = content
            n.size = len(content)

    _file("/etc/passwd",
        "root:x:0:0:root:/root:/bin/bash\n")

    _file("/etc/hostname", "minisforum-x1\n")

    # The occam2c.py translator — write as external script content
    _file("/opt/translator/occam2c.py",
        '#!/usr/bin/env python3\n'
        '"""occam2c.py - Occam to C translator."""\n'
        'import sys\n'
        'def trans(src):\n'
        '    o=[];ind=0;pn="vm"\n'
        '    o.append("// occam2c output");o.append("#include <stdio.h>")\n'
        '    o.append("#include <pthread.h>");o.append("")\n'
        '    for L in src.split("\\n"):\n'
        '        s=L.strip()\n'
        '        if not s or s.startswith("--"): continue\n'
        '        if s.startswith("#USE"): continue\n'
        '        if s.startswith("PROC "):\n'
        '            e=s.find("(")\n'
        '            if e>4: pn=s[5:e].strip()\n'
        '            o.append("void* "+pn+"(void*a){");ind=1;continue\n'
        '        if s.startswith("CHAN "): continue\n'
        '        if s=="WHILE TRUE": o.append(" while(1){");ind+=1;continue\n'
        '        if s in ("SEQ","PAR","ALT","IF"): continue\n'
        '        if ":=" in s:\n'
        '            p=s.split(":=",1);v=p[0].strip();vl=p[1].strip().rstrip(":")\n'
        '            o.append(" int "+v+"="+vl+";");continue\n'
        '        if "!" in s or "?" in s: continue\n'
        '        if s=="SKIP": o.append(" ;");continue\n'
        '        if s in (":","::"): o.append("}");ind=max(0,ind-1);continue\n'
        '    while ind>0: o.append("}");ind-=1\n'
'    o.append("");o.append("int main(int c,char**v){")' '\n'
'    o.append("  printf(\\"vak-linux v0.9\\\\n\\");")\n'
'    o.append("  printf(\\"ready\\\\n\\");")\n'
'    o.append("  fflush(stdout);"+pn+"(0);return 0;}")\n'
'    return "\\n".join(o)\n'
        'if len(sys.argv)>1:\n'
        '  with open(sys.argv[1]) as f: print(trans(f.read()))\n')
