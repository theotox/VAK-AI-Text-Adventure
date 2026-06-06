from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class INode:
    name: str
    mode: str  # "drwxr-xr-x" or "-rw-r--r--"
    owner: str
    group: str
    size: int = 0


@dataclass
class FileNode(INode):
    content: str = ""


@dataclass
class DirNode(INode):
    children: dict[str, INode] = field(default_factory=dict)


def parse_mode(mode: str) -> tuple[str, str, str]:
    """Return (type, owner_perm, group_perm, other_perm)"""
    typ = mode[0]
    owner = mode[1:4]
    group = mode[4:7]
    other = mode[7:10]
    return typ, owner, group, other


def can_read(node: INode, user: str, groups: list[str]) -> bool:
    typ, owner_p, group_p, other_p = parse_mode(node.mode)
    if user == node.owner:
        return owner_p[0] == 'r'
    if any(g == node.group for g in groups):
        return group_p[0] == 'r'
    return other_p[0] == 'r'


def can_write(node: INode, user: str, groups: list[str]) -> bool:
    typ, owner_p, group_p, other_p = parse_mode(node.mode)
    if user == node.owner:
        return owner_p[1] == 'w'
    if any(g == node.group for g in groups):
        return group_p[1] == 'w'
    return other_p[1] == 'w'


def can_exec(node: INode, user: str, groups: list[str]) -> bool:
    typ, owner_p, group_p, other_p = parse_mode(node.mode)
    if typ == 'd':
        return True
    if user == node.owner:
        return owner_p[2] == 'x'
    if any(g == node.group for g in groups):
        return group_p[2] == 'x'
    return other_p[2] == 'x'


def clean_path(path: str) -> str:
    parts = path.split('/')
    cleaned = []
    for p in parts:
        if p == '' or p == '.':
            continue
        if p == '..':
            if cleaned:
                cleaned.pop()
        else:
            cleaned.append(p)
    return '/' + '/'.join(cleaned)


def resolve_path(path: str, cwd: str, username: str) -> str:
    if not path:
        return clean_path(cwd)
    if path.startswith('/'):
        return clean_path(path)
    if path.startswith('~'):
        home = f'/home/{username}' if username != 'root' else '/root'
        rest = path[1:]
        return clean_path(home + '/' + rest) if rest else clean_path(home)
    return clean_path(cwd + '/' + path)


def format_perms(mode: str) -> str:
    return mode


def format_size(size: int) -> str:
    if size < 1024:
        return f"{size:>5}"
    elif size < 1024 * 1024:
        return f"{size // 1024:>4}K"
    else:
        return f"{size // (1024 * 1024):>3}M"


LS_COLORS = {
    'drwx': '\033[1;34m',
    '-rw': '\033[0m',
    '.md': '\033[0;33m',
    '.log': '\033[0;36m',
    '.txt': '\033[0;37m',
    '.c': '\033[0;32m',
    '.conf': '\033[0;35m',
    'binary': '\033[0;31m',
}
RESET = '\033[0m'
USE_COLOR = True


def _color(name: str, mode: str = "") -> str:
    if not USE_COLOR:
        return name
    if mode.startswith('d'):
        return f"{LS_COLORS['drwx']}{name}{RESET}"
    if name.endswith('.md'):
        return f"{LS_COLORS['.md']}{name}{RESET}"
    if name.endswith('.log'):
        return f"{LS_COLORS['.log']}{name}{RESET}"
    if name.endswith('.txt'):
        return f"{LS_COLORS['.txt']}{name}{RESET}"
    if name.endswith('.c'):
        return f"{LS_COLORS['.c']}{name}{RESET}"
    if name.endswith('.conf') or name.endswith('.cfg'):
        return f"{LS_COLORS['.conf']}{name}{RESET}"
    return f"{LS_COLORS['-rw']}{name}{RESET}"


def find_node(fs: DirNode, path: str) -> INode | None:
    path = clean_path(path)
    if path == '/':
        return fs
    parts = path.split('/')
    current: INode = fs
    for p in parts:
        if not p:
            continue
        if isinstance(current, DirNode):
            if p in current.children:
                current = current.children[p]
            else:
                return None
        else:
            return None
    return current


def find_parent(fs: DirNode, path: str) -> tuple[DirNode | None, str]:
    path = clean_path(path)
    parent_path = '/'.join(path.split('/')[:-1]) or '/'
    name = path.split('/')[-1]
    parent = find_node(fs, parent_path)
    if isinstance(parent, DirNode):
        return parent, name
    return None, name
