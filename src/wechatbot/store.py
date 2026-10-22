"""Single-owner local SQLite ledger. Persist intent before each side effect."""
import json
import sqlite3
from .config import local_path


def key(parts):
    return json.dumps(parts, ensure_ascii=False, separators=(',', ':'))


class Store:
    def __init__(self, root, history_turns=8):
        path = local_path(root, 'state/wechat.sqlite3')
        path.parent.mkdir(parents=True, exist_ok=True)
        self.owner = local_path(root, 'state/core-owner.lock').open('a+b')
        self.owner.write(b'0'); self.owner.flush(); self.owner.seek(0)
        try:
            if __import__('os').name == 'nt':
                import msvcrt
                msvcrt.locking(self.owner.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.owner, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            self.owner.close()
            raise ValueError('owner_exists') from None
        try:
            self.db = sqlite3.connect(path)
            self.db.execute('PRAGMA synchronous=FULL')
            self.db.executescript('''
                CREATE TABLE IF NOT EXISTS seen (id TEXT PRIMARY KEY);
                CREATE TABLE IF NOT EXISTS attempts (
                    id TEXT PRIMARY KEY, target TEXT NOT NULL, state TEXT NOT NULL,
                    phase TEXT NOT NULL, ack TEXT NOT NULL DEFAULT 'none');
                CREATE TABLE IF NOT EXISTS history (
                    seq INTEGER PRIMARY KEY, scope TEXT NOT NULL, user TEXT NOT NULL, assistant TEXT NOT NULL);
            ''')
            # A crash may have occurred before or after an external side effect.
            # Recover intent only, never replay an inbound event or generation.
            with self.db:
                self.db.execute("UPDATE attempts SET state='unknown' WHERE state IN ('prepared','submitted')")
            self.turns = history_turns
        except BaseException:
            self.owner.close()
            raise

    def claim(self, event):
        if self.db.execute('SELECT COUNT(*) FROM seen').fetchone()[0] >= 100000:
            raise ValueError('seen_capacity')
        parts = event.target + (event.source_message_id,)
        if event.id_scope == 'process_local':
            parts += (event.adapter_epoch,)
        with self.db:
            result = self.db.execute('INSERT OR IGNORE INTO seen VALUES (?)', (key(parts),))
        return result.rowcount == 1

    def blocked(self, target):
        return bool(self.db.execute("SELECT 1 FROM attempts WHERE target=? AND state IN ('unknown','prepared','submitted') LIMIT 1", (key(target),)).fetchone())

    def uncertain(self, target):
        return bool(self.db.execute("SELECT 1 FROM attempts WHERE target=? AND state='unknown' LIMIT 1", (key(target),)).fetchone())

    def prepare(self, trace, target):
        if self.db.execute('SELECT COUNT(*) FROM attempts').fetchone()[0] >= 10000:
            raise ValueError('attempt_capacity')
        if self.db.execute('SELECT COUNT(DISTINCT scope) FROM history').fetchone()[0] >= 256:
            raise ValueError('history_scope_capacity')
        if self.blocked(target):
            raise ValueError('target_blocked')
        with self.db:
            self.db.execute("INSERT INTO attempts(id,target,state,phase) VALUES (?,?,'prepared','model')", (trace, key(target)))

    def transition(self, trace, state, phase, ack='none'):
        row = self.record(trace)
        valid = {'prepared': {'prepared', 'submitted', 'failed', 'unknown'},
                 'submitted': {'accepted', 'failed', 'unknown'}}
        if state not in valid.get(row['state'], set()):
            raise ValueError('delivery_transition')
        with self.db:
            self.db.execute('UPDATE attempts SET state=?,phase=?,ack=? WHERE id=?', (state, phase, ack, trace))

    def accept(self, trace, event, reply, ack):
        if self.record(trace)['state'] != 'submitted' or ack not in ('api_accepted', 'ui_observed'):
            raise ValueError('delivery_transition')
        with self.db:
            self.db.execute("UPDATE attempts SET state='accepted',phase='delivery',ack=? WHERE id=?", (ack, trace))
            self.db.execute('INSERT INTO history(scope,user,assistant) VALUES (?,?,?)', (key(event.history_key), event.text, reply))
            self.db.execute('DELETE FROM history WHERE scope=? AND seq NOT IN (SELECT seq FROM history WHERE scope=? ORDER BY seq DESC LIMIT ?)', (key(event.history_key), key(event.history_key), self.turns))

    def history(self, event):
        rows = self.db.execute('SELECT user,assistant FROM history WHERE scope=? ORDER BY seq', (key(event.history_key),)).fetchall()
        return [dict(role=role, content=text) for row in rows for role, text in zip(('user', 'assistant'), row)]

    def record(self, trace):
        row = self.db.execute('SELECT state,phase,ack FROM attempts WHERE id=?', (trace,)).fetchone()
        return dict(zip(('state', 'phase', 'ack'), row)) if row else None

    def counts(self):
        return {name: self.db.execute(f'SELECT COUNT(*) FROM {name}').fetchone()[0] for name in ('seen', 'attempts', 'history')}

    def close(self):
        self.db.close()
        self.owner.close()
