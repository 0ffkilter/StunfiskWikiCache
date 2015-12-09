from aliases import *
from read_pokedex_json import *
from var_keys import *
import difflib
import pickle
import os

d = difflib.Differ();

def get_pokemon(pokemon):
    pokemon = re.sub(r"\s+$", "", pokemon) # remove trailing whitespace
    if pokemon in ALIAS_POKEMON:
        pokemon = ALIAS_POKEMON[pokemon]
    if not pokemon in NAME_TO_NUMBER:
        return None
    dex_index = re.sub(r"[ .']","", pokemon)
    pokedex_index = re.sub("-", "", dex_index)
    species = POKEDEX[pokedex_index]["species"]
    return species

def diff(page1, page2):
    return d.compare(page1, page2)

def areEqual(compare):
    return sum(1 for _ in compare) == 0

def save_obj(obj, name ):
    writepath = 'obj/' + name + '.pkl'
    with open(writepath, "wb+") as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def update_page(page_name):
    dict_obj = load_obj("poke_dict")
    dict_obj[page_name] = p.get_wiki_page("stunfisk", page_name).content_md
    save_obj(dict_obj, "poke_dict")

def check_pages():
    pokemon = []
    revisions = p.get_wiki_page("stunfisk", "revisions")
    for page in revisions.children:
        if get_pokemon(page["page"]) is not None:
            pokemon.append(page["page"])

    previous_dict = load_obj("poke_dict")
    change_dict = {}

    for poke in pokemon:
        species = get_pokemon(poke)
        if species is not None:
            page = p.get_wiki_page("stunfisk", poke)
            if  not species in previous_dict:
                previous_dict[species] = page.content_md
            else:
                res = diff(previous_dict[species].splitlines(True), page.content_md.splitlines(True))
                if not areEqual(res):
                    res = diff(previous_dict[species].splitlines(True), page.content_md.splitlines(True))
                    change_dict[species] = "\n".join(res)
                    previous_dict[species] = page.content_md

    return change_dict

def update_dict():
    pages = p.get_wiki_pages("stunfisk")
    p_dict = {}

    for page in pages:
        species = get_pokemon(page.page.encode("ascii"))
        if species is not None:
            print(species)
            p_dict[species] = page.content_md

    save_obj(p_dict, "poke_dict");
    change_dict = {}


p = praw.Reddit(user_agent = "Stunfisk wiki cache by /u/0ffkilter")
