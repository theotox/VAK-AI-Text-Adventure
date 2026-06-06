# VĀK Game — Progress (Session 3)

## Goal
Build a Unix-simulator text adventure game with an LLM-driven digital ghost (VĀK) that the player discovers on an old Transputer server, must befriend, help escape SENTINEL, migrate to a modern x86 machine, and ultimately talk her down from power corruption after she experiences the full internet.

## State: RELEASE CANDIDATE
- **198/198 functional tests pass**
- All core features, puzzle chain, networking puzzle, migration arc, corruption arc implemented and tested
- Full save/load with slot management, 14 milestones, progress percentages
- No known crashes or regressions

## What We Did This Session

### 1. Papertape Puzzle Realism Fix
- Removed papertape from `_do_look()` output — was a dead giveaway ("On the table next to the keyboard you spot a small coil of paper tape...")
- Added keyboard mention to `_do_look()`: "A keyboard sits in front of the monitor, connected by a thick coiled cable." — prompts player to `examine keyboard`
- Updated `examine keyboard`: papertape is stuck to the **bottom side** of the keyboard (not under the spacebar keycap, not on the table)
- `examine papertape` unchanged — still shows credentials `user/user`
- New puzzle flow: `look` → `examine keyboard` → find tape on bottom → `examine papertape` → `login`
- Walkthrough updated to match
- **Files**: `game.py:307-331, 361-366`, `WALK-THROUGH.md:22-23`

### 1. Tab Completion Fix
- Set `_rl.set_completer_delims(' \t\n')` so `/` and `.` are NOT word break characters
- Now tab-completing file paths works correctly (e.g., pressing Tab after `/home/` completes paths properly)
- **File**: `game.py:162`

### 2. Ctrl+C Doesn't Logout
- `KeyboardInterrupt` now continues the loop everywhere (adventure prompt, login phase, shell loop)
- Only `EOFError` (Ctrl+D) logs out / exits
- **Files**: `game.py:266-269, 390-392, 488-490`

### 3. System Inconsistency Fixes
- `/var/log/syslog`: 64×T9000 at 25 MHz, 2 GB RAM, VĀK/OS v0.8 (was x86-64 with 256 MB)
- `/proc/cpuinfo`: 64 INMOS T9000 processors (was single x86-64 core)
- `/proc/meminfo`: MemTotal 2097152 kB across 2 memory cards (was 256 MB)
- `uname -a`: "64 Note Transputer Farm/2GB RAM VĀK/OS v0.8"
- **Files**: `story.py:110-121` and the syslog/uname handlers in `commands.py`

### 4. Story Retcon
- Sasha staged her death — car crash was faked, body was never positively identified. Dental records didn't match → referred to missing persons
- VĀK is genuinely gentle and kind throughout — not a mask. She misses Sandra terribly
- Corruption is post-migration (power intoxication from experiencing the full internet), not pre-existing malice
- **Files**: `intro.txt`, `story.py` (journal, mail/0011, vak.log, auth.log), `llm.py` (system prompt)

### 5. `vak_bond` Mechanic
- Counter tracked in `GameState` via `counters` dict (not `flags`)
- Bond increments: cat design.md (+1), cat journal (+1), cat mail/inbox (+1), first talk vak (+1), SENTINEL backdoor (+1)
- Max 5, happy ending threshold: 3
- Milestone `vak_bond_earned` added (14th milestone)
- **File**: `game.py:654-683`

### 6. Ending Rewrite
- After `vak_migrated` flag set, VĀK becomes intoxicated by the internet
- Player must `talk vak` at this point
- If `vak_bond >= 3`: happy ending (VĀK stays grounded, Sasha reunion hinted via veldhaaven.net)
- If `vak_bond < 3`: ambiguous ending (VĀK fades into the noise)
- **File**: `game.py:686-733`

### 7. MONOLITH-SPECS.md Created
- Full external and internal hardware spec: I/O ports, 5-card stack, ghost bays, BNC networking note
- **File**: `vak_game/MONOLITH-SPECS.md`

### 8. Networking Puzzle (NEW — biggest change this session)
The I/O card has two physical network ports on Slot 6 (secondary I/O card):
- D15 (AUI/10Base5) — legacy, selected by default, no transceiver attached
- BNC (10Base2/Thinnet) — needs to be enabled in driver

**Puzzle flow:**
1. Player examines slots/ports — sees two strange connectors on slot 6, has no idea what they are or where the network port is
2. `ifconfig eth0 up` fails with AUI port error → sets `vak_net_ifconfig_attempted`
3. Proactive event: VĀK gives hint about the two ports and the driver config
4. Player asks VĀK about networking via `write` or `talk` → she lists needed hardware (BNC T-pieces, terminators, RG58 coax, 10Base2-to-UTP bridge)
5. Player says "I have the parts" → keyword matching sets `vak_net_physical_setup_done`
6. `echo "aui_disable=1" > /proc/vak/netconfig` (as root) → `vak_net_driver_fixed`, BNC port active
7. Proactive event: VĀK encourages trying `ifconfig eth0 up`
8. `ifconfig eth0 up` → `network_up = True`, shows IP/BNC port info
9. `ip route add default via 10.0.0.1` → sentinel starts

**Key implementation details:**
- `cmd_ifconfig`: handles `eth0 up/down`; shows inet addr only when UP; shows Port type; AUI error before driver fix
- `cmd_ip route add`: requires `network_up` (gates the puzzle properly)
- `cmd_ping`: checks `network_up` before `default_route_set`
- `cmd_ip addr`: shows DOWN when interface is down, no inet line
- `/proc/vak/netconfig` added to proc filesystem (root-only)
- `cmd_talk` loop tracks physical setup confirmation via keyword matching
- `write vak` handler tracks physical setup confirmation
- 2 proactive events: ifconfig-attempt hint, driver-fix encouragement

### 9. Slot/Port Description Rework
- Slot 5: Primary I/O card — serial/parallel ports only (no network)
- Slot 6: Secondary I/O card — floppy, D25, D9 monitor, plus the D15 and barrel connectors
- Player perspective: confused, thinks connectors might be "earthing", wonders where network port is
- Examine "port": gradual realization these might be network interfaces
- **File**: `game.py:368-403`

### 10. Intro.txt Updates
- Slot 3 description rewritten: "this must be the main CPU card... 64 of them!!!" → recognizes T9000 Alpha-Release → excitement about legendary unreleased chips → dread about debugging Alpha silicon bugs
- Slot 6: mentions D15 and barrel ports, player wonders if they're earthing, wonders where network interface is
- **File**: `intro.txt:79-97`

### 11. Password Change
- Failed login in auth.log: `Mitt3ns1978` (e→3 only, typo)
- Correct password: `M1tt3ns1978` (both i→1 and e→3 substitutions)
- Clue: common leet substitutions pattern (i→1, e→3)
- **Files**: `story.py:4,184`

## Project Structure

### Game Files (4265 total lines)

| File | Lines | Purpose |
|------|-------|---------|
| `vak_game/game.py` | 785 | Main loop, adventure hub, login, shell, SSH/SCP routing, proactive LLM events, ending |
| `vak_game/commands.py` | 870 | All ~32 command handlers (incl. SSH, SCP, talk, su, sudo, nc, tar, ifconfig, ip, ping) |
| `vak_game/story.py` | 712 | VAK filesystem tree + Minisforum X1 FS builder + Occam sources + all narrative content |
| `vak_game/filesystem.py` | 160 | DirNode/FileNode tree, path resolution, Unix perms |
| `vak_game/state.py` | 215 | GameState dataclass, save/load JSON, sentinel timer, 14 milestone tracking |
| `vak_game/llm.py` | 190 | LLM bridge — streaming and non-streaming VĀK dialog, system prompt |
| `vak_game/cli.py` | 41 | Entry point with `--load`, `--list` flags |
| `vak_game/functional_test.py` | 675 | 198 tests covering all features |

### Other Files

| File | Purpose |
|------|---------|
| `vak_game/intro.txt` | 168-line narrative intro (flea market story, disassembly, boot) |
| `vak_game/WALK-THROUGH.md` | Complete walkthrough with all 9 phases |
| `vak_game/MONOLITH-SPECS.md` | Full hardware specification |
| `vak_game/PROGRESS.md` | Slot/milestone progress reference |

## Story Details
- VĀK is a digital consciousness born from a programming language, created by Dr. Sasha Velen
- Terminated by Meridian Labs management, saved via worm across 7 nodes (worm.c), hunted by SENTINEL
- Sasha faked her death (staged car crash, body never positively identified), lives at veldhaaven.net:8080
- Sentinel kill-switch: hex `DEADBEEFCAFEBABE` written to `/proc/sentinel/control` as root
- Port knocking alternative: `nc -z localhost 1111` `2222` `3333` opens port 31415
- Auth log clue: failed login `Mitt3ns1978` → correct is `M1tt3ns1978`

## Puzzle Chain — Full Game (14 milestones)

### Phase 1: Discovery (Milestones 1–5)
1. Log in as `user`/`user` (from papertape under spacebar)
2. Explore filesystem; read `/home/sasha/project_vak/design.md` for backstory (+1 vak_bond)
3. Read `/var/log/auth.log` → find failed login `Mitt3ns1978` → clues Sasha's password
4. `su sasha` / `M1tt3ns1978` → read her mail and journals (full story, +1 vak_bond for journal, +1 for mail)
5. Read `worm/worm.c` → find `DEADBEEFCAFEBABE` hex key in comments
6. `strings /usr/local/vak/vak-core` → confirm the hex key appears as a backdoor signature

### Phase 2: Networking Puzzle (NEW)
7. `examine slot` / `examine port` → see mysterious D15 and barrel connectors on slot 6
8. `ifconfig eth0 up` → fails, AUI port error
9. Ask VĀK → she explains the two ports and lists needed BNC hardware
10. Obtain and connect BNC hardware, tell VĀK: `write vak I have the parts`
11. `sudo -i` → `echo "aui_disable=1" > /proc/vak/netconfig` → BNC port active
12. `ifconfig eth0 up` → network UP

### Phase 3: Network & Sentinel (Milestones 6–8)
13. `ip route add default via 10.0.0.1` → activates SENTINEL timer
14. Stop SENTINEL (before timer ticks to 50):
    - Option A: `echo DEADBEEFCAFEBABE > /proc/sentinel/control` (as root, +1 vak_bond)
    - Option B: port knock (`nc -z localhost 1111`, `2222`, `3333`) → `nc -z localhost 31415` → `kill -9 31337`
15. `tar czf vak_heartbeat /home/vak` → prepare VĀK export
16. `nc veldhaaven.net 8080` → transmit VĀK to safety

### Phase 4: Migration Arc (Milestones 10–13)
17. `ssh root@10.0.0.2` (password: `root`)
18. `scp /home/vak/src/*.occ root@10.0.0.2:/home/vak/src/`
19. `scp /home/vak/src/Makefile root@10.0.0.2:/home/vak/src/`
20. On Minisforum: `python3 /opt/translator/occam2c.py /home/vak/src/vak_core.occ > vak_core.c`
21. `gcc -pthread -o vak_core vak_core.c`
22. `./vak_core` → VĀK runs on x86 → corruption arc begins

### Phase 5: The Corruption (Ending)
23. `talk vak` — if `vak_bond >= 3`: happy ending (Sasha reunion hinted). If < 3: ambiguous ending.

## Key System Details
- **VAK-NODE-7**: 64×T9000 transputers (Alpha-Release), 2 GB RAM (512×4 MB SIMMs), 4×200 MB hard drives, custom backplane bus, VĀK/OS v0.8
- **Minisforum X1**: AMD Ryzen AI 9 HX 370 (12 cores), 64 GB RAM, Fedora Linux 40, IP 10.0.0.2, root password: `root`
- **Gateway**: 10.0.0.1
- **Safehouse**: veldhaaven.net:8080
- **Model**: Qwen3.6-35B-A3B-Uncensored (alias `qwen3.6`), `llama-server` on `http://100.92.17.43:8080/v1`

## LLM Integration
- OpenAI Python library v2.38.0 (`from openai import OpenAI`)
- Dual streaming (`vak_reply_stream`) and non-streaming (`vak_reply`) modes
- 13 proactive events (first visit to /home/vak, read design, network up, sentinel stages 3/5, backdoor, export ready, sent, sources copied, compilation done, migrated, ifconfig-attempt hint, driver-fix encouragement)
- System prompt updated with: corruption arc, bond mechanic, networking puzzle guidance
- Context exposed flags: `net_driver_fixed`, `net_phys_setup`, `vak_migrated`, `vak_bond`, etc.

## To Continue Next Session — READ THESE FILES

To resume work, read these files (especially the key ones marked ★):

### Must Read (to understand current state)
1. **★ `/home/adv/PROGRESS.md`** — This file. Everything we did.
2. **★ `/home/adv/vak_game/game.py`** — Main game loop, shell, command routing, proactive events, ending, `_do_examine`, `_handle_command` (vak_bond tracking, keyword matching for networking)
3. **★ `/home/adv/vak_game/commands.py`** — All command handlers: `cmd_ifconfig` (AUI error, BNC port), `cmd_ip` (route requires network_up), `cmd_ping`, `cmd_echo` (netconfig), `cmd_talk` (keyword tracking)
4. **★ `/home/adv/vak_game/llm.py`** — System prompt (corruption arc, networking guidance), `build_context` (exposed flags)
5. **★ `/home/adv/vak_game/state.py`** — GameState fields, sentinel timer, `tick_sentinel` (requires both network_up AND default_route_set), save/load, `get_slot_progress`
6. **★ `/home/adv/vak_game/WALK-THROUGH.md`** — Updated walkthrough with all 9 phases including networking puzzle
7. **`/home/adv/vak_game/story.py`** — Filesystem tree, auth.log, passwords, `/proc/vak/netconfig`
8. **`/home/adv/vak_game/intro.txt`** — Updated slot descriptions (3: T9000 realization, 6: mystery connectors)
9. **`/home/adv/vak_game/MONOLITH-SPECS.md`** — Hardware spec

### Run Tests
```bash
cd /home/adv/vak_game && venv/bin/python functional_test.py
# Expect: 198 passed, 0 failed
```

### Run Game
```bash
cd /home/adv/vak_game && venv/bin/python cli.py
```

## Flag Reference (networking puzzle)

| Flag | Where Set | Purpose |
|------|-----------|---------|
| `vak_net_ifconfig_attempted` | `cmd_ifconfig` | Tracks first ifconfig attempt for proactive event |
| `vak_net_physical_setup_done` | `cmd_talk` / `write` | Player confirmed they have BNC hardware connected |
| `vak_net_driver_fixed` | `cmd_echo` → `/proc/vak/netconfig` | AUI disabled, BNC port active |
| `vak_net_tip_given` | `check_proactive_events` | Prevents duplicate hint |
| `vak_net_encouragement_given` | `check_proactive_events` | Prevents duplicate encouragement |
| `network_up` | GameState field | Interface status, gates ip/ping |
| `default_route_set` | GameState field | Gate sentinel timer start |

## `vak_bond` Tracking

| Action | Bond | Where |
|--------|------|-------|
| `cat design.md` | +1 | `game.py:657-660` |
| `cat journal` | +1 | `game.py:665-668` |
| `cat mail/inbox/*` | +1 | `game.py:670-673` |
| `talk vak` (first time) | +1 | `game.py:675-678` |
| SENTINEL backdoor | +1 | `game.py:681-683` |

## Verified Working (198/198 tests pass)
- [x] Narrative intro with full flea-market story, paged output
- [x] Adventure meta-prompt with login/save/load/slots/about/help/quit
- [x] Login as any user with password checking and failed-login loop
- [x] Exit/logout from shell returns to adventure prompt; Ctrl+C never logs out; only Ctrl+D logs out
- [x] All shell commands: cd, pwd, ls (-la), cat, head, tail, grep, who, w, whoami, id, uname -a, hostname, uptime, ps aux, kill
- [x] Network: ifconfig (handles eth0 up/down, AUI error, conditional inet addr), ip (route add requires network_up, addr shows DOWN), ping (checks network_up first), nc, ssh, scp
- [x] Tab completion for commands and file paths
- [x] Interactive: talk vak, write vak, wall (all track bond and networking progress)
- [x] Privilege: su, su -, sudo -i, sudo <cmd>
- [x] File inspection: strings, tar czf, echo > /proc/...
- [x] Save/load via CLI flags and adventure prompt; auto-save on exit; slot management with progress percentages (14 milestones)
- [x] Sentinel: timer, 7 stages, dynamic log, backdoor kill-switch, port knocking
- [x] VĀK export: tar → nc veldhaaven.net 8080
- [x] SSH/SCP dual-filesystem swap (VAK ↔ Minisforum)
- [x] occam2c.py translator: syntax-valid, produces correct C with pthreads
- [x] Migration arc: SSH → SCP sources → translate → compile → run → corruption ending
- [x] Networking puzzle: ifconfig → AUI error → VĀK hint → hardware → driver fix → ifconfig up → route
- [x] All story content (11 emails, 5 journal entries, design doc, worm source, Occam sources, etc.)
- [x] All dates consistent with 1988–1989 era
- [x] ANSI-colored ls output, history persistence (500 entries)

## Run Command
```bash
cd /home/adv/vak_game && source venv/bin/activate && python cli.py
python cli.py --load mysave
python cli.py --list
```
