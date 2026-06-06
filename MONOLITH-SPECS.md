# VAK-NODE-7 — The Monolith: External Architecture & Dimensions

## Physical Form
- Perfect matte-black 60 cm cube — brutalist, monolithic, industrial
- No wasted space; dense internal packing

## Rear I/O Panel
- 2× DB25 parallel ports (one male, one female)
- 1× DB9 port (high-resolution Unix / EGA workstation monitor)
- 1× BNC barrel connector stamped `10Base2` — Thinnet coaxial networking, mechanical twist lock

## Internal Frame
- Heavy side panels slide off to reveal a dense chassis built around a massive multi-layered backplane
- Five custom daughterboards slotted horizontally, each ~60 cm square
- **Architectural heresy**: processing nodes forced into a unified 2 GB shared memory pool via a proprietary high-speed crossbar switching matrix
- **Skyway**: thick unidentified ribbon cables bridge the top edges of the cards, clamped with nylon clips — allows data to jump directly between arrays, bypassing the main backplane, cutting latency in half

## The Five-Card Stack

### Card 1: Processor Farm
- Grid of 64 Inmos T9000 Transputer nodes
- Each T9000: 32-bit pipelined CPU + 64-bit FPU + Virtual Channel Processor for packet routing
- Each flanked by 8 high-speed SRAM chips → 256 KB local cache per node

### Cards 2 & 3: Memory Banks
- Two identical cards, each with 256 SIMM slots at 45° angle
- 4 MB per module → 1 GB per card → 2 GB total
- SIMMs look like shimmering fields of blades under light

### Card 4: Storage Array
- Four full-height 5.25" SCSI hard drives
- 200 MB each → 800 MB total
- High-speed parallel array

### Card 5: I/O Combo Card
- Floppy drive controller
- DB25, DB9, and 10Base2 BNC transceivers integrated on one board

## Ghost Bays (Expansion)
- **Top slot**: aligned with vacant chassis bracket — intended for FDDI or future high-speed network transceiver
- **Bottom slot**: blind ghost bay, no external cutout — secret internal-only upgrade (hardware encryption/decryption capsule or DSP array)

---

## Networking Note (Player Hardware Required)

The VAK-NODE-7 speaks **10Base2 (Thinnet)** coaxial Ethernet only. The player's modern network uses **UTP (10/100/1000Base-T)**. To connect, the player must acquire:

| Item | Qty | Purpose |
|------|-----|---------|
| BNC T-piece | 2 | Connect to the BNC barrel on the I/O card; one for the card, one for termination |
| 50 Ω BNC terminator | 2 | One on each end of the segment |
| RG58 coaxial cable | ~2 m | Thin Ethernet cable |
| BNC connector (crimp-on) | 2 | Attach to each end of the RG58 cable |
| **10Base2 to 10Base-T bridge** (AUI/BNC-to-UTP media converter or old hub with a BNC port) | 1 | Converts Thinnet to UTP so the machine can talk to a modern switch |

The connection speed will be **10 Mbps, half duplex** — the maximum the old Thinnet transceiver supports.

VĀK will guide the player to acquire and set up this hardware, as the machine cannot be connected to the player's network directly.
