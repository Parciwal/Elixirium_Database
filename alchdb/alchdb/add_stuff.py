import sqlite3
from alchdb import modify
import pathlib
id = 10

# An itereator that repeatedly returns the intiially given id
class Id_iterator():
    def __init__(self,id):
        self.id = id
    
    def __iter__(self):
        return self

    def __next__(self):
        return self.id

def add_elements(item_name:str,effect_names:list[str],effect_strengths:list[int],affix_name:str,affix_strength:int,override):
    try:
        with sqlite3.connect(pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db')) as conn: #path of curent file, path of working directory is inconsistent
            # add  a item
            cur = conn.cursor()

            # duplicate check
            cur.execute(f"SELECT items_id FROM items WHERE items_name='{item_name}' ")
            rows = cur.fetchone()
            if rows:
                if not override:
                    raise AssertionError(f"{item_name} already exists")
                modify.modify_item(item_name,".*",0,0,".*",True)
            
            item_id = add_item(conn, item_name)
            item_id_iter = Id_iterator(item_id)

            print(f'Created a item with the id {item_id}')
            print()

            # add effects to the item, zip makes the needed tuples
            for effect in zip(item_id_iter,effect_names,effect_strengths):
                add_item_effect(conn, effect)

            # add affix to the item
            if (affix_name) and (affix_strength):
                add_item_affix(conn, (item_id,affix_name, affix_strength))

            elif (affix_name) or (affix_strength):
                print("affix invalid")

            #onl commit to avoid half baked items
            conn.commit()
    except sqlite3.Error as e:
        print(e)

def add_item(conn, item):
    # insert table statement
    sql = ''' INSERT INTO items(items_name)
              VALUES(?) '''
    
    # Create  a cursor
    cur = conn.cursor()
    # execute the INSERT statement
    cur.execute(sql, [item])

    # get the id of the last inserted row
    return cur.lastrowid

def add_item_effect(conn,effect):
    cur = conn.cursor()

    # get effect id for later
    sql_get = """SELECT effects.effect_id
                FROM effects
                WHERE effects.effect_name LIKE ? COLLATE NOCASE"""

    cur.execute(sql_get,[effect[1]])
    effect_id = cur.fetchall()

    # check if given name actually only fits one effect
    if len(effect_id) > 1:
        raise LookupError(f"effect name {effect[1]} not specific enough, item creation aborted")
    
    #make new conenction betwwen item and effect
    sql_add = '''INSERT INTO item_effect(item_id,effect_id,effect_strength)
             VALUES(?,?,?)'''
    if effect_id:
        print(f"adding item effect with {effect[0],effect_id[0][0],effect[2]}")
        cur.execute(sql_add,(effect[0],effect_id[0][0],effect[2]))
    else:
        print(f"No effect named {effect[1]}")
    

def add_effect(conn, effect:tuple[str,str]):
    """
    tuple of item id, effect name, effect id as input
    """
    # insert table statement
    sql = '''INSERT INTO effects(effect_name,category)
             VALUES(?,?) '''
    
    # create a cursor
    cur = conn.cursor()

    # execute the INSERT statement
    cur.execute(sql, effect)
    
    print(f"added effect with id {cur.lastrowid}")
    # get the id of the last inserted row
    return cur.lastrowid

def add_item_affix(conn,affix):
    cur = conn.cursor()
    
    sql_get = """SELECT affix.affix_id
                FROM affix
                WHERE affix.affix_name LIKE ? COLLATE NOCASE"""

    affix_id = cur.execute(sql_get,[affix[1]])
    affix_id = cur.fetchall()
    
    # only match one affix
    if len(affix_id) > 1:
        raise LookupError(f"affix name {affix[1]} not specific enough, item creation aborted")
    
    #check if affix id exists
    if not affix_id:
        # avoid adding false affix
        if not "%" in affix[1]:
            affix_id = [[add_affix(conn,affix[1])]]
        else:
            raise ValueError(f"looked up affix name not found, please create with full affix name")
    print(f"adding item affix with {affix[0],affix_id[0][0],affix[2]}")

    sql_add = '''INSERT INTO item_affix(item_id,affix_id,affix_strength)
             VALUES(?,?,?)'''
    cur.execute(sql_add,(affix[0],affix_id[0][0],affix[2]))

def add_affix(conn, affix_name:str):
    # insert table statement
    sql = '''INSERT INTO affix(affix_name)
             VALUES(?) '''
    
    # create a cursor
    cur = conn.cursor()

    # execute the INSERT statement
    cur.execute(sql,[affix_name])

    # commit the changes
    
    print(f'Created affix with the id {cur.lastrowid}')
    # get the id of the last inserted row
    return cur.lastrowid
