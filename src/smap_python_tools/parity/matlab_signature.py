from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass
class MatlabSignature:
    """Represents a MATLAB function signature."""

    name: str
    outputs: List[str]
    inputs: List[str]
    comments: List[str]


_DEF_RE = re.compile(
    r"^function\s+(?:\[(?P<outs>[^\]]*)\]|(?P<out>[^=\s]+))\s*=\s*(?P<name>\w+)\s*\((?P<ins>[^)]*)\)",
    re.IGNORECASE,
)
_NOOUT_RE = re.compile(
    r"^function\s+(?P<name>\w+)\s*\((?P<ins>[^)]*)\)",
    re.IGNORECASE,
)


def parse_matlab_signature(source: str) -> MatlabSignature:
    """Parse a MATLAB function signature and leading comments from ``source``.

    Parameters
    ----------
    source:
        Text of a MATLAB ``.m`` file.
    """

    lines = source.splitlines()
    comments: List[str] = []
    i = 0
    while i < len(lines) and lines[i].lstrip().startswith("%"):
        comments.append(lines[i].lstrip()[1:].strip())
        i += 1

    func_line = ""
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("function"):
            func_line = line
            break
        i += 1

    outputs: List[str] = []
    inputs: List[str] = []
    name = ""

    m = _DEF_RE.match(func_line)
    if m:
        outs = m.group("outs") or m.group("out") or ""
        name = m.group("name")
        ins = m.group("ins") or ""
        outputs = [o.strip() for o in outs.split(",") if o.strip()]
        inputs = [p.strip() for p in ins.split(",") if p.strip()]
    else:
        m = _NOOUT_RE.match(func_line)
        if m:
            name = m.group("name")
            ins = m.group("ins") or ""
            inputs = [p.strip() for p in ins.split(",") if p.strip()]

    return MatlabSignature(name=name, outputs=outputs, inputs=inputs, comments=comments)
