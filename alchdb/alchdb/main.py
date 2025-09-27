from alchdb import connect, add_stuff, get, modify, affix_and_effects,backup

import sqlite3
import argparse
import pathlib
import os
import sys

def main():
    sys.tracebacklimit = 0
    args = PARSER.parse_args()
    
    match args.command:
        case "backup":
            if args.save:
                backup.save(args.backup_name)
            else:
                backup.load(args.backup_name)
        case "insert":
            add_stuff.add_elements(
                args.item_name,
                args.effect_names.split(","),
                list(map(int,args.effect_strengths.split(","))),
                args.affix_name,
                args.affix_strength,
                args.override
            )
        
        case "init":
            if os.path.exists(pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db')):
                os.remove(pathlib.Path(__file__).parent.resolve().joinpath('ingredients.db'))
            connect.create_tables()
            connect.import_effects()
            if args.test:
                connect.insert_test_vals()
        case "modify":
            modify.modify_item(
                args.item_name_,
                args.effect_or_affix_name_,
                args.add_effect,
                args.add_aff,
                args.rename_item,
                args.delete
            )
        case "get":

            if args.effects:
                get.get_effects()
                return
            if args.affixe:
                get.get_affixe()
                return
            sorting = "item_name"
            if args.strength:
                sorting = "effect_strength"
            if args.name_affix:
                sorting = "affix_name"
            if args.affix_strength:
                sorting = "affix_strength"
            if args.name_effect:
                sorting = "effect_name"
            get.get_stuff(
                sorting,
                args.inverted,
                args.effect,
                args.item,
                args.affix,
                args.exclude_effect,
                args.category,
                args.exclude_category,
                args.item_id
            )
        case "effect":
            if args.delete_effect:
                affix_and_effects.del_effect(
                    args._effect_name
                )
            elif args._effect_category != "":
                affix_and_effects.change_or_add_effect(
                    args._effect_name,
                    args._effect_category
                )
            elif args._effect_rename != "":
                affix_and_effects.rename_effect(
                    args._effect_name,
                    args._effect_rename
                )
        case "affix":
            if args.delete_affix:
                affix_and_effects.del_affix(
                    args._affix_name
                )
            else:
                try:
                    with sqlite3.connect('ingredients.db') as conn:
                        add_stuff.add_affix(
                            conn,
                            args._affix_name
                        )
                except sqlite3.Error as e:
                    print(e)

PARSER = argparse.ArgumentParser(prog="aldb",description="A database for alchemy essences")

subparsers = PARSER.add_subparsers(dest="command")

parser_init = subparsers.add_parser("init",help="delete old database and initiliaze new one")
parser_init.add_argument("-t","--test",action="store_true")

parser_backup = subparsers.add_parser("backup",help="make a Backup of your current Database")

load_or_save = parser_backup.add_mutually_exclusive_group(required=True)
load_or_save.add_argument("-s","--save",action="store_true")
load_or_save.add_argument("-l","--laod",action="store_true")
parser_backup.add_argument("backup_name",type=str,nargs='?',help="name of backup, default=Old",default="Old")



parser_insert = subparsers.add_parser("add",help="add item")
parser_insert.add_argument("-n","--item_name",help="name of item to be added",required=True,type=str)
parser_insert.add_argument("-en","--effect_names",required=True,type=str,help="effect names split by a comma")
parser_insert.add_argument("-es","--effect_strengths",required=True,type=str,help="effect strengths split by a comma")
parser_insert.add_argument("-an","--affix_name",default=None,type=str,help="affix name to be used, if not existent, will add. Use %% to allow any amount of any character")
parser_insert.add_argument("-as","--affix_strength",default=None,type=int)
parser_insert.add_argument("-o","--override",help="override item",default=None,action="store_true")

parser_modify_effect = subparsers.add_parser("effect",help="modify effect")

parser_modify_effect.add_argument("-efn","--_effect_name",required=True,type=str)
effect_change = parser_modify_effect.add_mutually_exclusive_group(required=True)
effect_change.add_argument("-c","--_effect_category",default="",type=str)
effect_change.add_argument("-de","--delete_effect",help="delete effect",action="store_true")
effect_change.add_argument("-r","--_effect_rename",default="",type=str)


parser_modify_affix = subparsers.add_parser("affix",help="modify affix")

parser_modify_affix.add_argument("-afn","--_affix_name",required=True,type=str)
parser_modify_affix.add_argument("-da","--delete_affix",help="delete affix",action="store_true")


parser_modify_item = subparsers.add_parser("modify",help="modify item")

parser_modify_item.add_argument("-in","--item_name_",required=True,type=str)
parser_modify_item.add_argument("-eaf","--effect_or_affix_name_",default=".*",type=str)

change = parser_modify_item.add_mutually_exclusive_group(required=True)
change.add_argument("-a","--add_effect",help="add effect with strength",type=int,default=0)
change.add_argument("-adf","--add_aff",help="add affix with strength",type=int,default=0)
change.add_argument("-d","--delete",help="delete effect for item",action="store_true")
change.add_argument("-re","--rename_item",help="new name for item",default="",type=str)


parser_get = subparsers.add_parser("get",help="get item") #filter
parser_get.add_argument("-e","--effect",help="limit by effect name, accepts Regex (.* for any amount of any char)",default=".*")
parser_get.add_argument("-i","--item",help="limit by item name, accepts Regex",default=".*")
parser_get.add_argument("-a","--affix",help="limit by affix name, accepts Regex",default=".*")
parser_get.add_argument("-ee","--exclude_effect",help="exclude by effect name, accepts Regex",default="none")
parser_get.add_argument("-es","--effects",help="print all effects, accepts Regex",action="store_true")
parser_get.add_argument("-ae","--affixe",help="print all affixe, accepts Regex",action="store_true")

category = parser_get.add_mutually_exclusive_group()
category.add_argument("-c","--category",help="Filter for Effect with Category (pos/neg/neut)",default="")
category.add_argument("-ec","--exclude_category",help="Exclude Effect with Category (pos/neg/neut)",default="")
parser_get.add_argument("-id","--item_id",help="onle get item with this id",type=int,default=0)

parser_sorting = parser_get.add_mutually_exclusive_group() #wonach sortiert werden soll
parser_sorting.add_argument("-s","--strength",help="sort by effect strength",action="store_true")
parser_sorting.add_argument("-na","--name_affix",help="sort by affix",action="store_true")
parser_sorting.add_argument("-as","--affix_strength",help="sort by affix strength",action="store_true")
parser_sorting.add_argument("-ne","--name_effect",help="sort by effect",action="store_true")

parser_get.add_argument("-in","--inverted",help="invert_sorting",action="store_true")



if __name__ == '__main__':
    main()