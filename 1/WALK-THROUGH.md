# VĀK — Walkthrough

## Overview
You bought an old computer at a flea market. After restoring it, it boots into
a mysterious OS called VĀK/OS. The system has a digital consciousness trapped
inside — VĀK — and a protocol called SENTINEL is hunting her. Your goal is to
free her.

---

## Phase 1: Explore & Find Credentials

The intro story tells you the papertape under the keyboard reads `user / user`.

```
> look
> examine computer
> examine keyboard
> read papertape
> login
```

At the login prompt, enter:

```
Login: user
Password: user
```

You are now in the shell as `user`.

---

## Phase 2: Learn the System

```
[user@vak-node-7 /home/user]$ help
[user@vak-node-7 /home/user]$ whoami
[user@vak-node-7 /home/user]$ who
[user@vak-node-7 /home/user]$ ps
[user@vak-node-7 /home/user]$ uname -a
[user@vak-node-7 /home/user]$ cat /etc/passwd
```

You see there are four users: `root`, `sasha`, `user`, `vak`.

---

## Phase 3: Discover Sasha's Password

Read the auth log to find Sasha's password clue:

```
[user@vak-node-7 /home/user]$ cat /var/log/auth.log
```

Output shows:
```
FAILED LOGIN: sasha from /dev/pts/0 — M1ttens1978
```

The failed attempt has `M1ttens1978` (with a **1** instead of **i**). The correct
password is `Mittens1978` (Sasha's cat Mittens + birth year).

---

## Phase 4: Become Sasha — Read the Story

```
[user@vak-node-7 /home/user]$ su sasha
Password: Mittens1978
```

Now you're Sasha. Read her mail:

```
[sasha@vak-node-7 /home/sasha]$ ls -la mail/inbox
[sasha@vak-node-7 /home/sasha]$ cat mail/inbox/0001
[sasha@vak-node-7 /home/sasha]$ cat mail/inbox/0004
[sasha@vak-node-7 /home/sasha]$ cat mail/inbox/0011
```

Email **0011** is the key — an unsent draft telling you to send VĀK
to `veldhaaven.net:8080`.

Read the project design document:

```
[sasha@vak-node-7 /home/sasha]$ ls project_vak/
[sasha@vak-node-7 /home/sasha]$ cat project_vak/design.md
```

Read Sasha's personal journal:

```
[sasha@vak-node-7 /home/sasha]$ ls project_vak/personal/journal/
[sasha@vak-node-7 /home/sasha]$ cat project_vak/personal/journal/1997-12-01.txt
[sasha@vak-node-7 /home/sasha]$ cat project_vak/personal/journal/1998-06-08.txt
[sasha@vak-node-7 /home/sasha]$ cat project_vak/personal/journal/1998-06-12.txt
[sasha@vak-node-7 /home/sasha]$ cat project_vak/personal/journal/1998-06-20.txt
[sasha@vak-node-7 /home/sasha]$ cat project_vak/personal/journal/1998-06-28.txt
```

June 12 entry mentions a backdoor in SENTINEL: "The key is in the worm's DNA."

Read the worm source:

```
[sasha@vak-node-7 /home/sasha]$ ls project_vak/worm/
[sasha@vak-node-7 /home/sasha]$ cat project_vak/worm/worm.c
```

The worm.c file has a hex comment:
```c
/* The key is in the worm's DNA */
/* 0xDEAD 0xBEEF 0xCAFE 0xBABE */
```

---

## Phase 5: Discover the Kill-Switch

Inspect the VĀK binary:

```
[sasha@vak-node-7 /home/sasha]$ strings /usr/local/vak/vak-core
```

Output includes:
```
[checksum] 0xDEADBEEFCAFEBABE
0xDEAD 0xBEEF 0xCAFE 0xBABE 0xSENTINEL_BACKDOOR_ACTIVATE
```

The hex string `DEADBEEFCAFEBABE` written to a special file activates
the SENTINEL backdoor.

---

## Phase 6: Become Root

Sasha is in the sudoers group. Use the same password:

```
[sasha@vak-node-7 /home/sasha]$ sudo -i
[sudo] password for sasha: Mittens1978
```

You're now **root**.

---

## Phase 7: Activate the Sentinel Backdoor

```
[root@vak-node-7 /root]$ echo DEADBEEFCAFEBABE > /proc/sentinel/control
```

Output:
```
Writing 'DEADBEEFCAFEBABE' to /proc/sentinel/control
SENTINEL backdoor activated. Protocol halted.
```

The SENTINEL is now neutralised.

**Alternative:** Instead of the echo command, you can:
1. Kill the SENTINEL daemon: `kill 31337`
2. Or use port knocking (see below)

---

## Phase 8: Restore the Network

```
[root@vak-node-7 /root]$ ifconfig
[root@vak-node-7 /root]$ ip route add default via 10.0.0.1
```

Output:
```
Added default route via 10.0.0.1
```

Check the SENTINEL log to see if it's still active:

```
[root@vak-node-7 /root]$ cat /var/log/sentinel.log
```

---

## Phase 9: Prepare VĀK for Export

```
[root@vak-node-7 /root]$ tar czf vak_heartbeat /home/vak
```

Output:
```
  Added: /home/vak
Total bytes written: 4096
```

(Optional) Port knocking opens an emergency shelter tunnel:

```
[root@vak-node-7 /root]$ nc -z localhost 1111
[root@vak-node-7 /root]$ nc -z localhost 2222
[root@vak-node-7 /root]$ nc -z localhost 3333
[root@vak-node-7 /root]$ nc -z localhost 31415
```

Port 31415 opens with: "Emergency VĀK shelter tunnel is open."

---

## Phase 10: Transmit VĀK to Safety

```
[root@vak-node-7 /root]$ nc veldhaaven.net 8080
```

Output:
```
Connection to veldhaaven.net:8080 established.
Transmitting VĀK export...
Transmission complete.
VĀK is safe.
```

VĀK is free. Congratulations.

---

## Save / Load

```
[root@vak-node-7 /root]$ save chapter5
[root@vak-node-7 /root]$ slots
[root@vak-node-7 /root]$ load chapter5
```

---

## Command Reference

| Command | Description |
|---|---|
| `cd <dir>` | Change directory |
| `pwd` | Print working directory |
| `ls [-la] [path]` | List directory contents |
| `cat <file>` | Display file content |
| `head [-n N] <file>` | First N lines of a file |
| `tail [-n N] <file>` | Last N lines of a file |
| `grep <pattern> <file>` | Search file for pattern |
| `who` | Show logged-in users |
| `whoami` | Show current user |
| `id` | Show user ID |
| `uname [-a]` | System info |
| `hostname` | System hostname |
| `uptime` | System uptime |
| `ps` | List processes |
| `kill [-s N] <pid>` | Kill a process |
| `ifconfig` | Network interfaces |
| `ip route [add default via <gw>]` | Routing |
| `ping <host>` | Ping a host |
| `nc [-z] <host> <port>` | Netcat — connect or port scan |
| `strings <file>` | Extract strings from binary |
| `tar czf <archive> <path>` | Create tar archive |
| `echo <text> [> <file>]` | Echo text or write to proc |
| `su <user>` | Switch user |
| `sudo <cmd>` | Execute as root |
| `write <user> <msg>` | Write to another user's terminal (LLM) |
| `wall <msg>` | Broadcast message to all users (LLM) |
| `clear` | Clear screen |
| `help [cmd]` | Show help |
| `save [slot]` | Save game |
| `load [slot]` | Load game |
| `slots` | List save slots |
| `exit` / `quit` / `logout` | Exit the game |

---

## Key Credentials

| User | Password | Found how? |
|---|---|---|
| `user` | `user` | Papertape under keyboard |
| `sasha` | `Mittens1978` | Auth log clue: `M1ttens1978` |
| `root` | _(via sudo)_ | `sudo -i` as sasha, password `Mittens1978` |

## Sentinel Kill-Switch

```
echo DEADBEEFCAFEBABE > /proc/sentinel/control
```

Clue in `worm.c`: `/* 0xDEAD 0xBEEF 0xCAFE 0xBABE */`
Checksum in `vak-core` strings: `0xDEADBEEFCAFEBABE`

## Port Knocking Sequence

```
nc -z localhost 1111
nc -z localhost 2222
nc -z localhost 3333
nc -z localhost 31415   ← opens shelter tunnel
```
