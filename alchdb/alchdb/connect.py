import sqlite3
from alchdb import add_stuff
import pathlib

sql_statements = [
"""CREATE TABLE IF NOT EXISTS items (
    items_id INTEGER PRIMARY KEY, 
    items_name text NOT NULL
);""",

"""CREATE TABLE IF NOT EXISTS item_effect (
    item_id INT NOT NULL,
    effect_id INT NOT NULL,
    effect_strength INT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items(items_id)
    FOREIGN KEY (effect_id) REFERENCES effects(effect_id)
);""",

"""CREATE TABLE IF NOT EXISTS item_affix (
    item_id INT NOT NULL,
    affix_id INT NOT NULL,
    affix_strength INT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items(items_id)
    FOREIGN KEY (affix_id) REFERENCES affix(affix_id)
);""",

"""CREATE TABLE IF NOT EXISTS effects (
    effect_id INTEGER PRIMARY KEY,
    effect_name text NOT NULL, 
    category text
);""",

"""CREATE TABLE IF NOT EXISTS affix(
    affix_id INTEGER PRIMARY KEY, 
    affix_name text NOT NULL
);"""
]

def create_tables():
    try:
        with sqlite3.connect(pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db')) as conn:
            print(f"Opened database at {pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db')}")
            cursor = conn.cursor()
            for statement in sql_statements:
                cursor.execute(statement)
            conn.commit()
            print("Tables created successfully.")
    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)

def import_effects():
    try:
        with sqlite3.connect(pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db')) as conn:
            add_stuff.add_effect(conn,("Absorbtion","pos"))
            add_stuff.add_effect(conn,("Blindness","neg"))
            add_stuff.add_effect(conn,("Fire_Resistance","pos"))
            add_stuff.add_effect(conn,("Glowing","neut"))
            add_stuff.add_effect(conn,("Grow","neut"))
            add_stuff.add_effect(conn,("Shrink","neut"))
            add_stuff.add_effect(conn,("Health_Boost","pos"))
            add_stuff.add_effect(conn,("Hunger","neg"))
            add_stuff.add_effect(conn,("Instant_Damage","neg"))
            add_stuff.add_effect(conn,("Instant_Health","pos"))
            add_stuff.add_effect(conn,("Invisibility","neut"))
            add_stuff.add_effect(conn,("Jump_Boost","neut"))
            add_stuff.add_effect(conn,("Levitation","neg"))
            add_stuff.add_effect(conn,("Luck","pos"))
            add_stuff.add_effect(conn,("Mining_Fatigue","neg"))
            add_stuff.add_effect(conn,("Nausea","neut"))
            add_stuff.add_effect(conn,("Night_Vision","pos"))
            add_stuff.add_effect(conn,("Poison","neg"))
            add_stuff.add_effect(conn,("Regeneration","pos"))
            add_stuff.add_effect(conn,("Resistance","pos"))
            add_stuff.add_effect(conn,("Saturation","pos"))
            add_stuff.add_effect(conn,("Haste","pos"))
            add_stuff.add_effect(conn,("Slow_Falling","pos"))
            add_stuff.add_effect(conn,("Slowness","neg"))
            add_stuff.add_effect(conn,("Speed","pos"))
            add_stuff.add_effect(conn,("Strength","pos"))
            add_stuff.add_effect(conn,("Bad_Luck","neut"))
            add_stuff.add_effect(conn,("Water_Breathing","pos"))
            add_stuff.add_effect(conn,("Weakness","neg"))
            add_stuff.add_effect(conn,("Wither","neg"))
            print("effects succesfully added")
            conn.commit()
    except sqlite3.Error as e:
        print(e)

def insert_test_vals():
    add_stuff.add_elements("kohle",["Regeneration","Luck"],[12,8],None,None,False)
    add_stuff.add_elements("eisen",["Nausea","Invisibility"],[5,15],None,None,False)
    add_stuff.add_elements("gold",["Instant_Damage","Shrink"],[10,1],None,None,False)
    add_stuff.add_elements("bowl",["Regeneration","grow"],[5,8],"stärkeres nächstes",11,False)
    add_stuff.add_elements("eichenholzknopf",["Haste","Levitation"],[9,3],None,None,False)
    add_stuff.add_elements("schwert",["Weakness","Nausea","Instant_Health"],[3,17,9],"schwächere negative",6,False)
    print("test values succesfully added")
