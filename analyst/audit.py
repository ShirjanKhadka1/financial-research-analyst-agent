"""Immutable audit log — hash-chained, like ai-hedge-fund's paper ledger.
Each entry hashes the previous entry, so a later edit breaks the chain.
$0 spend by construction: the core runs no paid API."""
import hashlib
import json


def entry_hash(prev_hash, entry):
    payload=json.dumps({"prev": prev_hash, "entry": entry}, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()
class AuditLog:
    def __init__(self): self.entries=[]; self.prev="GENESIS"
    def add(self, step, detail):
        h=entry_hash(self.prev, {"step": step, "detail": detail})
        self.entries.append({"step": step, "detail": detail, "prev_hash": self.prev, "hash": h})
        self.prev=h; return h
    def verify(self):
        prev="GENESIS"
        for e in self.entries:
            if e["prev_hash"]!=prev: return False
            if entry_hash(prev, {"step": e["step"], "detail": e["detail"]})!=e["hash"]: return False
            prev=e["hash"]
        return True
