# VAK-NODE-7 — Save Slot Progress

The game tracks player progress through 14 milestones. Progress is shown as a percentage in `slots` / `--list` output.

## Milestones (14 total)

| # | Flag | Trigger | Phase |
|---|---|---|---|
| 1 | `narr_intro_shown` | Start game / view intro | Discovery |
| 2 | `read_design` | `cat design.md` | Sasha's Story |
| 3 | `found_sasha_passwd` | `cat auth.log` | Sasha's Story |
| 4 | `read_worm` | `cat worm.c` | Sasha's Story |
| 5 | `stringed_vak_core` | `strings /usr/local/vak/vak-core` | Sasha's Story |
| 6 | `default_route_set` | `ip route add default via 10.0.0.1` | Network |
| 7 | `sentinel_backdoor_activated` | Backdoor kill-switch or port knock | Sentinel |
| 8 | `vak_export_ready` | `tar czf ... /home/vak` | Export |
| 9 | `vak_sent` | `nc veldhaaven.net 8080` | Export |
| 10 | `minisforum_ssh` | `ssh root@10.0.0.2` | Migration |
| 11 | `sources_copied` | `scp *.occ` to Minisforum | Migration |
| 12 | `compilation_done` | `gcc -pthread -o vak_core` on Minisforum | Migration |
| 13 | `vak_migrated` | `./vak_core` on Minisforum | Migration |
| 14 | `vak_bond_earned` | Any +1 bond action | Bond |

## Progress table

| Milestones earned | Progress |
|---|---|
| 0 | 0% |
| 1 | 7% |
| 2 | 14% |
| 3 | 21% |
| 4 | 28% |
| 5 | 35% |
| 6 | 43% |
| 7 | 50% |
| 8 | 57% |
| 9 | 64% |
| 10 | 71% |
| 11 | 78% |
| 12 | 85% |
| 13 | 93% |
| 14 | 100% |

## Save file location

`vak_game/data/saves/<slot>.json`

## Networking puzzle flags

| Flag | Purpose |
|------|---------|
| `vak_net_ifconfig_attempted` | First `ifconfig eth0 up` with AUI error |
| `vak_net_physical_setup_done` | Player confirmed BNC hardware connected |
| `vak_net_driver_fixed` | `aui_disable=1` written to `/proc/vak/netconfig` |
| `network_up` | Interface is up (set by `ifconfig eth0 up`) |
| `default_route_set` | Route added (gates sentinel timer) |

See `/home/adv/PROGRESS.md` for full session summary and file-by-file work record.
