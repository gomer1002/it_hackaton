#

if __name__ == "__main__":
    import sqlite3 as sl
    from json import loads

    conf = loads(open("config.json", "r").read())

    conn = sl.connect(conf.get("SQLITE_DATABASE_PATH"))
    conn.row_factory = sl.Row

    uid = "2f06a952-7d41-4f22-97ec-3ea696040589"
    cur = conn.cursor()
    query = "DELETE FROM users"
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
