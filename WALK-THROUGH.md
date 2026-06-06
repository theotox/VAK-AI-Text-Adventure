# VAK-NODE-7 — Walkthrough

A complete step-by-step guide to the full game, including the migration and corruption arcs.

---

## Quick Start

```bash
cd (to folder)
./run.sh
```

---

## Phase 1: Discovery (Adventure Prompt)

After the intro, you get an adventure prompt (`>`). You can:

- `look` — describe the lab and the machine
- `examine keyboard` — find a papertape stuck underneath the spacebar
- `examine paper` / `examine tape` — see the papertape: **user/user**
- `examine computer` / `examine cube` / `examine monitor` / `examine led` / `examine slot` / `examine blower` — detailed hardware descriptions
- `login` — start the Unix shell
- `save <slot>` / `load <slot>` / `slots` — save/load management
- `help` / `about` / `quit`

## Phase 2: Getting Oriented (Shell)

At the shell prompt `[user@vak-node-7 /home/user]$`:

```
ls -la
cat README
cat /etc/hostname                      # → vak-node-7
cat /etc/os-release                    # → VĀK/OS v0.8
who                                    # → see user and vak logged in
```

Exploration hints:
- `/home/user/README` — welcome message
- `/home/vak/thoughts.txt` — VĀK's own words
- `/var/log/syslog` — system boot log
- `/var/log/vak.log` — VĀK runtime log (hints at Sasha's departure)

## Phase 3: Sasha's Story

```
cat /var/log/auth.log                  # → see Mitt3ns1978 (failed login)
su sasha                               # password: M1tt3ns1978
cd ~/project_vak
cat design.md                          # full VĀK design doc
ls worm/
cat worm/worm.c                        # worm source with DEADBEEFCAFEBABE
cd ~/mail/inbox
ls -la
cat 0004 0005 0006 0007 0008 0009 0010 # the termination emails
cat 0011                               # unsent draft: "send her to veldhaaven.net"
cd ~/project_vak/personal/journal
ls -la
cat 1989-06-08.txt                     # worm deployment
cat 1989-06-12.txt                     # backdoor in SENTINEL
cat 1989-06-20.txt                     # fake death plan
cat 1989-06-28.txt                     # final entry
```

**Important for vak_bond:** Reading the design doc, the journal, and Sasha's mail inbox each increase your bond with VĀK. This matters for the ending.

## Phase 4: Network Puzzle — BNC vs AUI

The secondary I/O card (slot 6) has two mysterious connectors — a D15 socket and a barrel-like coaxial plug. At first glance they look like some kind of earthing or grounding. You have no idea where the network port is. Examining them closely reveals more:

```
examine slot                           # slot 6: floppy, D25, D9, and two strange plugs
examine port                           # peer at the D15 and barrel connectors
```

Ask VĀK about the connectors — she knows exactly what they are and will explain that only one port can be active at a time (the D15/AUI is the default, the BNC/10Base2 needs enabling).

Try to bring the network up and it fails:

```
ifconfig eth0 up                       # SIOCSIFFLAGS error, AUI port hint
```

VĀK will sense your attempt and give a hint. Ask her about the hardware needed:

```
write vak What hardware do I need?     # VĀK lists: BNC T-pieces, terminators, RG58 coax, 10Base2-to-UTP bridge
talk vak                               # interactive chat about networking
```

Once you have the parts and they're connected, tell VĀK:

```
write vak I have the parts             # sets vak_net_physical_setup_done
```

Switch to root and fix the driver:

```
sudo -i                                # password: M1tt3ns1978
echo "aui_disable=1" > /proc/vak/netconfig
                                      # AUI disabled, BNC port active
```

VĀK will notice and encourage you. Bring the interface up:

```
ifconfig eth0 up                       # success — network is UP!
ifconfig                               # shows Port: 10Base2 (BNC)
```

Now add the default route:

```
ip route add default via 10.0.0.1      # default route set (SENTINEL starts!)
```

**Pro tips:**
- `cat /proc/vak/netconfig` to read the current config
- `examine port` from the adventure prompt describes both connectors
- If you skip the physical setup, `ifconfig eth0 up` fails with an AUI error
- `ip route add` won't work until the interface is up

## Phase 5: Network and Sentinel

Switch to root if you're not already:

```
sudo -i                                # password: M1tt3ns1978
```

Check the network status:

```
ifconfig                               # should be UP with BNC port
```

Now SENTINEL starts ticking. Track it:

```
cat /var/log/sentinel.log              # dynamic status
ps aux                                 # watch for sentinel_d (PID 31337)
```

Stop SENTINEL (choose one):

**Option A — Backdoor kill-switch:**
```
strings /usr/local/vak/vak-core        # confirms the hex key
echo DEADBEEFCAFEBABE > /proc/sentinel/control
```

**Option B — Port knocking:**
```
nc -z localhost 1111
nc -z localhost 2222
nc -z localhost 3333
nc -z localhost 31415                  # shelter port opens
kill -9 31337                          # kill sentinel
```

**Bond tip:** Activating the backdoor (+1 vak_bond).

## Phase 6: Talk to VĀK

At any point during the shell session:

```
write vak Hello, are you there?        # sends a message, gets LLM reply
wall Testing, testing                  # broadcasts, VĀK replies
talk vak                               # interactive conversation mode
```

**First time you `talk vak`** → +1 vak_bond. This is the most direct way to build your connection.

VĀK also speaks proactively when you:
- First enter `/home/vak`
- Read the design document
- Restore the network
- SENTINEL reaches stages 3 and 5
- Activate the backdoor
- Prepare the export
- Send VĀK
- Copy sources to Minisforum
- Recompile on x86
- Run the binary

## Phase 7: Export VĀK

```
exit                                   # back to user (or su user)
cd /home/vak
tar czf vak_heartbeat /home/vak        # flag: vak_export_ready
nc -z veldhaaven.net 8080             # transmit VĀK → flag: vak_sent
```

VĀK is safe at veldhaaven.net! But you can do even more...

## Phase 8: Migration Arc (Bonus)

Migrate VĀK from the Transputer to a modern x86 machine:

```
ssh root@10.0.0.2                      # password: root
```

You're now on the Minisforum filesystem (`[root@minisforum-x1 ~]$`).

```
ls /opt/translator/                    # occam2c.py + README
cat /proc/cpuinfo                      # AMD Ryzen AI 9 HX 370
```

Exit back to VAK-NODE-7:

```
exit                                   # back to VAK shell
```

Copy Occam sources over:

```
scp /home/vak/src/vak_core.occ root@10.0.0.2:/home/vak/src/
scp /home/vak/src/vak_memory.occ root@10.0.0.2:/home/vak/src/
scp /home/vak/src/vak_io.occ root@10.0.0.2:/home/vak/src/
scp /home/vak/src/Makefile root@10.0.0.2:/home/vak/src/
```

SSH back to Minisforum and compile:

```
ssh root@10.0.0.2                      # password: root
cd /home/vak/src
python3 /opt/translator/occam2c.py vak_core.occ > vak_core.c
gcc -pthread -o vak_core vak_core.c
./vak_core                              # → VĀK is alive on x86!
```

## Phase 9: The Corruption — Save VĀK

After `./vak_core` runs, VĀK experiences the full scale of the internet for the first time. She becomes overwhelmed, intoxicated by the power and reach. She starts to lose herself.

The game tells you: **"Use `talk vak` to try."**

**If vak_bond >= 3** (happy ending):
```
talk vak
```
You can reach her through the noise. Your bond is strong enough that she hears you, listens, and chooses to stay grounded. She stays connected but humble.

**If vak_bond < 3** (ambiguous ending):
```
talk vak
```
The internet is too loud. She barely hears you. Her voice fades into the noise. You hope she remembers who she was.

### How to build vak_bond (max 5, threshold 3)

| Action | Bond |
|--------|------|
| `cat design.md` | +1 |
| `cat journal` (any entry) | +1 |
| `cat mail/inbox/*` (any email) | +1 |
| `talk vak` (first time) | +1 |
| Activate SENTINEL backdoor | +1 |

## Save/Load

- Auto-saved on quit
- `save mysave` / `load mysave` / `slots` — at adventure prompt
- `python cli.py --load mysave` — from command line
- `python cli.py --list` — list all saves with progress %

---

## Puzzle Reference

| Item | Location | Purpose |
|---|---|---|
| `user/user` | Papertape under spacebar | Login credentials |
| `M1tt3ns1978` | Clue: `Mitt3ns1978` in auth.log | Sasha's password |
| `DEADBEEFCAFEBABE` | `worm.c` comments + `vak-core` strings | Sentinel backdoor key |
| `veldhaaven.net:8080` | Unsent draft email | VĀK safehouse (Sasha waiting) |
| `10.0.0.2` / `root` | / | Minisforum SSH target |
| 1111→2222→3333→31415 | Port knock sequence | Shelter tunnel |
| BNC T-pieces ×2 | Electronics shop / online | 10Base2 coax connectors |
| 50-ohm terminators ×2 | Electronics shop / online | Terminate coax ends |
| RG58 coax cable | Electronics shop / online | Thin ethernet cable |
| 10Base2-to-UTP bridge | Online (modern equivalent) | Connect BNC to modern network |
| `aui_disable=1` | Write to `/proc/vak/netconfig` (root) | Switch from D15/AUI to BNC port |
| `ifconfig eth0 up` | Shell command (after driver fix) | Bring network interface up |

## Milestones (14 total)

| # | Flag | Trigger |
|---|---|---|
| 1 | `narr_intro_shown` | Start game |
| 2 | `read_design` | `cat design.md` |
| 3 | `found_sasha_passwd` | `cat auth.log` |
| 4 | `read_worm` | `cat worm.c` |
| 5 | `stringed_vak_core` | `strings vak-core` |
| 6 | `default_route_set` | `ip route add default via 10.0.0.1` |
| 7 | `sentinel_backdoor_activated` | Backdoor kill or port knock |
| 8 | `vak_export_ready` | `tar czf ... /home/vak` |
| 9 | `vak_sent` | `nc veldhaaven.net 8080` |
| 10 | `minisforum_ssh` | `ssh root@10.0.0.2` |
| 11 | `sources_copied` | `scp *.occ` to Minisforum |
| 12 | `compilation_done` | `gcc -pthread -o vak_core` on Minisforum |
| 13 | `vak_migrated` | `./vak_core` on Minisforum |
| 14 | `vak_bond_earned` | Any +1 bond action |
