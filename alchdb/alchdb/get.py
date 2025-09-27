import sqlite3
from typing import Any
import re
import pathlib

def get_stuff(sorting,inverted,effect:str,item_name,affix,excluded_effect,category,exclude_category,item_id) -> None:
    try:
        with sqlite3.connect(pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db')) as conn:
            cur = conn.cursor()
            # if (effect == ".*") and (item_name == ".*") and (affix == ".*") and (excluded_effect == "none"):
            #     get_all(sorting,inverted,cur)
            # else:
            item_list = get_item_list_with_one_effect(cur,category,exclude_category,item_id)
            # for item in item_list:
            #     print(item)
            if item_name != ".*":
                item_list = filter_by_item(item_list,item_name)
            if affix != ".*":
                item_list = filter_by_affix(item_list,affix)
            if effect != ".*":
                item_list = filter_by_effect(item_list,effect)
            if excluded_effect != "none":
                item_list = filter_by_excluded_effect(item_list,excluded_effect)

            item_list = sort_list(item_list,sorting,inverted,effect.lower())
            for item in item_list:
                print(item)
            print("Amount =" ,len(item_list))
    except sqlite3.Error as e:
        print(e)

def get_all(sorting,inverted,cur:sqlite3.Cursor) -> None:
    if inverted:
        sort_order = "DESC"
    else:
        sort_order = "ASC"
    cur.execute(
        f"""WITH ranked AS (
            SELECT
                items.items_id,
                items.items_name,
                e.effect_name,
                ie.effect_strength,
                ROW_NUMBER() OVER (
                    PARTITION BY items.items_id
                    ORDER BY ie.effect_strength DESC, ie.effect_id
                ) AS rn
            FROM items
            LEFT JOIN item_effect AS ie ON ie.item_id = items.items_id
            LEFT JOIN effects AS e ON e.effect_id = ie.effect_id
            )
            SELECT
            items.items_name,
            MAX(CASE WHEN r.rn = 1 THEN r.effect_name     END) AS effect_1,
            MAX(CASE WHEN r.rn = 1 THEN r.effect_strength END) AS effect_strength_1,
            MAX(CASE WHEN r.rn = 2 THEN r.effect_name     END) AS effect_2,
            MAX(CASE WHEN r.rn = 2 THEN r.effect_strength END) AS effect_strength_2,
            MAX(CASE WHEN r.rn = 3 THEN r.effect_name     END) AS effect_3,
            MAX(CASE WHEN r.rn = 3 THEN r.effect_strength END) AS effect_strength_3,
            a.affix_name,
            ia.affix_strength
            FROM items
            LEFT JOIN ranked AS r ON r.items_id = items.items_id
            LEFT JOIN item_affix AS ia ON ia.item_id = items.items_id
            LEFT JOIN affix AS a ON a.affix_id = ia.affix_id
            GROUP BY
            items.items_name, a.affix_name, ia.affix_strength
            ORDER BY {sorting} {sort_order}
        """
    )
    #cur.execute("SELECT * FROM affix")
    rows = cur.fetchall()
    # for row in rows:
    #     print(f"{row}")

def get_item_list_with_one_effect(cur:sqlite3.Cursor,category,exclude_category,item_id) -> list[Any]:
    where = ""
    if category != "":
        where = f"WHERE effects.category == '{category}'"
    if exclude_category != "":
        where = f"WHERE effects.category != '{exclude_category}'"
    if item_id != 0:
        where = f"WHERE items.items_id == '{item_id}'"
    sql = f"""
        SELECT items.items_name, effects.effect_name, item_effect.effect_strength,affix.affix_name,item_affix.affix_strength
        FROM (((items
            LEFT JOIN item_effect ON item_effect.item_id = items.items_id)
            LEFT JOIN effects ON effects.effect_id = item_effect.effect_id)
            LEFT JOIN item_affix ON items.items_id = item_affix.item_id)
            LEFT JOIN affix ON item_affix.affix_id = affix.affix_id
        {where}
        ORDER BY items.items_name;
        """
    cur.execute(sql)
    rows = cur.fetchall()
    # for row in rows:
    #     print(f"{row}")
    return rows

def filter_by_item(item_list,item_name) -> list[Any]:
    result = []
    p = re.compile(item_name, re.IGNORECASE)

    for item in item_list:
        if p.match(item[0]):
            result += [item]
    return result

def filter_by_affix(item_list,affix) -> list[Any]:
    result = []
    p = re.compile(affix, re.IGNORECASE)
    for item in item_list:
        if item[3] and p.match(item[3]):
            result += [item]
    return result

def filter_by_effect(item_list,effect) -> list[Any]:
    result = []
    p = re.compile(effect, re.IGNORECASE)
    name: set = set(())
    for item in item_list:
        if item[1] and p.match(item[1]):
            name.add(item[0])
    for item in item_list:
        if item[0] in name:
            result += [item]
    return result

def filter_by_excluded_effect(item_list,excluded_effect) -> list[Any]:
    result = []
    p = re.compile(excluded_effect, re.IGNORECASE)
    name: set = set(())
    for item in item_list:
        if item[1] and p.match(item[1]):
            name.add(item[0])
    for item in item_list:
        if not (item[0] in name):
            result += [item]
    return result

def sort_list(item_list,sorting,inverted,effect) -> list[Any]:
    item_list = combine_list(item_list,effect)
    # for item in item_list:
    #     print(item)
    match sorting:
        case "effect_strength":
            item_list.sort(key=sort_by_effect_strength,reverse=not(inverted))
        case "affix_name":
            item_list.sort(key=sort_by_affix_name,reverse=not(inverted))
        case "affix_strength":
            item_list.sort(key=sort_by_affix_strength,reverse=not(inverted))
        case "effect_name":
            item_list.sort(key=sort_by_effect_name,reverse=not(inverted))
        case _:
            item_list.sort(key=sort_by_item_name,reverse=not(inverted))
    return item_list
        
def combine_list(item_list,effect) -> list[Any]:    
    result = []
    name_set = []
    for item in item_list:
        if not (item[0] in name_set):
            name_set += [item[0]]
    for name in name_set:
        rows = []
        for item in item_list:
            if item[0] == name:
                rows += [item]
        
        rows = sort_rows(rows,effect)
        affix = rows[0][3]
        affix_strength = rows[0][4]
        match len(rows):
            case 1:
                result += [(name,rows[0][1],rows[0][2],None,None,None,None,affix,affix_strength)]
            case 2:
                result += [(name,rows[0][1],rows[0][2],rows[1][1],rows[1][2],None,None,affix,affix_strength)]
            case 3:
                result += [(name,rows[0][1],rows[0][2],rows[1][1],rows[1][2],rows[2][1],rows[2][2],affix,affix_strength)]
            case _:
                raise IndexError(f"{name} has too many entries ({len(rows)}), try recreating the object\n Rows are: {rows}")
    # for item in result:
    #         print(f"{item}")
    return result           
    
def sort_rows(rows,effect):
    result = []
    p = re.compile(effect, re.IGNORECASE)
    for row in rows: #get first effect
        if row[1] and p.match(row[1]):
            result = [row]
    
    for row in rows: #attatch rest
        if not row[1] or not p.match(row[1]):
            result += [row]
    return result

def sort_by_effect_strength(item):
    if item[2]:
        return item[2]
    return 0

def sort_by_affix_name(item):
    if item[3]:
        return item[3][0]
    return "z"

def sort_by_affix_strength(item):
    if item[4]:
        return item[4]
    return 0

def sort_by_effect_name(item):
    if item[1]:
        return item[1][0]
    return "z"

def sort_by_item_name(item):
    if item[0][0]:
        return item[0][0]
    return "z"

def get_effects():
    try:
        with sqlite3.connect(pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db')) as conn:
            cur = conn.cursor()
            sql = f"""
                SELECT *
                FROM effects
                ORDER BY effects.effect_id;
                """
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                print(row)
    except sqlite3.Error as e:
        print(e)

def get_affixe():
    try:
        with sqlite3.connect(pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db')) as conn:
            cur = conn.cursor()
            sql = f"""
                SELECT *
                FROM affix
                ORDER BY affix.affix_id;
                """
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                print(row)
    except sqlite3.Error as e:
        print(e)

# SELECT items.items_name,
# AE.effect_name AS effect_1,A.effect_strength AS effect_strength_1,
# BE.effect_name AS effect_2,B.effect_strength AS effect_strength_2,
# CE.effect_name AS effect_3,C.effect_strength AS effect_strength_3,
# affix.affix_name,item_affix.affix_strength
# FROM (((((((items
#     LEFT JOIN item_effect A ON items.items_id = A.item_id)
#     LEFT JOIN effects AE ON A.effect_id = AE.effect_id)
#     LEFT JOIN item_effect B ON items.items_id = B.item_id)
#     LEFT JOIN effects BE ON B.effect_id = BE.effect_id)
#     LEFT JOIN item_effect C ON items.items_id = C.item_id)
#     LEFT JOIN effects CE ON C.effect_id = CE.effect_id)
#     LEFT JOIN item_affix ON items.items_id = item_affix.item_id)
#     LEFT JOIN affix ON item_affix.affix_id = affix.affix_id
# WHERE
#     A.effect_strength >= B.effect_strength
#     AND B.effect_strength >= C.effect_strength
# ORDER BY
#     items.items_name
