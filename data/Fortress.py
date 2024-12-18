"""Script containing Fortress city class"""

from data.city import City
from data.habitats_cities import *
from data.city_buildings import *
from data.hero import Hero
from copy import deepcopy
from GUI_handling import TownGUI as GUI
from difflib import get_close_matches
import GUI_handling.AdventureGUI
import image_processing.detecting_window
import image_processing.ok_detection
import time

class Fortress(City):
    def __init__(self,
                 name: str = "Fortress",
                 mage_guild: MageGuild = Fortress_Mage_Guild,
                 city_hall: CityHall = Fortress_City_Hall,
                 fort: Fort = Fortress_Fort,
                 marketplace: Marketplace = Fortress_Marketplace,
                 tavern: Tavern = Fortress_Tavern,
                 resource_silo: ResourceSilo = Fortress_Rescource_Silo,
                 blacksmith: Building = Fortress_Blacksmith,
                 t1: Habitat = Gnoll_Hut,
                 t2: Habitat = Lizard_Den,
                 t3: Habitat = Serpent_Fly_Hive,
                 t4: Habitat = Basilisk_Pit,
                 t5: Habitat = Gorgon_Lair,
                 t6: Habitat = Wyvern_Nest,
                 t7: Habitat = Hydra_Pond,
                 obelisk: Building = Blood_Obelisk,
                 cage: Building = Cage_of_Warlords,
                 captain: Building = Captains_Quarters,
                 glyphs: Building = Glyphs_of_Fear,
                 graal: bool = False,
                 upper_hero: Hero = Hero(0, "", "", 0, 0, 0, 0),
                 lower_hero: Hero = Hero(0, "", "", 0, 0, 0, 0),
                 owned_by: str = 'neutral'):
        """
        A class representing Fortress city

        :param name: Name of the given city
        :param mage_guild: Mage guild object
        :param city_hall: City hall object
        :param fort: Fort object
        :param marketplace: Marketplace object
        :param tavern: Tavern object
        :param resource_silo: Resource silo object
        :param blacksmith: Blacksmith object
        :param t1: 1st level habitat - Gnoll Hut
        :param t2: 2nd level habitat - Lizard Den
        :param t3: 3rd level habitat - Serpent Fly Hive
        :param t4: 4th level habitat - Basilisk Pit
        :param t5: 5th level habitat - Gorgon Lair
        :param t6: 6th level habitat - Wyvern Nest
        :param t7: 7th level habitat - Hydra Pond
        :param obelisk: Blood Obelisk object
        :param cage: Cage of Warlords object
        :param captain: Captain Quarters object
        :param glyphs: Glyphs of Fear
        :param graal: Boolean True - graal, False - no graal
        :param upper_hero: Hero object that is present in the higher row of the city slot bar
        :param lower_hero: Hero object that is present in the lower row of the city slot bar
        :param owned_by: Which player owns the building
        """
        super().__init__(mage_guild, fort, city_hall, tavern, marketplace, resource_silo, blacksmith, graal, upper_hero,
                         lower_hero, owned_by)
        self.name = name
        self.t1_generator_lvl = deepcopy(t1)
        self.t2_generator_lvl = deepcopy(t2)
        self.t3_generator_lvl = deepcopy(t3)
        self.t4_generator_lvl = deepcopy(t4)
        self.t5_generator_lvl = deepcopy(t5)
        self.t6_generator_lvl = deepcopy(t6)
        self.t7_generator_lvl = deepcopy(t7)
        self.blood_obelisk = obelisk
        self.cage_of_warlords = cage
        self.captains_quarters = captain
        self.glyphs_of_fear = glyphs

    def action(self, player, hero: Hero, okay=0):
        """
        Responsible for buying units

        :param okay: Okay parameter  -> which okay window popped up
        :param player: player object
        :param hero: Hero object
        """
        if self not in player.cities:
            image_processing.detecting_window.execute_detecting(hero)
            player.cities.append(self)
            self.need_read = True

        detected = 1
        while detected == 1:
            detected = image_processing.ok_detection.check_ok()
            if detected == 1:
                GUI_handling.AdventureGUI.accept_offer()

        upgrades = [False, False, False, False, False, False, False]

        amount1 = 0
        amount2 = 0
        amount3 = 0
        amount4 = 0
        amount5 = 0
        amount6 = 0
        amount7 = 0
        unit1 = 0
        unit2 = 0
        unit3 = 0
        unit4 = 0
        unit5 = 0
        unit6 = 0
        unit7 = 0
        upgraded = False
        if self.t7_generator_lvl.habitat_lvl == 1:
            cost = 0
            amount = 0
            while player.gold > cost and amount <= self.t7_generator_lvl.unit_ready:  # only gold because most units cost only gold
                amount += 1
                cost += self.t7_generator_lvl.unit_cost.gold
            player.gold -= cost
            amount7 = amount
            unit7 = self.t7_generator_lvl.unit_type
        elif self.t7_generator_lvl.habitat_lvl == 2:
            for i, x in enumerate(hero.slots.slots):
                if x.unit == self.t7_generator_lvl.unit_type and player.gold > x.amount * (
                        self.t7_generator_lvl.unit_cost_up.gold - self.t7_generator_lvl.unit_cost.gold):
                    GUI.upgrade_unit(9 + i)
                    upgraded = True
                    player.gold -= x.amount * (
                                self.t7_generator_lvl.unit_cost_up.gold - self.t7_generator_lvl.unit_cost.gold)
            cost = 0
            amount = 0
            while player.gold > cost and amount <= self.t7_generator_lvl.unit_ready:  # only gold because most units cost only gold
                amount += 1
                cost += self.t7_generator_lvl.unit_cost_up.gold
            player.gold -= cost
            amount7 = amount
            unit7 = self.t7_generator_lvl.unit_type_up
            upgrades[6] = True
        if self.t6_generator_lvl.habitat_lvl == 1:
            cost = 0
            amount = 0
            while player.gold > cost and amount <= self.t6_generator_lvl.unit_ready:  # only gold because most units cost only gold
                amount += 1
                cost += self.t6_generator_lvl.unit_cost.gold
            player.gold -= cost
            amount6 = amount
            unit6 = self.t6_generator_lvl.unit_type
        elif self.t6_generator_lvl.habitat_lvl == 2:
            for i, x in enumerate(hero.slots.slots):
                if x.unit == self.t6_generator_lvl.unit_type and player.gold > x.amount * (
                        self.t6_generator_lvl.unit_cost_up.gold - self.t6_generator_lvl.unit_cost.gold):
                    GUI.upgrade_unit(9 + i)
                    upgraded = True
                    player.gold -= x.amount * (
                                self.t6_generator_lvl.unit_cost_up.gold - self.t6_generator_lvl.unit_cost.gold)
            cost = 0
            amount = 0
            while player.gold > cost and amount <= self.t6_generator_lvl.unit_ready:  # only gold because most units cost only gold
                amount += 1
                cost += self.t6_generator_lvl.unit_cost_up.gold
            player.gold -= cost
            amount6 = amount
            unit6 = self.t6_generator_lvl.unit_type_up
            upgrades[5] = True
        if self.t5_generator_lvl.habitat_lvl == 1:
            cost = 0
            amount = 0
            while player.gold > cost and amount <= self.t5_generator_lvl.unit_ready:  # only gold because most units cost only gold
                amount += 1
                cost += self.t5_generator_lvl.unit_cost.gold
            player.gold -= cost
            amount5 = amount
            unit5 = self.t5_generator_lvl.unit_type
        elif self.t5_generator_lvl.habitat_lvl == 2:
            for i, x in enumerate(hero.slots.slots):
                if x.unit == self.t5_generator_lvl.unit_type and player.gold > x.amount * (
                        self.t5_generator_lvl.unit_cost_up.gold - self.t5_generator_lvl.unit_cost.gold):
                    GUI.upgrade_unit(9 + i)
                    upgraded = True
                    player.gold -= x.amount * (
                                self.t5_generator_lvl.unit_cost_up.gold - self.t5_generator_lvl.unit_cost.gold)
            cost = 0
            amount = 0
            while player.gold > cost and amount <= self.t5_generator_lvl.unit_ready:  # only gold because most units cost only gold
                amount += 1
                cost += self.t5_generator_lvl.unit_cost_up.gold
            player.gold -= cost
            amount5 = amount
            unit5 = self.t5_generator_lvl.unit_type_up
            upgrades[4] = True
        if self.t4_generator_lvl.habitat_lvl == 1:
            cost = 0
            amount = 0
            while player.gold > cost and amount <= self.t4_generator_lvl.unit_ready:  # only gold because most units cost only gold
                amount += 1
                cost += self.t4_generator_lvl.unit_cost.gold
            player.gold -= cost
            amount4 = amount
            unit4 = self.t4_generator_lvl.unit_type
        elif self.t4_generator_lvl.habitat_lvl == 2:
            for i, x in enumerate(hero.slots.slots):
                if x.unit == self.t4_generator_lvl.unit_type and player.gold > x.amount * (
                        self.t4_generator_lvl.unit_cost_up.gold - self.t4_generator_lvl.unit_cost.gold):
                    GUI.upgrade_unit(9 + i)
                    upgraded = True
                    player.gold -= x.amount * (
                                self.t4_generator_lvl.unit_cost_up.gold - self.t4_generator_lvl.unit_cost.gold)
            cost = 0
            amount = 0
            while player.gold > cost and amount <= self.t4_generator_lvl.unit_ready:  # only gold because most units cost only gold
                amount += 1
                cost += self.t4_generator_lvl.unit_cost_up.gold
            player.gold -= cost
            amount4 = amount
            unit4 = self.t4_generator_lvl.unit_type_up
            upgrades[3] = True
        if self.t3_generator_lvl.habitat_lvl == 1:
            cost = 0
            amount = 0
            while player.gold > cost and amount <= self.t3_generator_lvl.unit_ready:  # only gold because most units cost only gold
                amount += 1
                cost += self.t3_generator_lvl.unit_cost.gold
            player.gold -= cost
            amount3 = amount
            unit3 = self.t3_generator_lvl.unit_type
        elif self.t3_generator_lvl.habitat_lvl == 2:
            for i, x in enumerate(hero.slots.slots):
                if x.unit == self.t3_generator_lvl.unit_type and player.gold > x.amount * (
                        self.t3_generator_lvl.unit_cost_up.gold - self.t3_generator_lvl.unit_cost.gold):
                    GUI.upgrade_unit(9 + i)
                    upgraded = True
                    player.gold -= x.amount * (
                                self.t3_generator_lvl.unit_cost_up.gold - self.t3_generator_lvl.unit_cost.gold)
            cost = 0
            amount = 0
            while player.gold > cost and amount <= self.t3_generator_lvl.unit_ready:  # only gold because most units cost only gold
                amount += 1
                cost += self.t3_generator_lvl.unit_cost_up.gold
            player.gold -= cost
            amount3 = amount
            unit3 = self.t3_generator_lvl.unit_type_up
            upgrades[2] = True
        if self.t2_generator_lvl.habitat_lvl == 1:
            cost = 0
            amount = 0
            while player.gold > cost and amount <= self.t2_generator_lvl.unit_ready:  # only gold because most units cost only gold
                amount += 1
                cost += self.t2_generator_lvl.unit_cost.gold
            player.gold -= cost
            amount2 = amount
            unit2 = self.t2_generator_lvl.unit_type

        elif self.t2_generator_lvl.habitat_lvl == 2:
            for i, x in enumerate(hero.slots.slots):
                if x.unit == self.t2_generator_lvl.unit_type and player.gold > x.amount * (
                        self.t2_generator_lvl.unit_cost_up.gold - self.t2_generator_lvl.unit_cost.gold):
                    GUI.upgrade_unit(9 + i)
                    upgraded = True
                    player.gold -= x.amount * (
                                self.t2_generator_lvl.unit_cost_up.gold - self.t2_generator_lvl.unit_cost.gold)
            cost = 0
            amount = 0
            while player.gold > cost and amount <= self.t2_generator_lvl.unit_ready:  # only gold because most units cost only gold
                amount += 1
                cost += self.t2_generator_lvl.unit_cost_up.gold
            player.gold -= cost
            amount2 = amount
            unit2 = self.t2_generator_lvl.unit_type_up
            upgrades[1] = True
        if self.t1_generator_lvl.habitat_lvl == 1:
            cost = 0
            amount = 0
            while player.gold > cost and amount <= self.t1_generator_lvl.unit_ready:  # only gold because most units cost only gold
                amount += 1
                cost += self.t1_generator_lvl.unit_cost.gold
            player.gold -= cost
            amount1 = amount
            unit1 = self.t1_generator_lvl.unit_type
        elif self.t1_generator_lvl.habitat_lvl == 2:
            for i, x in enumerate(hero.slots.slots):
                if x.unit == self.t1_generator_lvl.unit_type and player.gold > x.amount * (
                        self.t1_generator_lvl.unit_cost_up.gold - self.t1_generator_lvl.unit_cost.gold):
                    GUI.upgrade_unit(9 + i)
                    upgraded = True
                    player.gold -= x.amount * (
                                self.t1_generator_lvl.unit_cost_up.gold - self.t1_generator_lvl.unit_cost.gold)
            cost = 0
            amount = 0
            while player.gold > cost and amount <= self.t1_generator_lvl.unit_ready:  # only gold because most units cost only gold
                amount += 1
                cost += self.t1_generator_lvl.unit_cost_up.gold
            player.gold -= cost
            amount1 = amount
            unit1 = self.t1_generator_lvl.unit_type_up
            upgrades[0] = True

        if upgraded:
            for i in range(8, 16):
                GUI.merge_stacks_unit(i)
                time.sleep(0.1)
        slot = 0
        creatures = [unit7, unit6, unit5, unit4, unit3, unit2, unit1]
        amounts = [amount7, amount6, amount5, amount4, amount3, amount2, amount1]
        for i in range(7):
            if amounts[i] != 0:
                slot = -1
                for j, x in enumerate(self.city_hero.slots.slots):
                    if x.unit.name == creatures[i].name:
                        slot = j
                        break
                if slot == -1:
                    for j, x in enumerate(self.city_hero.slots.slots):
                        if x.unit.name == "":
                            slot = j
                            break
                if slot != -1:
                    self.city_hero.slots.slots[slot].unit = creatures[i]
                    self.city_hero.slots.slots[slot].amount = amounts[i]

        for y in self.city_hero.slots.slots:
            slot = -1
            for i, x in enumerate(hero.slots.slots):
                if x.unit.name == y.unit.name:
                    slot = i
            if slot == -1:
                for i, x in enumerate(hero.slots.slots):
                    if x.unit.name == "":
                        if slot == -1:
                            slot = i
            if slot != -1:
                hero.slots.slots[slot].amount = y.amount
                hero.slots.slots[slot].unit = y.unit
        time.sleep(0.1)
        GUI.recruit_unit("all")
        time.sleep(0.1)
        GUI.move_all_units_to_other_side(1)
        from GUI_handling.AdventureGUI import leave_screen
        leave_screen()

        self.t1_generator_lvl.unit_ready -= amount1
        self.t2_generator_lvl.unit_ready -= amount2
        self.t3_generator_lvl.unit_ready -= amount3
        self.t4_generator_lvl.unit_ready -= amount4
        self.t5_generator_lvl.unit_ready -= amount5
        self.t6_generator_lvl.unit_ready -= amount6
        self.t7_generator_lvl.unit_ready -= amount7

    def end_week(self, player):
        """
        Checking lvl of fort building to estimate growth multiplier for given unit generator
        """
        multiplier = 1
        if self.fort.fort_lvl == 2:
            multiplier = 1.5
        elif self.fort.fort_lvl == 3:
            multiplier = 2
        if self.t1_generator_lvl.habitat_lvl > 0:
            self.t1_generator_lvl.unit_ready += self.t1_generator_lvl.growth * multiplier
        if self.t2_generator_lvl.habitat_lvl > 0:
            self.t2_generator_lvl.unit_ready += self.t2_generator_lvl.growth * multiplier
        if self.t3_generator_lvl.habitat_lvl > 0:
            self.t3_generator_lvl.unit_ready += self.t3_generator_lvl.growth * multiplier
        if self.t4_generator_lvl.habitat_lvl > 0:
            self.t4_generator_lvl.unit_ready += self.t4_generator_lvl.growth * multiplier
        if self.t5_generator_lvl.habitat_lvl > 0:
            self.t5_generator_lvl.unit_ready += self.t5_generator_lvl.growth * multiplier
        if self.t6_generator_lvl.habitat_lvl > 0:
            self.t6_generator_lvl.unit_ready += self.t6_generator_lvl.growth * multiplier
        if self.t7_generator_lvl.habitat_lvl > 0:
            self.t7_generator_lvl.unit_ready += self.t7_generator_lvl.growth * multiplier

    def __repr__(self):
        return self.name + f' value: ({str(self.value)})'

    def __str__(self):
        return self.name + f' value: ({str(self.value)})'

    def crop_building_names(self):
        """
        Reads and fills town object with adequate buildings in a given town
        """
        img = super().take_screenshot()
        result_array = []
        w = self.textbox_width
        h = self.textbox_height
        textbox_width = 150
        textbox_height = 16
        # City hall
        print('city hall')
        result = super().crop_city_hall(img)
        result_array.append(result)

        if result[0] == 'Town Hall':
            self.city_hall.city_hall_lvl = 0
        elif result[0] == 'City Hall':
            self.city_hall.city_hall_lvl = 1
        elif result[1] != 'yellow':
            self.city_hall.city_hall_lvl = 2
        else:
            self.city_hall.city_hall_lvl = 3
            self.city_hall.built = True

        # Citadel
        print('citadel')
        result = super().crop_citadel(img)
        result_array.append(result)

        if result[0] == 'Fort':
            self.fort.fort_lvl = 0
        elif result[0] == 'Citadel':
            self.fort.fort_lvl = 1
        elif result[0] == 'Castle' and result[1] != 'yellow':
            self.fort.fort_lvl = 2
        else:
            self.fort.fort_lvl = 3
            self.fort.built = True

        # Tavern
        print('tavern')
        result = super().crop_tavern(img)
        result_array.append(result)

        if result[1] == 'yellow':
            self.tavern.built = True

        # Blacksmith
        print('Blacksmith')
        result = super().crop_blacksmith(img)
        result_array.append(result)

        if result[1] == 'yellow':
            self.blacksmith.built = True

        # Marketplace
        print('Marketplace')
        img_copy = img[453:453 + h, 691:691 + w]
        result = super().give_text_and_color(img_copy)
        result_array.append(result)

        if result[0] == 'Marketplace':
            self.marketplace.built = False
        elif result[1] != 'yellow':
            self.marketplace.built = True
        else:
            self.resource_silo.built = True
            self.marketplace.built = True

        # Mage guild
        print('Mage guild')
        img_copy = img[453:453 + h, 885:885 + w]
        result = super().give_text_and_color(img_copy)
        result_array.append(result)

        if result[0] == 'Mage Guild Level 1':
            self.mage_guild.mage_guild_lvl = 0
        elif result[0] == 'Mage Guild Level 2':
            self.mage_guild.mage_guild_lvl = 1
        elif result[0] == 'Mage Guild Level 3' and result[1] != 'yellow':
            self.mage_guild.mage_guild_lvl = 2
        elif result[0] == 'Mage Guild Level 3' and result[1] == 'yellow':
            self.mage_guild.mage_guild_lvl = 3
        elif result[0] == 'Mage Guild Level 4' and result[1] != 'yellow':
            self.mage_guild.mage_guild_lvl = 3
        elif result[0] == 'Mage Guild Level 4' and result[1] == 'yellow':
            self.mage_guild.mage_guild_lvl = 4
        elif result[0] == 'Mage Guild Level 5' and result[1] != 'yellow':
            self.mage_guild.mage_guild_lvl = 4
        elif result[0] == 'Mage Guild Level 5' and result[1] == 'yellow':
            self.mage_guild.mage_guild_lvl = 5
            self.mage_guild.built = True

        # Shipyard 'Not implemented'
        print('Shipyard', 'Not implemented')
        # img_copy = img[453:453+h, 1079:1079+w]
        # result = super().give_text_and_color(img_copy)
        # result_array.append(result)

        # Cage of Warlords
        print('Cage of Warlords')
        img_copy = img[557:557 + h, 691:691 + w]
        result = 'Cage of Warlords', super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.cage_of_warlords.built = True

        # Glyphs of Fear/Blood Obelisk
        print('Glyphs of Fear')
        img_copy = img[557:557 + h, 885:885 + w]
        result = super().give_text_and_color(img_copy)
        result_array.append(result)

        if result[0] != 'Glyphs of Fear' and result[1] != 'yellow':
            self.glyphs_of_fear.built = True
        else:
            self.blood_obelisk.built = True
            self.glyphs_of_fear.built = True

        # Captain's Quarters
        print("Captain's Quarters")
        img_copy = img[557:557 + h, 1079:1079 + w]
        result = "Captain's Quarters", super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.captains_quarters.built = True

        # t1
        print('t1')
        result = super().crop_t1(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'gnoll hut':
            self.t1_generator_lvl.habitat_lvl = 0
        elif result[1] != 'yellow':
            self.t1_generator_lvl.habitat_lvl = 1
        else:
            self.t1_generator_lvl.habitat_lvl = 2
            self.t1_generator_lvl.built = True

        # t2
        print('t2')
        result = super().crop_t2(img)
        result_array.append(result)
        name = result[0].lower()
        if name == "lizard den":
            self.t2_generator_lvl.habitat_lvl = 0
        elif result[1] != 'yellow':
            self.t2_generator_lvl.habitat_lvl = 1
        else:
            self.t2_generator_lvl.habitat_lvl = 2
            self.t2_generator_lvl.built = True

        # t3
        print('t3')
        result = super().crop_t3(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'serpent fly hive':
            self.t3_generator_lvl.habitat_lvl = 0
        elif result[1] != 'yellow':
            self.t3_generator_lvl.habitat_lvl = 1
        else:
            self.t3_generator_lvl.habitat_lvl = 2
            self.t3_generator_lvl.built = True

        # t4
        print('t4')
        result = super().crop_t4(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'basilisk pit':
            self.t4_generator_lvl.habitat_lvl = 0
        elif result[1] != 'yellow':
            self.t4_generator_lvl.habitat_lvl = 1
        else:
            self.t4_generator_lvl.habitat_lvl = 2
            self.t4_generator_lvl.built = True

        # t5
        print('t5')
        result = super().crop_t5(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'gorgon lair':
            self.t5_generator_lvl.habitat_lvl = 0
        elif result[1] != 'yellow':
            self.t5_generator_lvl.habitat_lvl = 1
        else:
            self.t5_generator_lvl.habitat_lvl = 2
            self.t5_generator_lvl.built = True

        wyv = {'wyvern nest', 'upg. wyvern nest'}

        # t6
        print('t6')
        result = super().crop_t6(img)
        result_array.append(result)
        name = result[0].lower()
        name = get_close_matches(name, wyv, 1)[0]
        if name == 'wyvern nest':
            self.t6_generator_lvl.habitat_lvl = 0
        elif result[1] != 'yellow':
            self.t6_generator_lvl.habitat_lvl = 1
        else:
            self.t6_generator_lvl.habitat_lvl = 2
            self.t6_generator_lvl.built = True

        # t7
        print('t7')
        result = super().crop_t7(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'hydra pond':
            self.t7_generator_lvl.habitat_lvl = 0
        elif result[1] != 'yellow':
            self.t7_generator_lvl.habitat_lvl = 1
        else:
            self.t7_generator_lvl.habitat_lvl = 2
            self.t7_generator_lvl.built = True

        return result_array
