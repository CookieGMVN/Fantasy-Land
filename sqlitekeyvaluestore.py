import sqlite3

class KeyValueStore(dict):
    def __init__(self, filename=None):
        self.conn = sqlite3.connect(filename)
        self.conn.execute("CREATE TABLE IF NOT EXISTS db (key text unique, value text)")

    def close(self):
        self.conn.commit()
        self.conn.close()

    def __len__(self):
        rows = self.conn.execute('SELECT COUNT(*) FROM kv').fetchone()[0]
        return rows if rows is not None else 0

    def iterkeys(self):
        c = self.conn.cursor()
        for row in self.conn.execute('SELECT key FROM db'):
            yield row[0]

    def itervalues(self):
        c = self.conn.cursor()
        for row in c.execute('SELECT value FROM db'):
            yield row[0]

    def iteritems(self):
        c = self.conn.cursor()
        for row in c.execute('SELECT key, value FROM db'):
            yield row[0], row[1]

    def keys(self):
        return list(self.iterkeys())

    def values(self):
        return list(self.itervalues())

    def items(self):
        return list(self.iteritems())

    def __contains__(self, key):
        return self.conn.execute('SELECT 1 FROM db WHERE key = ?', (key,)).fetchone() is not None

    def __getitem__(self, key):
        item = self.conn.execute('SELECT value FROM db WHERE key = ?', (key,)).fetchone()
        if item is None:
            raise KeyError(key)
        return item[0]

    def __setitem__(self, key, value):
        self.conn.execute('REPLACE INTO db (key, value) VALUES (?,?)', (key, value))

    def __delitem__(self, key):
        if key not in self:
            raise KeyError(key)
        self.conn.execute('DELETE FROM db WHERE key = ?', (key,))

    def __iter__(self):
        return self.iterkeys()