import json
import os
import re
import math
import collections

character_dir_path = "./characters/"  # path to the diractory that stores character info
character_data_list = []  # list of character data extracted from their respective files
index_of_loaded_character = None
current_tab = None


# displayes the navigation bar
def display_header():
    print(
        ("-[" if current_tab == "stats" else "- ")
        + "stats"
        + ("]" if current_tab == "stats" else " "),
        end="",
    )
    print(
        ("-[" if current_tab == "inventory" else "- ")
        + "inventory"
        + ("]" if current_tab == "inventory" else " "),
        end="",
    )
    print(
        ("-[" if current_tab == "skills" else "- ")
        + "skills"
        + ("]" if current_tab == "skills" else " "),
        end="",
    )
    print(
        ("-[" if current_tab == "spells" else "- ")
        + "spells"
        + ("]" if current_tab == "spells" else " "),
        end="",
    )
    print(
        ("-[" if current_tab == "languages" else "- ")
        + "languages"
        + ("]" if current_tab == "languages" else " "),
        end="",
    )
    print(
        ("-[" if current_tab == "help" else "- ")
        + "help"
        + ("]-" if current_tab == "help" else " -"),
        end="\n\n",
    )


# clears the console
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# checks if a character is loaded
def character_is_loaded(tab: str):
    global current_tab
    current_tab = tab
    clear()
    display_header()
    if index_of_loaded_character is None:
        print(
            "No character is currently loaded! please input 'load [character_name]' in order to load a character."
        )
        return False
    return True


# extracts caracter data from the file
def extract_character_data():
    character_data_directory_contents = os.listdir(
        character_dir_path
    )  # contants of the 'characters' folder
    character_data_files = []  # list of character data files

    for file in character_data_directory_contents:  # adds files with
        if re.findall("\.json$", file):
            character_data_files.append(file)

    if not character_data_files:
        raise FileExistsError(
            "There are currently no json files in the 'character' directory.\nPlease add a character to the directory."
        )

    for character in character_data_files:
        with open(f"./characters/{character}", "r") as file:
            character_data_list.append(json.load(file))


# saves the character data to the character file
def save_character_data():
    character_data_directory_contents = os.listdir(character_dir_path)
    for character in character_data_list:
        with open(
            f"./characters/{character_data_directory_contents[character_data_list.index(character)]}",
            "w",
        ) as file:
            json.dump(character, file)


# reads the character data from the files and updates the rendering
def update_character_data():
    clear()
    character_data_directory_contents = os.listdir(character_dir_path)
    global character_data_list
    character_data_list.clear()

    character_data_files = []

    for file in character_data_directory_contents:
        if re.findall("\.json$", file):
            character_data_files.append(file)

    if not character_data_files:
        raise FileExistsError(
            "There are currently no json files in the 'character' directory.\nPlease add a character to the directory."
        )

    for character in character_data_files:
        with open(f"./characters/{character}", "r") as file:
            character_data_list.append(json.load(file))
    display_header()


def get_user_input():
    user_input: str = input("\n\n\nPlease enter a command: ").lower()
    match user_input:
        case "1":
            stats()
            return
        case "2":
            inventory()
            return
        case "3": 
            skills()
            return
        case "4":
            spells()
            return
        case "5":
            languages()
            return
        case "6":
            display_help()
            return
    
    if re.findall("\Aload", user_input):
        load(user_input.replace("load", "").strip())
    elif re.findall("\Aupd", user_input):
        update_character_data()
    elif re.findall("\Asta", user_input):
        stats()
    elif re.findall("\Ainv", user_input):
        inventory()
    elif re.findall("\Aski", user_input):
        skills()
    elif re.findall("\Alan", user_input):
        languages()
    elif re.findall("\Aspe", user_input):
        spells()
    elif re.findall("\Ahel", user_input):
        display_help()
    elif re.findall("\Apay", user_input):
        try:
            pay(int(user_input.replace("pay", "").strip()))
        except ValueError:
            print("Error, the payed amount can only be a number. Please try again.")
    elif re.findall("\Aearn", user_input):
        try:
            earn(int(user_input.replace("earn", "").strip()))
        except ValueError:
            print("Error, the earned amount can only be a number. Please try again.")
    elif re.findall("\Adamage", user_input):
        try:
            damage(int(user_input.replace("damage", "").strip()))
        except ValueError:
            print("Error, the damage value can only be a number. Please try again.")
    elif re.findall("\Adam", user_input):
        try:
            damage(int(user_input.replace("dam", "").strip()))
        except ValueError:
            print("Error, the damage value can only be a number. Please try again.")
    elif re.findall("\Aheal", user_input):
        try:
            heal(int(user_input.replace("heal", "").strip()))
        except ValueError:
            print("Error, the health value can only be a number. Please try again.")
    elif re.findall("\Adescribe", user_input):
        describe(user_input.replace("describe", "").strip())
    elif re.findall("\Adesc", user_input):
        describe(user_input.replace("desc", "").strip())
    else:
        clear()
        print(
            f"Unknown command '{user_input}'. Input 'help' to see all commands and their uses."
        )


def earn(amount: str):
    print(amount)
    if character_is_loaded("stats") is None:
        return
    character_data_list[index_of_loaded_character]["inventory"]["Gold Piece"][
        "count"
    ] += amount
    save_character_data()
    stats()


def pay(amount: str):
    if character_is_loaded("stats") is None:
        return
    character_data_list[index_of_loaded_character]["inventory"]["Gold Piece"][
        "count"
    ] -= amount
    save_character_data()
    stats()


def load(character_name: str):
    clear()
    update_character_data()
    all_characters = []
    possible_characters = []
    for character in character_data_list:
        all_characters.append(character["name"])
        if character_name in str(character["name"]).lower():
            possible_characters.append(character["name"])

    if len(possible_characters) == 0:
        print(f"No character with name '{character_name}' found.")
        print("Please pick one of the following names: ", end="")
        for character in all_characters:
            print(
                "'"
                + character
                + "'"
                + (" , " if (all_characters[-1] != character) else ""),
                end="",
            )
        print()
    elif len(possible_characters) == 1:
        for character in character_data_list:
            if character["name"] == possible_characters[0]:
                global index_of_loaded_character
                index_of_loaded_character = character_data_list.index(character)
                stats()
    else:
        print("No exact matches did you mean ", end="")
        for character in possible_characters:
            print(
                "'"
                + character
                + "'"
                + (" or " if (possible_characters[-1] != character) else "?"),
                end="",
            )
        print()


def stats():
    """Diplays stats of the loaded character."""
    if not character_is_loaded("stats"):
        return
    for field in character_data_list[index_of_loaded_character]:
        if field != "stats":
            if field == "hp":
                print(
                    f"{field+':':<15}"
                    + f"{character_data_list[index_of_loaded_character][field]['current']} / {character_data_list[index_of_loaded_character][field]['max']}"
                )
                continue
            print(
                f"{field+':':<15}"
                + f"{character_data_list[index_of_loaded_character][field]}"
            )
        else:
            print(
                f"{'gp:':<15}"
                + f"{character_data_list[index_of_loaded_character]['inventory']['Gold Piece']['count']}"
            )
            loaded_character_stats = character_data_list[index_of_loaded_character][
                "stats"
            ]
            for stat in loaded_character_stats:
                base_mod = math.floor((loaded_character_stats[stat]["base"] - 10) / 2)
                print(f"{(stat + ':'):<14}", end="")
                print(f"{loaded_character_stats[stat]['base']:>2}", end=" ")
                print(
                    f"(save: {('+' if base_mod + loaded_character_stats[stat]['save'] > 0 else '') + str(loaded_character_stats[stat]['save'] + base_mod):>3})"
                )
                for substat in loaded_character_stats[stat]:
                    if substat in ("base, save"):
                        continue
                    print(
                        f"    {(substat + ':'):<20}{('+' if loaded_character_stats[stat][substat] + base_mod > 0 else '') + str(loaded_character_stats[stat][substat] + base_mod):>3}"
                    )
                print()
            break


def inventory():
    if not character_is_loaded("inventory"):
        return
    character_inventory = character_data_list[index_of_loaded_character]["inventory"]
    character_inventory = dict(
        collections.OrderedDict(
            sorted(character_data_list[index_of_loaded_character]["inventory"].items())
        )
    )
    character_inventory = dict(
        sorted(character_inventory.items(), key=lambda kv: kv[1]["catigory"])
    )
    current_catigory = None
    for item in character_inventory:
        item_catigory = str(character_inventory[item]["catigory"])
        item_catigory = item_catigory.capitalize()
        if current_catigory != item_catigory:
            print(item_catigory + ":")
            current_catigory = item_catigory
        print(
            f"{('[' + str(character_inventory[item]['count']) + ']' if character_inventory[item]['count'] > 1 else '>'):>6} "
            + item
        )


def skills():
    if not character_is_loaded("skills"):
        return
    for skill in character_data_list[index_of_loaded_character]["skills"]:
        print(
            f"{skill}:\n    {character_data_list[index_of_loaded_character]['skills'][skill]}"
        )


def languages():
    if not character_is_loaded("languages"):
        return
    longest_length = 0
    for language in character_data_list[index_of_loaded_character]["languages"]:
        if len(language) > longest_length:
            longest_length = len(language)
    for language in character_data_list[index_of_loaded_character]["languages"]:
        print(
            f"{language + ':':<{longest_length + 2}}{character_data_list[index_of_loaded_character]['languages'][language]}"
        )


def damage(damage_value: int):
    if character_is_loaded("stats") is None:
        return
    character_data_list[index_of_loaded_character]["hp"]["current"] -= damage_value
    if character_data_list[index_of_loaded_character]["hp"]["current"] < 0:
        character_data_list[index_of_loaded_character]["hp"]["current"] = 0
    save_character_data()
    stats()


def heal(heal_value: int):
    if character_is_loaded("stats") is None:
        return
    character_data_list[index_of_loaded_character]["hp"]["current"] += heal_value
    if (
        character_data_list[index_of_loaded_character]["hp"]["current"]
        > character_data_list[index_of_loaded_character]["hp"]["max"]
    ):
        character_data_list[index_of_loaded_character]["hp"]["current"] = (
            character_data_list[index_of_loaded_character]["hp"]["max"]
        )
    save_character_data()
    stats()


def spells():
    if not character_is_loaded("spells"):
        return
    character_inventory = character_data_list[index_of_loaded_character]["spells"]
    character_inventory = dict(
        collections.OrderedDict(
            sorted(character_data_list[index_of_loaded_character]["spells"].items())
        )
    )
    character_inventory = dict(
        sorted(character_inventory.items(), key=lambda kv: kv[1]["lvl"])
    )
    character_inventory = dict(
        sorted(character_inventory.items(), key=lambda kv: kv[1]["type"])
    )
    current_catigory = None
    for item in character_inventory:
        item_catigory = str(character_inventory[item]["type"])
        item_catigory = item_catigory.capitalize()
        if current_catigory != item_catigory:
            print(item_catigory + ":")
            current_catigory = item_catigory
        print(
            f"{('[' + str(character_inventory[item]['lvl']) + ']' if character_inventory[item]['lvl'] > 1 else '>'):>6} "
            + item
        )


def display_help():
    clear()
    global current_tab
    current_tab = "help"
    display_header()
    print(
        "- Enter 'load [character_name] in order to load a character.\n"
        "Example: load Spring Caria\n"
        "Tip: You don't actually need to fully type out the name of the character. \n"
        "    As long as the entered string of text is unique to the name of the character (e.g. 'spr' or 'aria' for 'Spring Caria') it will understand.\n"
    )
    print(
        "- Enter the name of the tab from the navbar up top to go to that tab.\n"
        "Example: stats\n"
        "Tip: You don't actually need to type out the whole tab name. \n"
        "    The first three letters are enough (e.g. 'lan' for 'languages').\n"
    )
    print(
        "- Enter 'damage [damage_number]' in order to reduce the health of the currently loaded character by the specified number.\n"
        "Example: damage 3\n"
    )
    print(
        "- Enter 'heal [health_number] in order to heal the currently loaded character by the specified number.\n"
        "Example: heal 3\n"
    )
    print(
        "- Enter 'describe [entity_name] in order to see the description of an item/spell.\n"
        "    Note: This function only works in 'inventory' and 'spells' tabs.\n"
        "Example: describe steal sword.\n"
        "Tip: You can also shorten this command to 'desc' (e.g. 'desc bow').\n"
        "    Note: you can only type 'desc' OR 'describe'. Variants of the word like 'des' or 'descri' will not work.\n"
        "Tip: you don't actuallly need to type out the whole name of the entity.\n"
        "    As long as the entered string of text is unique to the item (e.g. 'bow' or 'cro' for 'crossbow') it will understand.\n"
    )
    print(
        "- Enter 'update' in order to update the character data form the data files in [./characters]\n"
        "Example: uptade\n"
        "Tip:You don't actually need to type out he whole command you can just 'upd' and it will undestand.\n"
    )


def describe(entity_name: str):
    match current_tab:
        case "inventory":
            describe_item(entity_name)
        case "spells":
            describe_spell(entity_name)
        case _:
            print("There are nothing that can be described on this page.")


def describe_item(item_name: str):
    if index_of_loaded_character is None:
        print(
            "No character is currently loaded! please input 'load [character_name]' in order to load a character."
        )
        return
    all_items = []
    possible_items = []
    for item in character_data_list[index_of_loaded_character]["inventory"]:
        all_items.append(item)
        if item_name in str(item).lower():
            possible_items.append(item)

    if len(possible_items) == 0:
        print(f"No item '{item_name}' found.")
        print("Please pick one of the following names: ", end="")
        for item in all_items:
            print("'" + item + "'" + (" , " if (all_items[-1] != item) else ""), end="")
        print()
    elif len(possible_items) == 1:
        for item in character_data_list[index_of_loaded_character]["inventory"]:
            if item == possible_items[0]:
                print(
                    f"{item}:\n    {character_data_list[index_of_loaded_character]['inventory'][item]['description']}"
                )
    else:
        print("No exact matches did you mean ", end="")
        for item in possible_items:
            print(
                "'" + item + "'" + (" or " if (possible_items[-1] != item) else "?"),
                end="",
            )
        print()


def describe_spell(spell_name: str):
    if index_of_loaded_character is None:
        print(
            "No character is currently loaded! please input 'load [character_name]' in order to load a character."
        )
        return
    all_spells = []
    possible_spells = []
    for spell in character_data_list[index_of_loaded_character]["spells"]:
        all_spells.append(spell)
        if spell_name in str(spell).lower():
            possible_spells.append(spell)

    if len(possible_spells) == 0:
        print(f"No spell '{spell_name}' found.")
        print("Please pick one of the following names: ", end="")
        for spell in all_spells:
            print(
                "'" + spell + "'" + (" , " if (all_spells[-1] != spell) else ""), end=""
            )
        print()
    elif len(possible_spells) == 1:
        for spell in character_data_list[index_of_loaded_character]["spells"]:
            if spell == possible_spells[0]:
                print(
                    f"{spell}:\n    {character_data_list[index_of_loaded_character]['spells'][spell]['description']}"
                )
    else:
        print("No exact matches did you mean ", end="")
        for spell in possible_spells:
            print(
                "'" + spell + "'" + (" or " if (possible_spells[-1] != spell) else "?"),
                end="",
            )
        print()


def main():
    extract_character_data()
    clear()
    stats()
    while True:
        get_user_input()


main()
