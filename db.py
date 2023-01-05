import mysql.connector
from datetime import datetime
import cr

hostname = cr.hostname
un = cr.un
password = cr.password
database = cr.database

def get_users():
    conn = mysql.connector.connect( host=hostname, user=un, passwd=password, db=database )
    cur = conn.cursor()
    cur.execute( """SELECT email, password, uid FROM users ORDER BY uid DESC""" )
    data = cur.fetchall()
    conn.close()
    return data


def submit_post(slug, title, body, image_path, emgithub, youtube, p_type, keywords):
    author = 'Miles Catlett'
    created_on = datetime.today()
    pid = get_post_ids()
    conn = mysql.connector.connect( host=hostname, user=un, passwd=password, db=database )
    cur = conn.cursor()
    stmt = ("INSERT INTO posts (pid, slug, author, title, body, image_path, emgithub, youtube, type, created_on, keywords) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    data = (pid, slug, author, title, body, image_path, emgithub, youtube, p_type, created_on, keywords)
    cur.execute(stmt, data)
    conn.commit()
    conn.close()
    
    
def update_post(slug, title, body, image_path, emgithub, youtube, p_type, keywords):
    conn = mysql.connector.connect( host=hostname, user=un, passwd=password, db=database )
    cur = conn.cursor()
    stmt = ("UPDATE posts SET title = %s, body = %s, image_path = %s, emgithub = %s, youtube = %s, type = %s, keywords = %s WHERE slug = %s")
    data = (title, body, image_path, emgithub, youtube, p_type, keywords, slug)
    cur.execute(stmt, data)
    conn.commit()
    conn.close()
    
    
def add_user(name, email, pword):
    uid = get_user_ids()
    registered_on = datetime.today()
    uname = name.replace(" ", "_") + str(uid)
    conn = mysql.connector.connect( host=hostname, user=un, passwd=password, db=database )
    cur = conn.cursor()
    stmt = ("""INSERT INTO users (uid, name, uname, email, password, registered_on) VALUES (%s, %s, %s, %s, %s, %s)""")
    data = (uid, name, uname, email, pword, registered_on)
    cur.execute(stmt, data)
    conn.commit()
    conn.close()
    return data[1]
    
    
def get_post_ids():
    conn = mysql.connector.connect( host=hostname, user=un, passwd=password, db=database )
    cur = conn.cursor()
    cur.execute( """SELECT pid FROM posts ORDER BY pid DESC""" )
    data = cur.fetchall()
    conn.close()
    if data == []:
        return 1
    else:
        return int(data[0][0]) + 1
        
def get_user_ids():
    conn = mysql.connector.connect( host=hostname, user=un, passwd=password, db=database )
    cur = conn.cursor()
    cur.execute( """SELECT uid FROM users ORDER BY uid DESC""" )
    data = cur.fetchall()
    conn.close()
    if data == []:
        return 1
    else:
        return int(data[0][0]) + 1

        
def get_portfolio():
    conn = mysql.connector.connect( host=hostname, user=un, passwd=password, db=database )
    cur = conn.cursor()
    cur.execute( """SELECT * FROM posts WHERE type = 'portfolio'""" )
    data = cur.fetchall()
    conn.close()
    return data
    
    
def get_article():
    conn = mysql.connector.connect( host=hostname, user=un, passwd=password, db=database )
    cur = conn.cursor()
    cur.execute( """SELECT * FROM posts WHERE type = 'blog'""" )
    data = cur.fetchall()
    conn.close()
    return data
    
    
def get_all():
    conn = mysql.connector.connect( host=hostname, user=un, passwd=password, db=database )
    cur = conn.cursor()
    cur.execute( """SELECT * FROM posts""" )
    data = cur.fetchall()
    conn.close()
    return data
    
    
def get_article_by_slug(slug):
    conn = mysql.connector.connect( host=hostname, user=un, passwd=password, db=database )
    cur = conn.cursor()
    query = """SELECT * FROM posts WHERE slug = %s"""
    cur.execute( query, (slug,) )
    data = cur.fetchall()
    conn.close()
    return data
    
    
def get_article_by_pid(pid):
    conn = mysql.connector.connect( host=hostname, user=un, passwd=password, db=database )
    cur = conn.cursor()
    query = """SELECT * FROM posts WHERE pid = %s"""
    cur.execute( query, (pid,) )
    data = cur.fetchall()
    conn.close()
    return data
        

def check_slug(title):
    pid = get_post_ids()
    title = title.lower()
    slug = title.replace(" ", "-")
    conn = mysql.connector.connect( host=hostname, user=un, passwd=password, db=database )
    cur = conn.cursor()
    cur.execute( """SELECT slug FROM posts""" )
    data = cur.fetchall()
    conn.close()
    length = len(data[0])
    counter = 0
    for s in data[0]:
        if s != slug:
            counter += 1
        if s == slug:
            return slug + '-' + str(pid)
    if counter == length:
        return slug
    
    