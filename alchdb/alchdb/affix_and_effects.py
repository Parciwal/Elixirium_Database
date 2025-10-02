from alchdb import add_stuff
import sqlite3
import pathlib

def del_effect(name):
    try:
        with sqlite3.connect(pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db')) as conn: #path of curent file, path of working directory is inconsistent
            cur = conn.cursor()
            sql = f"""
            DELETE FROM effects
            WHERE effect_name = ?;
            """
            cur.execute(sql,[name])

            # feedback is important
            print(f"{cur.rowcount} rows affected")
            conn.commit()
    except sqlite3.Error as e:
        print(e)

def change_or_add_effect(name,category):
    try:
        with sqlite3.connect(pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db')) as conn: #path of curent file, path of working directory is inconsistent
            cur = conn.cursor()
            sql = f"""
            SELECT effect_id FROM effects
            WHERE effect_name = ?;
            """
            cur.execute(sql,[name])
            row = cur.fetchone()

            # checks if efect exists, if not, adds it
            if row:
                update_effect(cur,row[0],category)
            else:
                add_stuff.add_effect(conn,(name,category))
            conn.commit()
    except sqlite3.Error as e:
        print(e)

def update_effect(cur,id,category):
    sql = f"""
            UPDATE effects
            SET category = ?
            WHERE effect_name = ?;
            """
    cur.execute(sql,[id,category])

    # feedback is important
    print(f"{cur.rowcount} rows affected")

def del_affix(name):
    try:
        with sqlite3.connect(pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db')) as conn: #path of curent file, path of working directory is inconsistent
            cur = conn.cursor()
            sql = f"""
            DELETE FROM affix
            WHERE affix_name = ?;
            """
            cur.execute(sql,[name])

            # feedback is important
            print(f"{cur.rowcount} rows affected")
            conn.commit()
    except sqlite3.Error as e:
        print(e)

def rename_effect(name,new_name):
    try:
        with sqlite3.connect(pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db')) as conn: #path of curent file, path of working directory is inconsistent
            cur = conn.cursor()
            
            sql = f"""
                UPDATE effects
                SET effect_name = ?
                WHERE effect_name = ?;
                """
            cur.execute(sql,[new_name,name])

            # feedback is important
            print(f"{cur.rowcount} rows affected")
            conn.commit()
    except sqlite3.Error as e:
        print(e)

