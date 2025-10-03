import sqlite3
from alchdb import add_stuff
import pathlib

def modify_item(item_name,effect_name,item_strength,affix_strength,new_name,delete):
    try:
        with sqlite3.connect(pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db')) as conn:
            cur = conn.cursor()
            if delete and effect_name != ".*": #delete effect from item
                sql = f"""
                    SELECT item_effect.item_id,item_effect.effect_id 
                    FROM (item_effect
                        JOIN items ON items.items_id = item_effect.item_id)
                        JOIN effects ON effects.effect_id = item_effect.effect_id 
                    WHERE items.items_name = ?
                    AND effects.effect_name = ?;
                """
                cur.execute(sql,[item_name,effect_name])
                rows = cur.fetchall()
                for row in rows:
                    sql = f"""
                    DELETE FROM item_effect
                    WHERE item_id = ?
                    AND effect_id = ?;
                    """
                    cur.execute(sql,row)
                
                # feedback is important
                print(f"{cur.rowcount} rows affected")
                conn.commit()
                return
            if delete: #delete item with all effects and affixes
                sql = f"""
                    SELECT item_effect.item_id
                    FROM item_effect
                        JOIN items ON items.items_id = item_effect.item_id
                    WHERE items.items_name = ?;
                """
                cur.execute(sql,[item_name])
                rows = cur.fetchall()
                for row in rows:
                    print(row)
                    sql = f"""
                        DELETE FROM item_effect
                        WHERE item_id = ?;
                        """
                    cur.execute(sql,row)
                
                # feedback is important
                print(f"{cur.rowcount} rows affected")
                conn.commit()
                for row in rows:
                    sql = f"""
                        DELETE FROM item_affix
                        WHERE item_id = ?;
                        """
                    cur.execute(sql,row)
                sql = f"""
                    DELETE FROM items
                    WHERE items_name = ?;
                    """
                cur.execute(sql,[item_name])
                conn.commit()
                return
            if new_name != "": #rename
                sql = f"""
                SELECT items.items_id
                FROM items
                WHERE items_name = ?;
                """
                cur.execute(sql,[new_name])
                exist = cur.fetchall()
                if exist:
                    raise ValueError(f"{new_name} already exists")

                sql = f"""
                UPDATE items
                SET items_name = ?
                WHERE items_name = ?;
                """
                cur.execute(sql,[new_name,item_name])
                
                # feedback is important
                print(f"{cur.rowcount} rows affected")
                conn.commit()
                return
            
            # if none of the above: add effect or affix
            cur.execute(f"SELECT items_id FROM items WHERE items_name='{item_name}' ")
            rows = cur.fetchall()
            for row in rows:
                if item_strength:
                    add_stuff.add_item_effect(conn,(row[0],effect_name,item_strength))
                else:
                    add_stuff.add_item_affix(conn,(row[0],effect_name,affix_strength))
            conn.commit()
    except sqlite3.Error as e:
        print(e)