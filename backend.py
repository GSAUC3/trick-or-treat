import sqlite3 as sq

x='HighScore.db'

def connect():
    conn=sq.connect(x)
    c=conn.cursor()
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS scoreboard (
            score INTERGER NOT NULL
        )
        '''
    )
    conn.commit()
    conn.close()

def insert(score):
    conn=sq.connect(x)
    c=conn.cursor()
    c.execute('''INSERT INTO scoreboard VALUES (?)''',(score,))
    conn.commit()
    conn.close()

def updatescore(score):
    if get_score()<score:
        conn=sq.connect(x)
        c=conn.cursor()
        
        
        c.execute('''
            UPDATE scoreboard SET score=?
        ''',(score,))
        conn.commit()
        conn.close()

def get_score():
    conn=sq.connect(x)
    c=conn.cursor()
    c.execute(
        """
        select * from scoreboard
        """
    )
    ans=c.fetchone()
    conn.commit()
    conn.close()
    return ans[0]

def droptable():
    conn=sq.connect(x)
    c=conn.cursor()
    c.execute(
        """
    DROP TABLE scoreboard
        """
    )
    conn.commit()
    conn.close()
  
    

connect()
