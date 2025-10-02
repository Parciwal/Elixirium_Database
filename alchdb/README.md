# Elexirium Database

Installation Guide:

You need to have python installed. Check if you have that before continuing.
Windows: you can install ythong through the Microsoft Store.

Open your command line window (cmd, preferably wsl bash)

Navigate to a folder of your choice (on windows, you can go to the folder in file explorer and type "cmd" in the navigation bar to open the comand line window there).
Where the folder is and what is in it is not important, it will just host our virtual enviroment. Make sure you can find it again.

Create you virtual enviroment with the following command:

`python .m venv .venv`

This will create the folder .venv with your virtual enviroment.
This virtual enviroment(venv) is so, we install the package locally. This is cleaner that installing it system wide.

Now activate the venv with on of the following commands:

Windows CMD: `call .venv\Scripts\activate`

Unix: `source .venv/bin/activate`

make sure you can run pip:

Windows: `py -m pip --version`

Unix: `python3 -m pip --version`

If pip is not installed, follow the tutorial on this site: https://packaging.python.org/en/latest/tutorials/installing-packages/

Now we have the comandline prepared, next unpack the distribution into the folder you have your .venv in. It makes accessing it easier.

As the last step, run the install command:

`pip install alchdb-1.0.1-py3-none-any.whl`

If you put the files somewhere else, you need the path to the .whl file.

Now to creating your database:

First initialize it with Init like this:

`alchdb init`

At the top of the resulting execution, you can see the path where the database is being created. You'll see it is below the folder you are currently in.

Be careful every time you run this command, it will delete the old database. It is reccomended to make backups with `alchdb backup`.
Use `alchdb backup -h`for more info.

----------

To add an item, simply use the add command, here an Example:

`alchdb add -n Bowl -en fir%,wat% -es 19,9 -an %pre% -as 12`

Explanation:

`-n` 

The name of your item. Any string will do, but it is recommended to replace spaces with underscores (_) to make typing easier. If you still want spaces, encase your name in quotationmarks.

`-en` 

A list of all effects, seperated by Comma, the item gives. Use % as a standin for any amount of any character. This can be used to shorten the names, it just has to be unique to that effect. If it isn't unique, It will throw an error. 
The vanilla effects are intigrated, for modded effects, you can enter tham manuall into the database, run `alchdb effect -h` for more info.

`-es` 

A list of strengths for the effects. The Order must be the same, as the list of effects.

`-an` 

The name of the affix. Can be left out if no affix is there. The affixes are not included, you have to type them out completely when you use them for the first time. You can also abbreviate them with %.
If you try to get an affix you don't have in the database with % abbreviation, it will throw an error and tell you to enter the fll name next time.

`-as`

The strength of the affix, any integer is valid.

Optional:

`-o`

The override, if you messed up last time and need to override the item, use this. Caution: this will override the item with the same name. If you misspelled the name, you have to rename it, run `alchdb modify -h` for more info.

-----------

Now for retrieving that Item. Retrieving items is done with the get command:

`alchdb get -i ".\*raw.\*" -c pos -e haste -s`

Explanation:

`-i`

The item name. Accepts regex notation. .* means any Character except newline. So this will return any Item with "raw" in the name.

`-c`

The Category. All efects are classed into one of three categories. Positive, negative, neuter (pos/neg/neut). You can see all effects and their cateogries by running `alchdb get .es`.
If you want to change a category, look at `alchdb effect -h` for more info.

`-e`

The effect name. Filters all items after this effect. This effect will now be in the first column, and sorting by affect strength will now sort in regards to this effect,

`-s`

Sort by effect strength.

To get the whole Database, simply run `aldchdb get`without any arguments.