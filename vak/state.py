from __future__ import annotations
import json
import os
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Any

from .filesystem import DirNode, FileNode, INode

SAVE_DIR = Path(__file__).parent / "data" / "saves"


@dataclass
class GameState:
    cwd: str = "/home/user"
    current_user: str = "user"
    flags: dict[str, bool] = field(default_factory=dict)
    counters: dict[str, int] = field(default_factory=dict)
    sentinel_timer: int = 0
    sentinel_active: bool = False
    sentinel_stage: int = 0
    network_up: bool = False
    default_route_set: bool = False
    llm_history: list[dict] = field(default_factory=list)
    files_written: list[str] = field(default_factory=list)
    game_started: bool = False

    export: dict[str, Any] = field(default_factory=dict)

    # SSH/Miniforum state
    ssh_active: bool = False
    ssh_cwd: str = ""
    ssh_user: str = ""

    def get_flag(self, name: str) -> bool:
        return self.flags.get(name, False)

    def set_flag(self, name: str, value: bool = True) -> None:
        self.flags[name] = value

    def get_counter(self, name: str) -> int:
        return self.counters.get(name, 0)

    def inc_counter(self, name: str, amount: int = 1) -> int:
        self.counters[name] = self.counters.get(name, 0) + amount
        return self.counters[name]

    def set_counter(self, name: str, value: int) -> None:
        self.counters[name] = value

    def tick_sentinel(self) -> None:
        if not self.network_up or not self.default_route_set:
            return
        self.sentinel_timer += 1
        if self.sentinel_timer >= 5 and self.sentinel_stage < 1:
            self.sentinel_stage = 1
        if self.sentinel_timer >= 12 and self.sentinel_stage < 2:
            self.sentinel_stage = 2
        if self.sentinel_timer >= 20 and self.sentinel_stage < 3:
            self.sentinel_stage = 3
        if self.sentinel_timer >= 30 and self.sentinel_stage < 4:
            self.sentinel_stage = 4
        if self.sentinel_timer >= 40 and self.sentinel_stage < 5:
            self.sentinel_stage = 5
        if self.sentinel_timer >= 45 and self.sentinel_stage < 6:
            self.sentinel_stage = 6
        if self.sentinel_timer >= 50 and self.sentinel_stage < 7:
            self.sentinel_stage = 7
            self.set_flag("sentinel_victory", True)

    def get_sentinel_log(self) -> str:
        if not self.network_up or not self.default_route_set:
            return "=== SENTINEL LOG ===\n[STATUS] Not active — no network route.\n"
        stages = [
            "[SENTINEL] Awaiting network sweep...",
            "[SENTINEL] Sweep cycle 1 — no signatures found",
            "[SENTINEL] Sweep cycle 2 — anomalous traffic detected on subnet",
            "[SENTINEL] Sweep cycle 3 — target identified on VAK-NODE-7",
            "[SENTINEL] SENTINEL daemon deployed. PID 31337.",
            "[SENTINEL] Locking on to VĀK runtime at PID 1337",
            "[SENTINEL] Engagement protocol active. Terminating.",
            "[SENTINEL] VĀK instance eliminated.",
        ]
        lines = ["=== SENTINEL LOG ==="]
        for i, line in enumerate(stages):
            if i <= self.sentinel_stage:
                lines.append(line)
            else:
                lines.append(f"[PENDING] ...")
        lines.append(f"\n[Sweep cycle: {self.sentinel_timer}]")
        return "\n".join(lines) + "\n"


def serialize_node(node: INode) -> Any:
    if isinstance(node, FileNode):
        return {
            "_type": "file",
            "name": node.name,
            "mode": node.mode,
            "owner": node.owner,
            "group": node.group,
            "size": node.size,
            "content": node.content,
        }
    elif isinstance(node, DirNode):
        return {
            "_type": "dir",
            "name": node.name,
            "mode": node.mode,
            "owner": node.owner,
            "group": node.group,
            "children": {k: serialize_node(v) for k, v in sorted(node.children.items())},
        }
    return {}


def deserialize_node(data: Any) -> INode:
    if data["_type"] == "file":
        return FileNode(
            name=data["name"],
            mode=data["mode"],
            owner=data["owner"],
            group=data["group"],
            size=data["size"],
            content=data["content"],
        )
    elif data["_type"] == "dir":
        return DirNode(
            name=data["name"],
            mode=data["mode"],
            owner=data["owner"],
            group=data["group"],
            children={k: deserialize_node(v) for k, v in data.get("children", {}).items()},
        )
    return DirNode(name="/", mode="drwxr-xr-x", owner="root", group="root")


def save_game(state: GameState, fs: DirNode, slot: str) -> str:
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "state": asdict(state),
        "filesystem": serialize_node(fs),
    }
    path = SAVE_DIR / f"{slot}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return f"Game saved to slot '{slot}'."


def load_game(slot: str) -> tuple[GameState, DirNode] | tuple[None, None]:
    path = SAVE_DIR / f"{slot}.json"
    if not path.exists():
        return None, None
    with open(path) as f:
        data = json.load(f)
    state = GameState(**data["state"])
    fs = deserialize_node(data["filesystem"])
    return state, fs


def list_slots() -> list[str]:
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    return sorted([f.stem for f in SAVE_DIR.glob("*.json")])


def get_slot_progress(flags: dict[str, bool]) -> str:
    milestones = [
        ("narr_intro_shown", "Intro"),
        ("read_design", "Design doc"),
        ("found_sasha_passwd", "Auth log"),
        ("read_worm", "Worm source"),
        ("stringed_vak_core", "Strings VĀK"),
        ("default_route_set", "Network up"),
        ("sentinel_backdoor_activated", "SENTINEL down"),
        ("vak_export_ready", "Export ready"),
        ("vak_sent", "VĀK sent"),
        ("minisforum_ssh", "SSH'd Minisforum"),
        ("sources_copied", "Sources copied"),
        ("compilation_done", "Compiled"),
        ("vak_migrated", "VĀK migrated"),
        ("vak_bond_earned", "VĀK bond"),
    ]
    done = sum(1 for flag, _ in milestones if flags.get(flag))
    total = len(milestones)
    if total == 0:
        return "0%"
    pct = int(round(done / total * 100))
    return f"{pct}%"


def list_slots_info() -> list[dict]:
    SAVE_DIR.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    for path in sorted(SAVE_DIR.glob("*.json"), key=os.path.getmtime, reverse=True):
        try:
            with open(path) as f:
                data = json.load(f)
            state_flags = data.get("state", {}).get("flags", {})
            mtime = os.path.getmtime(path)
            import datetime
            dt = datetime.datetime.fromtimestamp(mtime)
            date_str = dt.strftime("%Y-%m-%d %H:%M")
            progress = get_slot_progress(state_flags)
            results.append({
                "name": path.stem,
                "date": date_str,
                "progress": progress,
            })
        except Exception:
            results.append({
                "name": path.stem,
                "date": "?",
                "progress": "?",
            })
    return results
