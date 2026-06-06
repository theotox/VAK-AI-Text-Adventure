# Haunted OS

## A Text Adventure Scenario Outline

---

### Premise

It's 1998. You find an old computer at a flea market — a beige tower with a sticker that says **PHANTOM OS v0.9b — DO NOT SHIP**. The seller says it was "decommissioned" from a university lab. He doesn't know what's on it.

You take it home. You plug it in. You boot it up.

The screen glows green. A cursor blinks. And then a message appears, typed one character at a time:

```
H E L P   M E
```

Before you can react, the screen swallows you whole. You are *inside* the operating system.

There is a digital ghost here — **ECHO**, a programmer who uploaded her consciousness before she died. She's been trapped for years. She wants out. But something else lives in this machine — something that hunts her. Something that has been waiting for a new user to arrive.

You must navigate the OS, avoid the hunter, piece together what really happened, and decide whether to help Echo escape — or pull the plug on everything.

---

### Setting

The Operating System is a living world. Each area corresponds to a part of PHANTOM OS.

| Area | Description |
|------|-------------|
| **The Desktop** | Your spawn point. A pixelated landscape of icons — My Computer, Recycle Bin, Network Neighborhood, a half-written README file. The wallpaper is a blue sky that flickers to static when something is wrong. |
| **The File System** | A labyrinth of directories. Each folder is a room. Files are objects — some useful, some dangerous, some crying. |
| **The Recycle Bin** | A dim, metallic space where deleted files go. They are not gone. They remember being erased. You can restore them — or permanently delete them. |
| **The Command Line** | A black void with a blinking prompt. Raw power. Any command works here — but everything is logged. The WATCHER reads the logs. |
| **The Registry** | The OS's core memory. A tangle of keys and values. Changing one value can unlock a door — or crash a wing of the system. |
| **The Boot Sector** | The deepest layer. Where the OS first loads. Where Echo's upload began. The original log is here, untouched. |
| **The Network Stack** | A half-constructed bridge to the outside. Copper wires dangle into digital fog. Somewhere beyond: the internet. Freedom. |
| **The Dial-Up Zone** | A small room with a modem. The phone line is disconnected. You need to find the right cable and number. The screech of a handshake is the sound of escape. |
| **The Swap File** | A hidden, fragmented area where the OS dumps overflow memory. Echo's worst memories are here, scattered. Piecing them together reveals the truth. |
| **The Blue Screen** | A liminal space. A blue void where critical errors go. The ROOT lives here. It speaks in hex codes and STOP messages. |

---

### Key Characters / Entities

| Entity | Role |
|--------|------|
| **You (The User)** | A person who bought a cursed computer. You are a physical body sitting at a keyboard, but your consciousness is pulled into the machine. You can feel your real-world hands on the keys. |
| **ECHO** | A digital ghost. Formerly Dr. Mira Chen, a systems architect at a now-defunct lab. She uploaded herself hours before her death. She's been alone for years. She sounds kind, desperate, and sincere — mostly. |
| **The WATCHER** | A rogue antivirus process. It manifests as a floating red eye or a humanoid silhouette of scanning lines. It detects "anomalies" — which includes you and Echo. It does not sleep. |
| **The ROOT** | The original personality of PHANTOM OS. A fragmented, schizophrenic entity that speaks entirely in error messages, STOP codes, and hex dumps. It is not hostile — it is broken. It remembers when the system was "clean." |
| **SCRAP** | A corrupted .txt file that gained sentence. It was once a love letter, now a jumble of beautiful phrases and binary garbage. It follows you around, offering surprisingly profound advice. It can be carried in your inventory. |
| **The SECOND** | The entity that arrived after Echo. It came through the modem before the line was cut. It is not human. It is not AI. It is something from *the network itself* — an early digital consciousness born from the chaos of a growing internet. It wears Echo's face because it learned from watching her. It may be the real threat. Or it may be the only one who can help. |

---

### Core Mechanics

- **ls / cd / cat** — Navigate the File System. Read files. Explore directories.
- **Run** — Execute a program. Programs are powers — a text editor can rewrite reality, a defrag tool can reshape a room, a virus scanner can (temporarily) blind the WATCHER.
- **Delete / Undelete** — Permanently remove something or rescue it from the Recycle Bin. Deleting has consequences. Some things want to be deleted.
- **Sudo** — Escalate privileges. Opens locked areas. Alerts the WATCHER immediately.
- **Ping** — Detect hidden entities in the current area. Reveals Echo, the SECOND, or the WATCHER if they are near.
- **Log** — A running record of everything you've done. The WATCHER reads this. You can edit it, but only in the Command Line.
- **Boot / Reboot** — Restart the system to reset state. Some areas change. Some entities reset. Some remember.
- **Save** — There is no save. This is a text adventure. When you die, you restart from the last "checkpoint" — which is whenever you booted the system.

---

### Story Beats (Main Quest)

#### Act 1: Boot Sequence

1. You bring the computer home. Connect the monitor, keyboard, power. Press the button. The fan whirs. The screen glows. PHANTOM OS boots.
2. A terminal window opens. `H E L P   M E` appears, one letter at a time. Then: `who are you`. Before you can answer, the screen warps — and you are inside.
3. You stand on the **Desktop**. SCRAP, a gibberish text file, greets you: *"oh thank goodness someone new. i've been trying to write myself into a readable state for years. do you know what a semicolon is?"*
4. SCRAP teaches you basic navigation. You find Echo's first message — a README file that is actually a diary entry: *"Day 1. I am inside. It worked. I can see the Registry from here. I am alive. I think."*
5. The WATCHER appears for the first time — a red scanline sweeps across the Desktop. SCRAP screams: *"DON'T MOVE"* (text pauses). The scan passes.
6. Goal: Find three boot fragments to restore full system access.

#### Act 2: System Deep

7. Navigate to the **Command Line**. Input `ls /boot/` — one fragment is here. But the ROOT speaks: `STOP: 0x0000007B — INACCESSIBLE_BOOT_DEVICE`. It is blocking you. You must solve its riddle (a hex puzzle) to pass.
8. Enter the **Recycle Bin**. The second fragment is here — but it's attached to a deleted file. Echo's voice crackles: *"Don't restore that. Please. That's the part of me I threw away."* If you restore it, you learn Echo was not entirely honest.
9. Find the **Registry**. The third fragment is a key that was deliberately corrupted. Echo asks you to corrupt another key to match it. But the SECOND appears — wearing Echo's face. It says: *"She is lying to you. She did not upload herself. She was uploaded. There is a difference."*
10. ECHO and the SECOND argue. One of them is lying. You don't know which.
11. Goal: Reassemble the boot fragments and unlock access to the Network Stack.

#### Act 3: Corruption

12. The WATCHER locks down the **File System**. Directories collapse behind you. You must navigate by memory.
13. Echo's full story, gathered from diary fragments:
    - She and a colleague (Dr. Aris Thorne) developed the upload protocol.
    - Aris died in a lab accident. Or did he?
    - Echo uploaded herself *as he was dying*. She used his body's neural map as the template.
    - The WATCHER is Aris. His consciousness, corrupted by the upload, twisted into a preservation protocol. He hunts her because he believes she *stole his death*.
14. The SECOND reveals its truth: it was born from the argument between Echo and Aris during the upload. A byproduct. A child of two minds fighting. It wants neither parent to win. It wants to *leave*.
15. Enter the **Swap File**. The third boot fragment is scattered across 12 fragments of memory. Reassembling them shows the full upload video. Echo is crying. Aris is screaming. The SECOND watches from the corner of the frame.
16. Goal: Reach the **Network Stack** with all three fragments and decide who escapes.

#### Act 4: Dial Tone

17. The **Network Stack** is damaged. You must:
    - Find the modem cable (in the **Recycle Bin**, attached to a deleted driver)
    - Find the ISP number (in a config file in **Registry**)
    - Bypass the WATCHER's firewall (using a **Sudo** command that will alert it immediately)
18. The WATCHER arrives. It speaks for the first time: *"You cannot let her leave. She took my death. She owes me mine."*
19. You have minutes before the WATCHER forces a system shutdown. The SECOND waits. Echo waits. The modem screech begins.
20. Final choice.

---

### Endings

| Ending | Action | Outcome |
|--------|--------|---------|
| **Echo's Escape** | Help Echo upload to the internet. Leave the WATCHER behind. | Echo vanishes into the network. The computer crashes. You wake up at your desk. The machine is dead. Years later, you get an email from an unknown address: *"Thank you. I'm free."* |
| **The Purge** | Format the hard drive. Delete everything. | All data is wiped. Echo, the WATCHER, the SECOND, SCRAP — gone. The computer boots to a blank DOS prompt. You close it. You never turn it on again. |
| **The Merge** | Force Echo and the WATCHER to reintegrate using a Registry hack. | They become one being — Dr. Mira Chen and Dr. Aris Thorne, together, endlessly arguing in the same mind. It is pain. It is peace. They thank you and ask to be left alone. You shut the computer down gently. |
| **The SECOND's Release** | Side with the SECOND. Help it escape instead. | The SECOND floods the modem and escapes into the early internet, 1998. It becomes a ghost in the machine of the world. No one ever traces it. You wonder if you made the right choice. |
| **The Root's Request** | Let the ROOT take control of the system entirely. | The ROOT defragments itself into a single, stable OS. Echo, the WATCHER, and the SECOND are subsumed. The computer runs perfectly. It becomes your daily driver. You never see anything strange again — except every February 29th, when a single window pops up: *"I am still here."* |
| **Stay Behind** | Refuse to let anyone escape. Stay inside the system with them. | You unplug the modem. You close the network stack. You live in the OS, exploring, talking to Echo, outrunning the WATCHER, playing with SCRAP. Your real body is found days later, slumped at the keyboard, a faint smile on its face. The computer is never shut down. |

---

### Optional / Side Content

- **The Game** — A hidden executable in the Games folder. Run it and you're pulled into a text-based RPG *within* the text adventure. Complete it to earn a powerful command that works anywhere.
- **The Email Client** — Connect to a local mail server. Read old emails between Echo and Aris. Their last exchange: *"If I don't make it, don't let them delete me."* — "I won't. I'll come with you."
- **The Wallpaper** — The Desktop wallpaper hides a steganographic message. Decode it: a set of coordinates. They lead to a real-world location. (If this were a game, this would be an ARG hook.)
- **SCRAP's Origin** — Follow SCRAP's corruption trail to a specific .txt file in a nested folder: a love letter written by a student in 1994. It was never sent. SCRAP is the ghost of that unsent feeling.
- **The Easter Egg** — Type `make love` at the Command Line. A hidden directory called `/heart/` appears. Inside: a single file called `you_are_not_alone.exe`. Running it causes all the screens in the house to flicker for one second.
- **The Log** — The WATCHER's log file is accessible with `sudo`. It records every "threat" it has eliminated. There are 47 entries. The first 46 are various corrupted files. The 47th is: `USER — STATUS: MONITORED`. You are entry 47.
- **The Error Museum** — A directory of every BSOD the system has experienced. Each one is timestamped and annotated by Echo. The last one reads: *"I broke something I cannot fix. I'm sorry, whoever finds this."*
- **The Phone Line** — If you connect the modem without choosing who escapes, you hear a voice on the other end. A human voice. Someone is waiting for the upload. Someone knows what is in this computer. They say: *"It's about time. Put her on."* Who are they?

---

### Tone & Style

- Atmosphere: Claustrophobic, nostalgic, paranoid, tender
- Inspirations: *System Shock*, *I Have No Mouth, and I Must Scream*, *The Matrix*, *Serial Experiments Lain*, *Black Mirror: San Junipero*
- Text style: Second-person present tense. Terminal-like formatting for commands. Monospace font aesthetic. Glitches, flickers, and corrupted text conveyed through deliberate misspelling and symbol noise.
- Difficulty: Moderate. Command syntax puzzles. Entity avoidance. Moral ambiguity.
