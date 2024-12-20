"""Script containing a dictionary """
from data.classes_const import *

battle_dict = {0: Air_Elemental, 1: "obstacle", 2: Ancient_Behemoth, 3: Angel, 4: Archangel, 5: Archer,
               6: Arch_Devil, 7: Arch_Mage, 8: Ayssid, 9: Azure_Dragon, 10: "obstacle", 11: Basilisk,
               12: Battle_Dwarf, 13: Behemoth, 14: Beholder, 15: Black_Dragon, 16: Black_Knight, 17: Boar,
               18: Bone_Dragon, 19: "obstacle", 20: Cavalier, 21: Centaur, 22: Centaur_Captain, 23: Cerberus,
               24: Champion, 25: Chaos_Hydra, 26: Corsair, 27: Crew_Mate, 28: Crusader, 29: Crystal_Dragon,
               30: Cyclops, 31: Cyclops_King, 32: Demon, 33: Dendroid_Guard, 34: Dendroid_Soldier, 35: Devil,
               36: Diamond_Golem, 37: Dragon_Fly, 38: Dread_Knight, 39: Dwarf, 40: Earth_Elemental, 41: Efreeti,
               42: Efreet_Sultan, 43: Enchanter, 44: Energy_Elemental, 45: Evil_Eye, 46: Faerie_Dragon,
               47: Familiar, 48: Fangarm, 49: Firebird, 50: Fire_Elemental, 51: "obstacle",
               52: Genie, 53: Ghost_Dragon, 54: Giant, 55: Gnoll, 56: Gnoll_Marauder, 57: Goblin, 58: Gog,
               59: Gold_Dragon, 60: Gold_Golem, 61: Gorgon, 62: Grand_Elf, 63: Greater_Basilisk,
               64: Green_Dragon, 65: Gremlin, 66: Griffin, 67: Halberdier, 68: Halfling, 69: Harpy,
               70: Harpy_Hag, 71: Haspid, 72: Hell_Hound, 73: Hobgoblin, 74: Horned_Demon, 75: Hydra,
               76: Ice_Elemental, 77: Imp, 78: Infernal_Troglodyte, 79: Iron_Golem, 80: Leprechaun, 81: Lich,
               82: Lizardman, 83: Lizard_Warrior, 84: Mage, 85: Magic_Elemental, 86: Magma_Elemental, 87: Magog,
               88: Manticore, 89: Marksman, 90: Master_Genie, 91: Master_Gremlin, 92: Medusa, 93: Medusa_Queen,
               94: Mighty_Gorgon, 95: Minotaur, 96: Minotaur_King, 97: Monk, 98: Mummy, 99: Naga, 100: Naga_Queen,
               101: Nix, 102: Nix_Warrior, 103: Nomad, 104: Nymph, 105: Obsidian_Gargoyle, 106: Oceanid,
               107: Ogre, 108: Ogre_Mage, 109: Orc, 110: Orc_Chieftain, 111: Peasant, 112: Pegasus, 113: Phoenix,
               114: Pikeman, 115: Pirate, 116: Pit_Fiend, 117: Pit_Lord, 118: Pixie, 119: Power_Lich,
               120: Psychic_Elemental, 121: Red_Dragon, 122: Roc, 123: Rogue, 124: Royal_Griffin,
               125: Rust_Dragon, 126: Satyr, 127: Scorpicore, 128: Seaman, 129: Sea_Dog, 130: Sea_Serpent,
               131: Sea_Witch, 132: Serpent_Fly, 133: Sharpshooter, 134: Silver_Pegasus, 135: Skeleton,
               136: Skeleton_Warrior, 137: Sorceress, 138: Sprite, 139: Steel_Golem, 140: Stone_Gargoyle,
               141: Stone_Golem, 142: Stormbird, 143: Storm_Elemental, 144: Swordsman, 145: Thunderbird,
               146: Titan, 147: Troglodyte, 148: Troll, 149: Unicorn, 150: Vampire, 151: Vampire_Lord,
               152: Walking_Dead, 153: War_Unicorn, 154: Water_Elemental, 155: Wight, 156: Wolf_Raider,
               157: Wolf_Rider, 158: Wood_Elf, 159: Wraith, 160: Wyvern, 161: Wyvern_Monarch, 162: Zealot,
               163: Zombie, 164: "fosa", 165: "obstacle", 166: "terrain"}

# map_dict = {0: Abandoned_Mine, 1: Air_Elemental, 2: Alchemists_Lab, 3: Altar_of_Mana,
#             4: Altar_of_Sacrifice, 5: Ancient_Behemoth, 6: Ancient_Lamp, 7: Angel,
#             8: Garrison, 9: Archangel, 10: Arch_Devil, 11: Archer, 12: Arch_Mage,
#             13: Arena, 14: Artifact, 15: Admirals_Hat, 16: Ambassadors_Sash,
#             17: Amulet_of_the_Undertaker, 18: Angelic_Alliance,
#             19: Angel_Feather_Arrows, 20: Angel_Wings, 21: Armageddons_Blade,
#             22: Armor_of_the_Damned, 23: Armor_of_Wonder, 24: Arms_of_Legion,
#             25: Badge_of_Courage, 26: Bird_of_Perception,
#             27: Blackshard_of_the_Dead_Knight, 28: Boots_of_Levitation,
#             29: Boots_of_Polarity, 30: Boots_of_Speed,
#             31: Bowstring_of_the_Unicorns_Mane, 32: Bow_of_Elven_Cherrywood,
#             33: Bow_of_the_Sharpshooter, 34: Breastplate_of_Brimstone,
#             35: Breastplate_of_Petrified_Wood, 36: Buckler_of_the_Gnoll_King,
#             37: Cape_of_Conjuring, 38: Cape_of_Silence, 39: Cape_of_Velocity,
#             40: Cards_of_Prophecy, 41: Celestial_Necklace_of_Bliss,
#             42: Centaurs_Axe, 43: Charm_of_Eclipse, 44: Charm_of_Mana,
#             45: Cloak_of_the_Undead_King, 46: Clover_of_Fortune,
#             47: Collar_of_Conjuring, 48: Cornucopia, 49: Crest_of_Valor,
#             50: Crown_of_Dragontooth, 51: Crown_of_the_Five_Seas,
#             52: Crown_of_the_Supreme_Magi, 53: Dead_Mans_Boots,
#             54: Demons_Horseshoe, 55: Diplomats_Cloak, 56: Diplomats_Ring,
#             57: Dragonbone_Greaves, 58: Dragon_Scale_Armor,
#             59: Dragon_Scale_Shield, 60: Dragon_Wing_Tabard, 61: Elixir_of_Life,
#             62: Emblem_of_Cognizance, 63: Endless_Bag_of_Gold,
#             64: Endless_Purse_of_Gold, 65: Endless_Sack_of_Gold,
#             66: Equestrians_Gloves, 67: Everflowing_Crystal_Cloak,
#             68: Everpouring_Vial_of_Mercury, 69: Eversmoking_Ring_of_Sulfur,
#             70: Garniture_of_Interference, 71: Glyph_of_Gallantry,
#             72: Golden_Bow, 73: Golden_Goose, 74: Greater_Gnolls_Flail,
#             75: Head_of_Legion, 76: Hellstorm_Helmet, 77: Helm_of_Chaos,
#             78: Helm_of_Heavenly_Enlightenment, 79: Helm_of_the_Alabaster_Unicorn,
#             80: Hideous_Mask, 81: Horn_of_the_Abyss,
#             82: Hourglass_of_the_Evil_Hour, 83: Inexhaustible_Cart_of_Lumber,
#             84: Inexhaustible_Cart_of_Ore, 85: Ironfist_of_the_Ogre,
#             86: Ladybird_of_Luck, 87: Legs_of_Legion,
#             88: Lions_Shield_of_Courage, 89: Loins_of_Legion,
#             90: Mystic_Orb_of_Mana, 91: Necklace_of_Dragonteeth,
#             92: Necklace_of_Ocean_Guidance, 93: Necklace_of_Swiftness,
#             94: Ogres_Club_of_Havoc, 95: Orb_of_Driving_Rain,
#             96: Orb_of_Inhibition, 97: Orb_of_Silt, 98: Orb_of_Tempestuous_Fire,
#             99: Orb_of_the_Firmament, 100: Orb_of_Vulnerability,
#             101: Pendant_of_Courage, 102: Pendant_of_Death,
#             103: Pendant_of_Dispassion, 104: Pendant_of_Downfall,
#             105: Pendant_of_Free_Will, 106: Pendant_of_Holiness,
#             107: Pendant_of_Life, 108: Pendant_of_Negativity,
#             109: Pendant_of_Reflection, 110: Pendant_of_Second_Sight,
#             111: Pendant_of_Total_Recall, 112: Plate_of_Dying_Light,
#             113: Power_of_the_Dragon_Father, 114: Quiet_Eye_of_the_Dragon,
#             115: Recanters_Cloak, 116: Red_Dragon_Flame_Tongue, 117: Rib_Cage,
#             118: Ring_of_Conjuring, 119: Ring_of_Infinite_Gems,
#             120: Ring_of_Life, 121: Ring_of_Oblivion, 122: Ring_of_Suppression,
#             123: Ring_of_the_Magi, 124: Ring_of_the_Wayfarer,
#             125: Ring_of_Vitality, 126: Royal_Armor_of_Nix,
#             127: Runes_of_Imminency, 128: Sandals_of_the_Saint,
#             129: Scales_of_the_Greater_Basilisk, 130: Seal_of_Sunset,
#             131: Sea_Captains_Hat, 132: Sentinels_Shield, 133: Shackles_of_War,
#             134: Shamans_Puppet, 135: Shield_of_Naval_Glory,
#             136: Shield_of_the_Damned, 137: Shield_of_the_Dwarven_Lords,
#             138: Shield_of_the_Yawning_Dead, 139: Skull_Helmet, 140: Speculum,
#             141: Spellbinders_Hat, 142: Sphere_of_Permanence,
#             143: Spirit_of_Oppression, 144: Spyglass, 145: Statesmans_Medal,
#             146: Statue_of_Legion, 147: Still_Eye_of_the_Dragon,
#             148: Stoic_Watchman, 149: Surcoat_of_Counterpoise,
#             150: Sword_of_Hellfire, 151: Sword_of_Judgement,
#             152: Talisman_of_Mana, 153: Targ_of_the_Rampaging_Ogre,
#             154: Thunder_Helmet, 155: Titans_Cuirass, 156: Titans_Gladius,
#             157: Titans_Thunder, 158: Tome_of_Air, 159: Tome_of_Earth,
#             160: Tome_of_Fire, 161: Tome_of_Water, 162: Torso_of_Legion,
#             163: Trident_of_Dominion, 164: Tunic_of_the_Cyclops_King,
#             165: Vampires_Cowl, 166: Vial_of_Dragon_Blood,
#             167: Vial_of_Lifeblood, 168: Wayfarers_Boots,
#             169: Wizards_Well, 170: Azure_Dragon, 171: Basilisk, 172: Battle_Dwarf,
#             173: Behemoth, 174: Beholder, 175: Beholders_Sanctuary, 176: Black_Dragon,
#             177: Black_Knight, 178: Black_Market, 179: Black_Tower, 180: Boar, 181: Bone_Dragon,
#             182: Border_Gate, 183: Border_Guard, 184: Buoy, 185: Campfire, 186: Cannon_Yard,
#             187: Cartographer, 188: Cavalier, 189: Centaur, 190: Centaur_Captain, 191: Cerberus,
#             192: Champion, 193: Chaos_Hydra, 194: Churchyard, 195: Clover_Field,
#             196: Colosseum_of_the_Magi, 197: Corpse, 198: Cover_of_Darkness, 199: Cracked_Ice,
#             200: Crusader, 201: Crypt, 202: Crystal, 203: Crystal_Cavern, 204: Crystal_Dragon,
#             205: Cursed_Ground, 206: Cyclops, 207: Cyclops_King, 208: Cyclops_Stockpile, 209: Demon,
#             210: Dendroid_Guard, 211: Dendroid_Soldier, 212: Den_of_Thieves, 213: Derelict_Ship,
#             214: Derrick, 215: Devil, 216: Diamond_Golem, 217: Dirt, 218: Dragon_Fly,
#             219: Dragon_Fly_Hive, 220: Dragon_Utopia, 221: Dread_Knight, 222: Dunes, 223: Dwarf,
#             224: Dwarven_Treasury, 225: Earth_Elemental, 226: Efreeti, 227: Efreet_Sultan,
#             228: Enchanter, 229: Energy_Elemental, 230: Evil_Eye, 231: Evil_Fog,
#             232: Experimental_Shop, 233: "Eye_of_the_Magi", 234: Faerie_Dragon, 235: Faerie_Ring,
#             236: Familiar, 237: Favorable_Winds, 238: Fields_of_Glory, 239: Fiery_Fields,
#             240: Firebird, 241: Fire_Elemental, 242: Flotsam, 243: Fountain_of_Fortune,
#             244: Fountain_of_Youth, 245: Freelancers_Guild, 246: Garden_of_Revelation, 247: Garrison,
#             248: Gazebo, 249: Gems, 250: Gem_Pond, 251: Genie, 252: Ghost_Dragon, 253: Giant,
#             254: Gnoll, 255: Gnoll_Marauder, 256: Goblin, 257: Gog, 258: Gold_Dragon,
#             259: Gold_Golem, 260: Gold_Mine, 261: Gorgon, 262: Grand_Elf, 263: Grass,
#             264: Grave, 265: Greater_Basilisk, 266: Green_Dragon, 267: Gremlin, 268: Griffin,
#             269: Griffin_Conservatory, 270: Halberdier, 271: Halfling, 272: Harpy, 273: Harpy_Hag,
#             274: Hell_Hound, 275: Hermits_Shack, 276: Hero, 277: Highlands, 278: Hill_Fort,
#             279: Hobgoblin, 280: Holy_Ground, 281: Horned_Demon, 282: "Hut_of_the_Magi", 283: Hydra,
#             284: Ice_Elemental, 285: Idol_of_Fortune, 286: Imp, 287: Imp_Cache,
#             288: Infernal_Troglodyte, 289: Iron_Golem, 290: Ivory_Tower, 291: Jetsam, 292: Junkman,
#             293: Keymasters_Tent, 294: Lava, 295: "Lean_to", 296: Learning_Stone,
#             297: Library_of_Enlightenment, 298: Lich, 299: Lighthouse, 300: Lizardman,
#             301: Lizard_Warrior, 302: Lucid_Pools, 303: Mage, 304: Magic_Clouds,
#             305: Magic_Elemental, 306: Magic_Plains, 307: Magic_Spring, 308: Magic_Well,
#             309: Magma_Elemental, 310: Magog, 311: Mansion, 312: Manticore, 313: Obstacle_terr,
#             314: Marksman, 315: Marletto_Tower, 316: Master_Genie, 317: Master_Gremlin, 318: Medusa,
#             319: Medusa_Queen, 320: Medusa_Stores, 321: Mercenary_Camp, 322: Mercury, 323: Mermaids,
#             324: Mighty_Gorgon, 325: Mineral_Spring, 326: Minotaur, 327: Minotaur_King, 328: Monk,
#             329: Monolith_One_Way_Entrance, 330: Monolith_One_Way_Exit, 331: Monolith_Two_Way,
#             332: Mummy, 333: Mystical_Garden, 334: Naga, 335: Naga_Bank, 336: Naga_Queen,
#             337: Nomad, 338: Oasis, 339: Obelisk, 340: Observation_Tower, 341: Observatory,
#             342: Obsidian_Gargoyle, 343: Obstacle_terr, 344: Ocean_Bottle, 345: Ogre, 346: Ogre_Mage,
#             347: Orc, 348: Orc_Chieftain, 349: Ore, 350: Ore_Pit, 351: Pandoras_Box,
#             352: Pandoras_Box, 353: Peasant, 354: Pegasus, 355: Phoenix, 356: Pikeman,
#             357: Pillar_of_Fire, 358: Pirate_Cavern, 359: Pit_Fiend, 360: Pit_Lord, 361: Pixie,
#             362: Portal_One_Way_Entrance, 363: Portal_One_Way_Exit, 364: Power_Lich, 365: Prison,
#             366: Prison, 367: Prison, 368: Prospector, 369: Psychic_Elemental, 370: "Pyramid",
#             371: Quest_Guard, 372: Rally_Flag, 373: Redwood_Observatory, 374: Red_Dragon,
#             375: Red_Tower, 376: Portal_Two_Way, 377: Refugee_Camp,
#             378: Crystal, 379: Gems, 380: Gold, 381: Mercury,
#             382: Ore, 383: Sulfur, 384: Wood, 385: Dirt_Road, 386: Roc,
#             387: Rock, 388: Rockland, 389: Rogue, 390: Rough, 391: Royal_Griffin, 392: Ruins,
#             393: Rust_Dragon, 394: Sanctuary, 395: Sand, 396: Sawmill, 397: Scholar,
#             398: School_of_Magic, 399: School_of_Magic, 400: School_of_War, 401: Scorpicore,
#             402: Seafaring_Academy, 403: Sea_Barrel, 404: Sea_Chest, 405: Seers_Hut,
#             406: Seers_Hut, 407: Serpent_Fly, 408: Sharpshooter, 409: Shipwreck,
#             410: Shipwreck, 411: Shipwreck_Survivor, 412: Shipyard,
#             413: Shrine_Of_Magic_Gesture, 414: Shrine_Of_Magic_Gesture,
#             415: Shrine_Of_Magic_Incantation, 416: Shrine_Of_Magic_Incantation,
#             417: Shrine_Of_Magic_Mystery, 418: Shrine_Of_Magic_Mystery,
#             419: Shrine_Of_Magic_Thought, 420: Shrine_Of_Magic_Thought, 421: "Sign",
#             422: Silver_Pegasus, 423: "Sirens", 424: Skeleton, 425: Skeleton_Transformer,
#             426: Skeleton_Warrior, 427: Snow, 428: "Spell_Scroll", 429: Spit, 430: Sprite,
#             431: Stables, 432: "Star_Axis", 433: Stone_Gargoyle, 434: Stone_Golem,
#             435: Storm_Elemental, 436: Subterranean, 437: Subterranean_Gate, 438: Sulfur,
#             439: Sulfur_Dune, 440: Swamp, 441: Swan_Pond, 442: Swordsman, 443: Tavern,
#             444: Tavern, 445: Temple, 446: Temple_Of_Loyalty, 447: Temple_of_the_Sea,
#             448: Thunderbird, 449: Titan, 450: "Town", 451: Town_Gate,
#             452: "Trading_Post", 453: "Trailblazer", 454: Treasure_Chest,
#             455: Tree_Of_Knowledge, 456: Troglodyte, 457: Troll, 458: Unicorn,
#             459: "University", 460: Vampire, 461: Vampire_Lord, 462: Vial_Of_Mana,
#             463: Portal_Two_Way, 464: Obstacle_terr, 465: Wagon, 466: Wagon, 467: Walking_Dead,
#             468: Warehouse_of_Crystal, 469: Warehouse_of_Gem, 470: Warehouse_of_Gold,
#             471: Warehouse_of_Mercury, 472: Warehouse_of_Ore, 473: Warehouse_of_Sulfur,
#             474: Warehouse_of_Wood, 475: Warlocks_Lab, 476: "Warriors_Tomb",
#             477: "War_Machine_Factory", 478: War_Unicorn, 479: Wasteland, 480: Water,
#             481: Watering_Hole, 482: Watering_Place, 483: Water_Elemental, 484: Water_Wheel,
#             485: Whirlpool, 486: Wight, 487: Windmill, 488: Witch_Hut, 489: Wolf_Raider,
#             490: Wolf_Raider_Picket, 491: Wolf_Rider, 492: Wood, 493: Wood_Elf, 494: Wraith,
#             495: Wyvern, 496: Wyvern_Monarch, 497: Zealot, 498: Zombie, 499: Castle,
#             500: Castle, 501: Conflux, 502: Conflux, 503: Cove, 504: Cove, 505: Dungeon, 506: Dungeon, 507: Fortress,
#             508: Fortress, 509: Inferno, 510: Inferno, 511: Necropolis, 512: Necropolis,
#             513: Rampart, 514: Rampart, 515: Stronghold, 516: Stronghold, 517: Tower, 518: Tower}


