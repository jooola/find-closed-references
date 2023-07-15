from dataclasses import dataclass
from typing import Optional


@dataclass
class Ref:
    file: str
    line: int

    host: str
    owner: str
    repo: str
    ref_type: str
    ref_id: int
    ignore: Optional[bool] = None

    closed: Optional[bool] = None

    def __init__(
        self,
        file: str,
        line: int,
        host: str,
        owner: str,
        repo: str,
        ref_type: str,
        ref_id: str,
        ignore: Optional[str] = None,
    ) -> None:
        self.file = str(file)
        self.line = line
        self.host = host
        self.owner = owner
        self.repo = repo
        self.ref_type = ref_type
        self.ref_id = int(ref_id)
        self.ignore = bool(ignore)
