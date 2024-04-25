import json
import os
import re
import math
import collections

character_dir_path = "./characters/"  # path to the diractory that stores character info
character_data_list = []  # list of character data extracted from their respective files
index_of_loaded_character = None
current_tab: str = "stats"


# clears the console
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# checks if a character is loaded
def is_character_loaded(tab: str):
    global current_tab
    current_tab = tab
    clear()
    display_header()
    if index_of_loaded_character is None:
        print(
            "No character is currently loaded! Please input 'load [character_name]'.\n"
            "Contents of the characters folder:"
        )
        for character in character_data_list:
            print(
                f"{character_data_list.index(character)+1}. " + f"{character['name']}"
            )
        return False
    return True


# extracts caracter data from the file
def extract_character_data():
    character_data_directory_contents = os.listdir(character_dir_path)
    character_data_files = []

    for file in character_data_directory_contents:
        if re.findall("\.json$", file):
            character_data_files.append(file)

    if not character_data_files:
        raise FileExistsError(
            "There are currently no json files in the 'character' directory.\nPlease add a character to the directory."
        )

    for character in character_data_files:
        with open(f"{character_dir_path}{character}", "r") as file:
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


# handles input by the user and the program itself
def handle_input(program_input: str = None):
    if program_input:
        user_input = program_input
    else:
        user_input: str = input("\n\n\n>>> ").lower()

    if user_input[0] is "1":
        stats()
    elif user_input[0] is "2":
        inventory()
    elif user_input[0] is "3":
        spells()
    elif user_input[0] is "4":
        skills()
    elif user_input[0] is "5":
        languages()
    elif user_input[0] is "6":
        help()
    elif re.findall("\Aload", user_input):
        load(user_input.replace("load", "").strip())
    elif re.findall("\Asta", user_input):
        stats()
    elif re.findall("\Ainv", user_input):
        inventory()
    elif re.findall("\Aspe", user_input):
        spells()
    elif re.findall("\Aski", user_input):
        skills()
    elif re.findall("\Alan", user_input):
        languages()
    elif re.findall("\Ahel", user_input):
        help()
    elif re.findall("\Aadd", user_input):
        add()
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
    elif re.findall("\Adelete", user_input):
        delete(user_input.replace("delete", "").strip())
    elif re.findall("\Adel", user_input):
        delete(user_input.replace("del", "").strip())
    else:
        clear()
        display_header()
        print(
            f"Unknown command '{user_input}'. Input 'help' to see all commands and their uses."
        )


# loads a caracter from the character list
def load(character_name: str):
    clear()
    update_character_data()
    possible_characters = []
    for character in character_data_list:
        if character_name.lower() in str(character["name"]).lower():
            possible_characters.append(character["name"])

    if len(possible_characters) == 0:
        print(f"No character with name '{character_name}' found.")
        print("Please pick one of the following names: ")
        for character in character_data_list:
            print(f"{character_data_list.index(character)+1}." + f"{character['name']}")
        print()
    elif len(possible_characters) == 1:
        for character in character_data_list:
            if character["name"] == possible_characters[0]:
                global index_of_loaded_character
                index_of_loaded_character = character_data_list.index(character)
                handle_input(current_tab)
    else:
        print("No exact matche, pleaes select one of the following:")
        for character in possible_characters:
            print(
                f"{possible_characters.index(character)+1}. " + character
            )
        print()


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
        ("-[" if current_tab == "spells" else "- ")
        + "spells"
        + ("]" if current_tab == "spells" else " "),
        end="",
    )
    print(
        ("-[" if current_tab == "skills" else "- ")
        + "skills"
        + ("]" if current_tab == "skills" else " "),
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


# displays the stats of the loaded character
def stats():
    """Diplays stats of the loaded character."""
    if not is_character_loaded("stats"):
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
                + f"{character_data_list[index_of_loaded_character]['inventory']['gp']['count']}"
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


# displays the inventory of the loaded character
def inventory():
    if not is_character_loaded("inventory"):
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
    print()


# displayes the skills of the loaded character
def skills():
    if not is_character_loaded("skills"):
        return
    for skill in character_data_list[index_of_loaded_character]["skills"]:
        print(
            f"> {skill}:\n{character_data_list[index_of_loaded_character]['skills'][skill]}\n"
        )


# displays the spells of the loaded character
def spells():
    if not is_character_loaded("spells"):
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
    print()


# displays the languages of the loaded characer
def languages():
    if not is_character_loaded("languages"):
        return
    longest_length = 0
    for language in character_data_list[index_of_loaded_character]["languages"]:
        if len(language) > longest_length:
            longest_length = len(language)
    for language in character_data_list[index_of_loaded_character]["languages"]:
        print(
            f"{language + ':':<{longest_length + 2}}{character_data_list[index_of_loaded_character]['languages'][language]}"
        )


# displays the help menu
def help():
    clear()
    global current_tab
    current_tab = "help"
    display_header()
    print(
        """(*Note: if the formatting looks broken use ctrl + MMB to zoom out in order to fix it)  

Command abbreviation explained:
├─> [] - expected data to be inputed
│   └─> Example: 'heal [health healed]' -> 'heal 3'
└─> () - the command could also be shortened to the specified form
    ├─> Example: 'describe(desc) [item/spell name]' -> 'desc Sword')
    └─> Notes: 
        └─> the '|' marks different ways in which the command can be shortend

Navigation:
├─> stats(sta | 1)     - navigates to the stats screen
├─> inventory(inv | 2) - navigates to the inventory tab
├─> spells(spe | 3)    - navigates to the spells tab
├─> skills(ski | 4)    - navigates to the skills tab
├─> languages(lan | 5) - navigates to the languages tab
└─> help(hel | 6)      - navigates to the help menu (Yippee! You found it!)
    
Tab spacific commands:
├─> Stats:
│   ├─> Money manipulation:
│   │   ├─> earn [amount earned] - increases gp count by the specified amount
│   │   └─> pay [amount payed]   - decreases gp count by the specified amount
│   └─> Health manipulation:
│       ├─> heal [amount healed]       - increases hp by specified amount up to max hp
│       └─> damage(dam) [damage taken] - decreases hp by specified amount down to 0 hp
├─> Inventory:
│   ├─> add                        - starts the sequence of adding an item
│   ├─> delete(del) [item name]    - deletes the specified item
│   └─> describe(desc) [item name] - displays the description of the specified item
├─> Spells:
│   ├─> add                         - starts the sequence of adding a spell
│   ├─> delete(del) [spell name]    - deletes the sepecified spell
│   └─> describe(desc) [spell name] - displays the descriptino of the specified spell
├─> Skills:
│   ├─> add                      - starts the sequence of adding a skill
│   └─> delete(del) [skill name] - deletes the specified skill
└─> Languages:
    ├─> add                      - starts the sequence of adding a language
    └─> delete(del) [skill name] - deletes the specified language
"""
    )


# deducts the specified amount of hp from the loaded character
def damage(damage_value: int):
    if is_character_loaded("stats") is None:
        return
    character_data_list[index_of_loaded_character]["hp"]["current"] -= damage_value
    if character_data_list[index_of_loaded_character]["hp"]["current"] < 0:
        character_data_list[index_of_loaded_character]["hp"]["current"] = 0
    save_character_data()
    stats()


# heal the loaded character py the specified amount
def heal(heal_value: int):
    if is_character_loaded("stats") is None:
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


# increment the money of the loaded character by the specified amount
def earn(amount: str):
    print(amount)
    if is_character_loaded("stats") is None:
        return
    character_data_list[index_of_loaded_character]["inventory"]["Gold Piece"][
        "count"
    ] += amount
    save_character_data()
    stats()


# decrease the money of the loaded character by the specified amount
def pay(amount: str):
    if is_character_loaded("stats") is None:
        return
    character_data_list[index_of_loaded_character]["inventory"]["Gold Piece"][
        "count"
    ] -= amount
    save_character_data()
    stats()


# calls one of the describs functions depending on which tab the user is currently on
def describe(entity_name: str):
    match current_tab:
        case "inventory":
            describe_item(entity_name)
        case "spells":
            describe_spell(entity_name)
        case _:
            handle_input(current_tab)
            print("There are nothing that can be described on this page.")

    def describe_item(item_name: str):
        if index_of_loaded_character is None:
            print(
                "No character is currently loaded! Please input 'load [character_name]' ."
            )
            return

        possible_items = []
        for item in character_data_list[index_of_loaded_character]["inventory"]:
            if item_name in str(item).lower():
                possible_items.append(item)

        handle_input(current_tab)
        if len(possible_items) == 0:
            print(f"No item with name '{item_name}' found.")
        elif len(possible_items) == 1:
            print(
                f"> {possible_items[0]}:\n{character_data_list[index_of_loaded_character]['inventory'][possible_items[0]]['description']}"
            )
        else:
            print("No exact match. Possible items: ", end="")
            for item in possible_items:
                print(
                    item + (", " if (possible_items[-1] != item) else ""),
                    end="",
                )
            print()

    def describe_spell(spell_name: str):
        if index_of_loaded_character is None:
            print(
                "No character is currently loaded! Please input 'load [character_name]' ."
            )
            return

        possible_spells = []
        for spell in character_data_list[index_of_loaded_character]["spells"]:
            if spell_name in str(spell).lower():
                possible_spells.append(spell)

        handle_input(current_tab)
        if len(possible_spells) == 0:
            print(f"No spell with name '{spell_name}' found.")
        elif len(possible_spells) == 1:
            print(
                f"> {possible_spells[0]}:\n{character_data_list[index_of_loaded_character]['spells'][possible_spells[0]]['description']}"
            )
        else:
            print("No exact match. Possible spells: ", end="")
            for spell in possible_spells:
                print(
                    spell + (", " if (possible_spells[-1] != spell) else ""),
                    end="",
                )
            print()


# starts the process of adding something to the dataset
def add():
    def add_item():
        if not is_character_loaded("inventory"):
            return

        name: str
        count: int
        catigory: str
        description: str

        name = input(
            "Press [enter] without entering any text to cancel adding an item.\n"
            "\n"
            "Please enter a name of the item you want to add: "
        )

        if name is "":
            inventory()
            return

        for item in character_data_list[index_of_loaded_character]["inventory"]:
            if str(item).lower == name.lower():
                character_data_list[index_of_loaded_character]["inventory"][name][
                    "count"
                ] += 1
                inventory()
                print("\nSince the item already exists, it's count was incremented.")
                return

        try:
            count = int(
                input(
                    "\n(*Note: cancels adding an item if the input consists of any symbols other then 0-9)\n"
                    "Please enter the count of the item: "
                )
            )
        except ValueError:
            inventory()
            return

        catigory = input(
            "\nPlease enter the catigory into which the item belongs: "
        ).lower()

        if not catigory:
            inventory()
            return

        description = input("\nPlease enter a description for the item: ")

        if not description:
            inventory()
            return

        character_data_list[index_of_loaded_character]["inventory"][name] = {
            "catigory": catigory,
            "count": count,
            "description": description,
        }
        save_character_data()
        inventory()

    def add_spell():
        if not is_character_loaded("spells"):
            return

        name: str
        lvl: int
        type: str
        description: str

        name = input(
            "Press [enter] without entering any text to cancel adding a spell.\n"
            "\n"
            "Please enter a name of the spell you want to add: "
        )

        if name is "":
            spells()
            return

        for spell in character_data_list[index_of_loaded_character]["spells"]:
            if str(spell).lower == name.lower():
                spells()
                print(
                    "\nA spell with this name already exists! You can't have 2 spells with the exact same name."
                )
                return

        try:
            lvl = int(
                input(
                    "\n(*Note: cancels adding a spell if the input consists of any symbols other then 0-9)\n"
                    "Please enter the count of the item: "
                )
            )
        except ValueError:
            spells()
            return

        type = input("\nPlease enter type of the spell: ").lower()

        if not type:
            spells()
            return

        description = input("\nPlease enter a description for the spell: ")

        if not description:
            spells()
            return

        character_data_list[index_of_loaded_character]["spells"][name] = {
            "type": type,
            "lvl": lvl,
            "description": description,
        }
        save_character_data()
        spells()

    def add_skill():
        if not is_character_loaded("skills"):
            return

        name: str
        description: str

        name = input(
            "Press [enter] without entering any text to cancel adding the skill.\n"
            "\n"
            "Please enter a name of the skill you want to add: "
        )

        if name is "":
            skills()
            return

        for skill in character_data_list[index_of_loaded_character]["skills"]:
            if str(skill).lower == name.lower():
                skills()
                print(
                    "\nA skill with this name already exists! You can't have 2 skills with the exact same name."
                )
                return

        description = input("\nPlease enter a description for the sikll: ")

        if not description:
            skills()
            return

        character_data_list[index_of_loaded_character]["skills"][name] = description
        save_character_data()
        skills()

    def add_language():
        if not is_character_loaded("languages"):
            return

        name: str
        lvl: str

        name = input(
            "Press [enter] without entering any text to cancel adding the language.\n"
            "\n"
            "Please enter the language you want to add: "
        )

        if name is "":
            languages()
            return

        for language in character_data_list[index_of_loaded_character]["languages"]:
            if str(language).lower == name.lower():
                languages()
                print(
                    "\nA language with this name already exists! You can't have 2 languages with the exact same name."
                )
                return

        lvl = input("\nPlease enter a description for the language: ")

        if not lvl:
            spells()
            return

        character_data_list[index_of_loaded_character]["languages"][name] = lvl
        save_character_data()
        languages()

    match current_tab:
        case "inventory":
            add_item()
        case "spells":
            add_spell()
        case "skills":
            add_skill()
        case "languages":
            add_language()
        case _:
            print("There is nothing you can add on this page.")


# starts the process of deleting something from the dataset
def delete(entity_name: str):
    def delete_item(item_name: str):
        if index_of_loaded_character is None:
            print(
                "No character is currently loaded! Please input 'load [character_name]' ."
            )
            return

        possible_items = []
        for item in character_data_list[index_of_loaded_character]["inventory"]:
            if item_name in str(item).lower():
                possible_items.append(item)

        handle_input(current_tab)
        if len(possible_items) == 0:
            print(f"No item with name '{item_name}' found.")
        elif len(possible_items) == 1:
            print(f"Are you sure that you want to delete '{possible_items[0]}'?")
            confirmation = input("confirm (y/n): ")
            if confirmation[0] == "y":
                character_data_list[index_of_loaded_character]["inventory"].pop(
                    possible_items[0]
                )
                save_character_data()
            inventory()
        else:
            print("No exact match. Possible items: ", end="")
            for item in possible_items:
                print(
                    item + (", " if (possible_items[-1] != item) else ""),
                    end="",
                )
            print()

    def delete_spell(spell_name: str):
        if index_of_loaded_character is None:
            print(
                "No character is currently loaded! Please input 'load [character_name]' ."
            )
            return

        possible_spells = []
        for spell in character_data_list[index_of_loaded_character]["spells"]:
            if spell_name in str(spell).lower():
                possible_spells.append(spell)

        handle_input(current_tab)
        if len(possible_spells) == 0:
            print(f"No item with name '{spell_name}' found.")
        elif len(possible_spells) == 1:
            print(f"Are you sure that you want to delete '{possible_spells[0]}'?")
            confirmation = input("confirm (y/n): ")
            if confirmation[0] == "y":
                character_data_list[index_of_loaded_character]["spells"].pop(
                    possible_spells[0]
                )
                save_character_data()
            spells()
        else:
            print("No exact match. Possible skills: ", end="")
            for spell in possible_spells:
                print(
                    spell + (", " if (possible_spells[-1] != spell) else ""),
                    end="",
                )
            print()

    def delete_skill(skill_name: str):
        if index_of_loaded_character is None:
            print(
                "No character is currently loaded! Please input 'load [character_name]' ."
            )
            return

        possible_skills = []
        for skill in character_data_list[index_of_loaded_character]["skills"]:
            if skill_name in str(skill).lower():
                str(possible_skills.append(skill)).lower()

        handle_input(current_tab)
        if len(possible_skills) == 0:
            print(f"No item with name '{skill_name}' found.")
        elif len(possible_skills) == 1:
            print(f"Are you sure that you want to delete '{possible_skills[0]}'?")
            confirmation = input("confirm (y/n): ")
            if confirmation[0] == "y":
                character_data_list[index_of_loaded_character]["skills"].pop(
                    possible_skills[0]
                )
                save_character_data()
            skills()
        else:
            print("No exact match. Possible skills: ", end="")
            for skill in possible_skills:
                print(
                    skill + (", " if (possible_skills[-1] != skill) else ""),
                    end="",
                )
            print()

    def delete_language(language_name: str):
        if index_of_loaded_character is None:
            print(
                "No character is currently loaded! Please input 'load [character_name]' ."
            )
            return

        possible_languages = []
        for language in character_data_list[index_of_loaded_character]["languages"]:
            if language_name in str(language).lower():
                possible_languages.append(language)

        handle_input(current_tab)
        if len(possible_languages) == 0:
            languages()
            print(f"No language '{language_name}' found.")
        elif len(possible_languages) == 1:
            print(f"Are you sure that you want to delete '{possible_languages[0]}'?")
            confirmation = input("confirm (y/n): ")
            if confirmation[0] == "y":
                character_data_list[index_of_loaded_character]["languages"].pop(
                    possible_languages[0]
                )
                save_character_data()
            languages()
        else:
            print("No exact match. Possible languages: ", end="")
            for language in possible_languages:
                print(
                    language + (", " if (possible_languages[-1] != language) else ""),
                    end="",
                )
            print()

    match current_tab:
        case "inventory":
            delete_item(entity_name)
        case "spells":
            delete_spell(entity_name)
        case "skills":
            delete_skill(entity_name)
        case "languages":
            delete_language(entity_name)
        case _:
            handle_input(current_tab)
            print("\nThere is nothing on this page you can delete.")


def main():
    extract_character_data()
    if len(character_data_list) == 1:
        load(character_data_list[0]["name"])
    else:
        stats()
    while True:
        handle_input()


main()
