"""Script containing Dungeon city class"""

from data.city import City
from data.habitats_cities import *
from data.city_buildings import *
from data.hero import Hero
from data.building import *
from copy import deepcopy
from GUI_handling import TownGUI as GUI
import GUI_handling.AdventureGUI
import image_processing.detecting_window
import image_processing.ok_detection
import time

class Dungeon(City):
    def __init__(self,
                 name: str = "Dungeon",
                 mage_guild: MageGuild = Dungeon_Mage_Guild,
                 city_hall: CityHall = Dungeon_City_Hall,
                 fort: Fort = Dungeon_Fort,
                 marketplace: Marketplace = Dungeon_Marketplace,
                 tavern: Tavern = Dungeon_Tavern,
                 resource_silo: ResourceSilo = Dungeon_Rescource_Silo,
                 blacksmith: Building = Dungeon_Blacksmith,
                 t1: Habitat = Warren,
                 t2: Habitat = Harpy_Loft,
                 t3: Habitat = Pillar_of_Eyes,
                 t4: Habitat = Chapel_of_Stilled_Voices,
                 t5: Habitat = Labyrinth,
                 t6: Habitat = Manticore_Lair,
                 t7: Habitat = Dragon_Cave,
                 merch: Building = Artifact_Merchants_D,
                 portal: Building = Portal_of_Summoning,
                 mana: Building = Mana_Vortex,
                 scholar: Building = Battle_Scholar_Academy,
                 rings: Building = Mushroom_Rings,
                 graal: bool = False,
                 upper_hero: Hero = Hero(0, "", "", 0, 0, 0, 0),
                 lower_hero: Hero = Hero(0, "", "", 0, 0, 0, 0),
                 owned_by: str = 'neutral'):
        """

        A class representing Dungeon city

        :param name: Name of the given city
        :param mage_guild: Mage guild object
        :param city_hall: City hall object
        :param fort: Fort object
        :param marketplace: Marketplace object
        :param tavern: Tavern object
        :param resource_silo: Resource silo object
        :param blacksmith: Blacksmith object
        :param t1: 1st level habitat - Warren
        :param t2: 2nd level habitat - Harpy Loft
        :param t3: 3rd level habitat - Pillar of Eyes
        :param t4: 4th level habitat - Chapel of Stilled Voices
        :param t5: 5th level habitat - Labyrynth
        :param t6: 6th level habitat - Manticore Lair
        :param t7: 7th level habitat - Dragon Cave
        :param merch: Artifact merchant object
        :param portal: Portal of Summoning object
        :param mana: Mana Vortex object
        :param scholar: Battle Scholar Academy object
        :param rings: Mushroom Rings object
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
        self.artifact_merchant = merch
        self.portal_of_summoning = portal
        self.mana_vortex = mana
        self.battle_scholar_academy = scholar
        self.mushroom_rings = rings

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
        img_copy = img[453:453 + h, 594:594 + w]
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
        img_copy = img[453:453 + h, 788:788 + w]
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

        # Mana Vortex

        print("Mana Vortex")
        img_copy = img[453:453 + h, 1176:1176 + w]
        result = "Mana Vortex", super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.mana_vortex.built = True

        # Portal of Summoning
        print("Portal of Summoning")
        img_copy = img[453:453 + h, 1176:1176 + w]
        result = "Portal of Summoning", super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.portal_of_summoning.built = True

        # Artifact Merchant
        print('Artifact Merchant')
        img_copy = img[557:557 + h, 691:691 + w]
        result = 'Artifact Merchant', super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.artifact_merchant.built = True

        # Battle Scholar Academy
        print('Battle Scholar Academy')
        img_copy = img[557:557 + h, 885:885 + w]
        result = 'Battle Scholar Academy', super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.battle_scholar_academy.built = True

        # Mushroom Rings
        print('Mushroom Rings')
        img_copy = img[557:557 + h, 1079:1079 + w]
        result = 'Mushroom Rings', super().check_color(img_copy)
        result_array.append(result)

        if result[1] == 'yellow':
            self.mushroom_rings.built = True

        # t1
        print('t1', end=" ")
        result = super().crop_t1(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'warren':
            self.t1_generator_lvl.habitat_lvl = 0
        elif result[1] != 'yellow':
            self.t1_generator_lvl.habitat_lvl = 1
        else:
            self.t1_generator_lvl.habitat_lvl = 2
            self.t1_generator_lvl.built = True
        print(self.t1_generator_lvl.habitat_lvl)

        # t2
        print('t2', end=" ")
        result = super().crop_t2(img)
        result_array.append(result)
        name = result[0].lower()
        if name == "harpy loft":
            self.t2_generator_lvl.habitat_lvl = 0
        elif result[1] != 'yellow':
            self.t2_generator_lvl.habitat_lvl = 1
        else:
            self.t2_generator_lvl.habitat_lvl = 2
            self.t2_generator_lvl.built = True
        print(self.t2_generator_lvl.habitat_lvl)

        # t3
        print('t3', end=" ")
        result = super().crop_t3(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'pillar of eyes':
            self.t3_generator_lvl.habitat_lvl = 0
        elif result[1] != 'yellow':
            self.t3_generator_lvl.habitat_lvl = 1
        else:
            self.t3_generator_lvl.habitat_lvl = 2
            self.t3_generator_lvl.built = True
        print(self.t3_generator_lvl.habitat_lvl)

        # t4
        print('t4', end=" ")
        result = super().crop_t4(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'chapel of stilled voices':
            self.t4_generator_lvl.habitat_lvl = 0
        elif result[1] != 'yellow':
            self.t4_generator_lvl.habitat_lvl = 1
        else:
            self.t4_generator_lvl.habitat_lvl = 2
            self.t4_generator_lvl.built = True
        print(self.t4_generator_lvl.habitat_lvl)

        # t5
        print('t5', end=" ")
        result = super().crop_t5(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'labyrinth':
            self.t5_generator_lvl.habitat_lvl = 0
        elif result[1] != 'yellow':
            self.t5_generator_lvl.habitat_lvl = 1
        else:
            self.t5_generator_lvl.habitat_lvl = 2
            self.t5_generator_lvl.built = True
        print(self.t5_generator_lvl.habitat_lvl)

        # t6
        print('t6', end=" ")
        result = super().crop_t6(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'manticore lair':
            self.t6_generator_lvl.habitat_lvl = 0
        elif result[1] != 'yellow':
            self.t6_generator_lvl.habitat_lvl = 1
        else:
            self.t6_generator_lvl.habitat_lvl = 2
            self.t6_generator_lvl.built = True
        print(self.t6_generator_lvl.habitat_lvl)

        # t7
        print('t7', end=" ")
        result = super().crop_t7(img)
        result_array.append(result)
        name = result[0].lower()
        if name == 'dragon cave':
            self.t7_generator_lvl.habitat_lvl = 0
        elif result[1] != 'yellow':
            self.t7_generator_lvl.habitat_lvl = 1
        else:
            self.t7_generator_lvl.habitat_lvl = 2
            self.t7_generator_lvl.built = True
        print(self.t7_generator_lvl.habitat_lvl)

        return result_array
