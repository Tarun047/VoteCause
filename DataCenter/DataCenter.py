""" The DataCenter module uses sqlite3 for storage of Data By default."""
import sqlite3
conn = sqlite3.connect("Poll.db")
def checkState():
    """
    Function Name: checkState.

    Function Use: Rectify Integerity of the DataBase.
    """
    try:
        c = conn.cursor()
        c.execute("SELECT * from POLL_TAB")
    except:
        c = conn.cursor()
        c.execute("CREATE TABLE POLL_TAB(id INTEGER PRIMARY KEY AUTOINCREMENT,poll_id TEXT,poll_data TEXT)")
    try:
        c = conn.cursor()
        c.execute("SELECT * from POLL_STATS")
    except:
        c = conn.cursor()
        c.execute("CREATE TABLE POLL_STATS(id INTEGER PRIMARY KEY AUTOINCREMENT,poll_id TEXT,poll_addr TEXT,prev_stats TEXT)")



def writeStats(poll_id,poll_addr,stats):
    c = conn.cursor()
    c.execute("INSERT INTO POLL_STATS(poll_id,poll_addr,prev_stats) VALUES(?,?,?)",(poll_id,poll_addr,stats))
    conn.commit()

def updateStats(poll_id,stats):
    c = conn.cursor()
    c.execute("UPDATE POLL_STATS SET prev_stats = ? WHERE poll_id = ?",(stats,poll_id))
    conn.commit()

def readStats(poll_id):
    c = conn.cursor()
    data = c.execute("SELECT prev_stats from POLL_STATS WHERE poll_id=?",(poll_id,)).fetchone()
    return data

def removeStats(poll_id):
    c = conn.cursor()
    c.execute("DELETE FROM POLL_STATS WHERE poll_id=?",(poll_id,))
    conn.commit()

def read(poll_id):
    c = conn.cursor()
    data = c.execute("SELECT * FROM POLL_TAB WHERE poll_id=?",(poll_id,)).fetchall()
    return data

def readAll():
    """
    Function Name: readAll.

    Function use: To Retrieve all the relavant Interns details.
    """

    c = conn.cursor()
    data =  c.execute("SELECT poll_id,poll_data FROM POLL_TAB").fetchall()
    conn.commit()

    return data


def write(poll_id,poll_data):
    """
    Function Name: write.

    Function Use: writes the Intern's Data to the DataBase.
    """
    c = conn.cursor()
    c.execute("INSERT INTO POLL_TAB(poll_id,poll_data) VALUES(?,?)",(poll_id,poll_data))

    conn.commit()

def delete(poll_id):
    """
    Function Name: delete.

    Function Use: Removes Intern data from the DataBase.
    """
    c = conn.cursor()
    c.execute("DELETE FROM POLL_TAB WHERE poll_id=?",(poll_id,))
    conn.commit()
