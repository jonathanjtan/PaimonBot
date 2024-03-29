# >database.py KEKW

characters_element = {
    "albedo": "geo",
    "amber": "pyro",
    "barbara" : "hydro",
    "beidou" : "electro",
    "bennett" : "pyro",
    "chongyun" : "cryo",
    "diluc" : "pyro",
    "diona" : "cryo",
    "fischl" : "electro",
    "ganyu" : "cryo",
    "jean" : "ameno",
    "kaeya" : "cryo",
    "keqing" : "electro",
    "klee" : "pyro",
    "lisa" : "electro",
    "mona" : "hydro",
    "ningguang" : "geo",
    "noelle" : "geo",
    "qiqi" : "cryo",
    "razor" : "electro",
    "sucrose" : "ameno",
    "tartaglia" : "hydro",
    "traveler" : "traveler", # Special case? Apparently we're getting characters with multiple elements soon
    "venti" : "ameno",
    "xiangling" : "pyro",
    "xinyan" : "pyro",
    "xingqiu" : "hydro",
    "zhongli" : "geo"
}

# TODO: update when dendro drops
element_materials = {
    "ameno" : {"vayuda turquoise", "hurricane seed"},
    "dendro" : {"placeholder 1", "placeholder 2"},
    "electro" : {"vajrada amethyst", "lightning prism"},
    "pyro" : {"agnidus agate", "everflame seed"},
    "geo" : {"prithiva topaz", "basalt pillar"},
    "cryo": {"shivada jade", "hoarfrost core"},
    "hydro" : {"varunada lazurite", "cleansing heart"},
    "traveler" : {"brilliant diamond"}
}

# characters to their level ascension materials
characters_level = {
    "albedo": {"cecilia", "scroll"},
    "amber": {"small lamp grass", "arrowhead"},
    "barbara" : {"philanemo mushroom", "scroll"},
    "beidou" : {"noctilucous jade", "hoarder"},
    "bennett" : {"windwheel aster", "hoarder"},
    "chongyun" : {"cor lapis", "mask"},
    "diluc" : {"small lamp grass", "fatui"},
    "diona" : {"calla lily", "arrowhead"},
    "fischl" : {"small lamp grass", "arrowhead"},
    "jean" : {"dandelion seed", "mask"},
    "kaeya" : {"calla lily", "hoarder"},
    "keqing" : {"cor lapis", "nectar"},
    "klee" : {"philanemo mushroom", "scroll"},
    "ganyu" : {"nectar", "qingxin"},
    "lisa" : {"valberry", "slime"},
    "mona" : {"philanemo mushroom", "nectar"},
    "ningguang" : {"glaze lily", "fatui"},
    "noelle" : {"valberry", "mask"},
    "qiqi" : {"violetgrass", "scroll"},
    "razor" : {"wolfhook", "mask"},
    "sucrose" : {"windwheel aster", "nectar"},
    "tartaglia" : {"starconch", "fatui"},
    "traveler" : {"windwheel aster", "mask"},
    "venti" : {"cecilia", "slime"},
    "xiangling" : {"jueyun chili", "slime"},
    "xingqiu" : {"silk flower", "mask"},
    "xinyan" : {"violetgrass", "hoarder"},
    "zhongli" : {"cor lapis", "slime"}
}
# add the boss drops to character level up material
for character, level in characters_level.items():
    element = characters_element[character]
    level.update(element_materials[element])

# fatui = knife
commons = {
    "slime", 
    "mask", 
    "arrowhead", 
    "scroll", 
    "horn", 
    "leyline", 
    "chaos", 
    "mist", 
    "knife", 
    "fatui", 
    "hoarder", 
    "bone", 
    "nectar"
}

books = {"ballad", "diligence", "freedom", "gold", "prosperity", "resistance"}

# characters to their talent ascension materials
characters_talent = {
    "albedo": {"ballad"},
    "amber": {"freedom"},
    "barbara" : {"freedom"},
    "beidou" : {"gold"},
    "bennett" : {"resistance"},
    "chongyun" : {"diligence"},
    "diluc" : {"resistance"},
    "diona" : {"freedom"},
    "fischl" : {"ballad"},
    "ganyu" : {"diligence"},
    "jean" : {"resistance"},
    "kaeya" : {"ballad"},
    "keqing" : {"prosperity"},
    "klee" : {"freedom"},
    "lisa" : {"ballad"},
    "mona" : {"resistance"},
    "ningguang" : {"prosperity"},
    "noelle" : {"resistance"},
    "qiqi" : {"prosperity"},
    "razor" : {"resistance"},
    "sucrose" : {"freedom"},
    "tartaglia" : {"freedom"},
    "traveler" : {"freedom"},
    "venti" : {"ballad"},
    "xiangling" : {"diligence"},
    "xingqiu" : {"gold"},
    "xinyan" : {"gold"},
    "zhongli" : {"gold"}
}
# add the commons to talent level up material
for character, talent in characters_talent.items():
    talent.update(characters_level[character].intersection(commons))

# weapon strings
decarabian = "decarabian"
wolf = "wolf"
gladiator = "gladiator"
guyun = "guyun"
elixir = "elixir"
aerosiderite = "aerosiderite"

weapon_ascension = {decarabian, wolf, gladiator, guyun, elixir, aerosiderite}

# TODO: add commons to weapon_materials
sword = {
    "cool steel" : {decarabian},
    "dark iron sword" : {guyun},
    "favonius sword" : {decarabian},
    "fillet blade" : {elixir},
    "harbinger of doom" : {wolf},
    "iron sting" : {aerosiderite},
    "lions roar" : {guyun},
    "prototype rancour" : {elixir},
    "sacrificial sword" : {gladiator},
    "skyrider sword" : {aerosiderite},
    "skyward blade" : {wolf},
    "sword of descension"  : {wolf},
    "the black sword" : {wolf},
    "the flute" : {wolf},
    "travelers handy sword" : {gladiator}
}

catalyst = {
    "emerald orb" : {guyun},
    "eye of perception" : {elixir},
    "favonius codex" : {decarabian},
    "lost prayer to the sacred winds" : {gladiator},
    "magic guide" : {decarabian},
    "mappa mare" : {aerosiderite},
    "otherworldly story" : {gladiator},
    "prototype malice" : {elixir},
    "royal grimore" : {aerosiderite},
    "sacrificial fragments" : {gladiator},
    "solar pearl" : {guyun},
    "the widsith" : {wolf},
    "thrilling tales of dragon slayers" : {wolf},
    "twin nephrite" : {elixir},
    "wine and song" : {wolf}
}

claymore = {
    "bloodtainted greatsword" : {wolf},
    "debate club" : {elixir},
    "favonius greatsword" : {gladiator},
    "ferrous shadow" : {decarabian},
    "prototype aminus" : {aerosiderite},
    "rainslasher" : {elixir},
    "royal greatsword" : {gladiator},
    "sacrificial greatsword" : {wolf},
    "serpent spine" : {aerosiderite},
    "skyrider greatsword" : {aerosiderite},
    "the bell" : {decarabian},
    "white iron greatsword" : {gladiator},
    "whiteblind" : {guyun},
    "wolfs gravestone" : {gladiator},
}

bow = {
    "alley hunter" : {wolf},
    "amos bow" : {gladiator},
    "blackcliff warbow" : {guyun},
    "compound bow" : {aerosiderite},
    "favonius warbow" : {gladiator},
    "messenger" : {elixir},
    "prototype crescent" : {elixir},
    "raven bow" : {decarabian},
    "recurve bow" : {gladiator},
    "rust" : {guyun},
    "sacrificial bow" : {wolf},
    "sharpshooters oath" : {wolf},
    "skyward harp" : {wolf},
    "slingshot" : {guyun},
    "stringless" : {decarabian},
    "the viridescent hunt" : {decarabian},
}

polearm = {
    "black tassel" : {aerosiderite},
    "crescent pike" : {guyun},
    "dragons bane" : {elixir},
    "favonius lance" : {gladiator},
    "halberd" : {elixir},
    "primordial jade winged spear" : {guyun},
    "prototype grudge" : {aerosiderite},
    "skyward spine" : {gladiator},
    "white tassel" : {guyun}
}

sword = {
    "cool steel" : {decarabian},
    "dark iron sword" : {guyun},
    "favonius sword" : {decarabian},
    "fillet blade" : {elixir},
    "harbinger of doom" : {wolf},
    "iron sting" : {aerosiderite},
    "lions roar" : {guyun},
    "prototype rancour" : {elixir},
    "sacrificial sword" : {gladiator},
    "skyrider sword" : {aerosiderite},
    "skyward blade" : {wolf},
    "sword of descension"  : {wolf},
    "the black sword" : {wolf},
    "the flute" : {wolf},
    "travelers handy sword" : {gladiator}
}

weapons_materials = {**catalyst, **claymore, **bow, **polearm, **sword}

# materials : (condition, how)
materials = {
    # boss drops
    "vayuda turquoise" : (["Anytime"], "Ameno Hypostasis"),
    "hurricane seed" : (["Anytime"], "Ameno Hypostasis"),
    "agnidus agate" : (["Anytime"], "Pyro Regisvine"),
    "everflame seed" : (["Anytime"], "Pyro Regisvine"),
    "vajrada amethyst" : (["Anytime"], "Electro Hypostasis"),
    "lightning prism" : (["Anytime"], "Electro Hypostasis"),
    "prithiva topaz" : (["Anytime"], "Geo Hypostasis"),
    "basalt pillar" : (["Anytime"], "Geo Hypostasis"),
    "shivada jade" : (["Anytime"], "Cryo Regisvine"),
    "hoarfrost core" : (["Anytime"], "Cryo Regisvine"),
    "varunada lazurite" : (["Anytime"], "Oceanid"), 
    "cleansing heart" : (["Anytime"], "Oceanid"),

    # TODO: commons
    # TODO: specialties

    # books
    "ballad" : (["Wednesday", "Saturday", "Sunday"], "Forsaken Rift"),
    "diligence" : (["Tuesday", "Friday", "Sunday"], "Taishan Mansion"),
    "freedom" : (["Monday", "Thursday", "Sunday"], "Forsaken Rift"),
    "gold" : (["Wednesday", "Saturday", "Sunday"], "Taishan Mansion"),
    "prosperity" : (["Monday", "Thursday", "Sunday"], "Taishan Mansion"),
    "resistance" : (["Tuesday", "Friday", "Sunday"], "Forsaken Rift"),

    # weapon ascension
    decarabian : (["Monday", "Thursday", "Sunday"], "Cecilia Garden"),
    wolf : (["Tuesday", "Friday", "Sunday"], "Cecilia Garden"),
    gladiator : (["Wednesday", "Saturday", "Sunday"], "Cecilia Garden"),
    guyun : (["Monday", "Thursday", "Sunday"], "Lianshan Formula"),
    elixir : (["Tuesday", "Friday", "Sunday"], "Lianshan Formula"),
    aerosiderite : (["Wednesday", "Saturday", "Sunday"], "Lianshan Formula"),
}
