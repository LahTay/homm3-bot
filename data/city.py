"""Script containing city class representing casles in the game"""
import cv2

from data.building import *
from data.hero import Hero
from mss import mss
from image_processing import ocr
import numpy as np


class City:
    def __init__(self, mage_guild: MageGuild, fort: Fort, city_hall: CityHall, tavern: Tavern,
                 marketplace: Marketplace, resource_silo: ResourceSilo, blacksmith: Building, graal: bool = False,
                 upper_hero: Hero = Hero(0, "", "", 0, 0, 0, 0), lower_hero: Hero = Hero(0, "", "", 0, 0, 0, 0),
                 owned_by: str = 'neutral'):
        """
        Init function for a City Class.

        :param mage_guild: Mage guild object
        :param fort: Fort object
        :param city_hall: City hall object
        :param tavern: Tavern object
        :param marketplace: Marketplace object
        :param resource_silo: Resource silo object
        :param blacksmith: Blacksmith object
        :param graal: Boolean True - graal, False - no graal
        :param upper_hero: Hero object that is present in the higher row of the city slot bar
        :param lower_hero: Hero object that is present in the lower row of the city slot bar
        :param owned_by: Which player owns the building
        """
        self.city = "City"
        self.fort = fort
        self.city_hall = city_hall
        self.mage_guild = mage_guild       
        self.tavern = tavern
        self.marketplace = marketplace
        self.blacksmith = blacksmith
        self.name_of_city = ""
        self.resource_silo = resource_silo
        self.need_read = False
        self.graal = graal

        self.city_hero = upper_hero
        self.arriving_hero = lower_hero
        self.owned_by = owned_by
        self.value = 0
        self.textbox_width = int(150)
        self.textbox_height = int(16)
        self.position = (0,0)


    def end_day(self,player):
        """
        Buffer function
        """
        if self.city_hall.city_hall_lvl == 1:
            player.gold += 500
        if self.city_hall.city_hall_lvl == 2:
            player.gold += 1000
        if self.city_hall.city_hall_lvl == 3:
            player.gold += 2000
        if self.city_hall.city_hall_lvl == 4:
            player.gold += 4000

    def take_screenshot(self):
        """
        Takes a screenshot.

        :return: screenshot image
        """
        with mss() as sct:
            monitor = sct.monitors[1]
            img = np.array(sct.grab(monitor))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            #cv2.imshow('win', img)
            #cv2.waitKey(0)
            return img

    def read_text(self, img):
        """
        Reads text from an image.

        :param img: input image
        :return: read text
        """
        text: str = ocr.read_generic_text(img, 2)
        return text

    def check_color(self, img):
        """
        Checks background color of an image where the text is.

        :param img: input image
        :return: one of four strings: 'green', 'yellow', 'red', 'gray'
        """
        if (img[0, 0, 0] == 123 and
            img[0, 0, 1] == 181 and
           img[0, 0, 2] == 115):
            return 'green'
        elif (img[0, 0, 0] == 99 and
              img[0, 0, 1] == 189 and
              img[0, 0, 2] == 231):
            return 'yellow'
        elif (img[0, 0, 0] == 123 and
              img[0, 0, 1] == 123 and
              img[0, 0, 2] == 255):
            return 'red'
        else:
            return 'gray'

    def give_text_and_color(self, img):
        """
        Returns text and color of the text's background.

        :param img: input image
        :return: name, color
        """
        name: str = self.read_text(img)
        color = self.check_color(img)
        return name, color

    def crop_city_hall(self, img):
        """
        Cropps city hall

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[349:349 + self.textbox_height, 594:594 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_citadel(self, img):
        """
        Cropps citadel

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[349:349 + self.textbox_height, 788:788 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_tavern(self, img):
        """
        Cropps tavern

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[349:349 + self.textbox_height, 982:982 + self.textbox_width]
        return 'Tavern', self.check_color(img_copy)

    def crop_blacksmith(self, img):
        """
        Cropps blacksmith

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[349:349 + self.textbox_height, 1176:1176 + self.textbox_width]
        return 'Blacksmith', self.check_color(img_copy)

    def crop_t1(self, img):
        """
        Cropps tier one unit building

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[661:661 + self.textbox_height, 594:594 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_t2(self, img):
        """
        Cropps tier two unit building

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[661:661 + self.textbox_height, 788:788 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_t3(self, img):
        """
        Cropps tier three unit building

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[661:661 + self.textbox_height, 982:982 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_t4(self, img):
        """
        Cropps tier four unit building

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[661:661 + self.textbox_height, 1176:1176 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_t5(self, img):
        """
        Cropps tier five unit building

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[765:765 + self.textbox_height, 691:691 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_t6(self, img):
        """
        Cropps tier six unit building

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[765:765 + self.textbox_height, 885:885 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def crop_t7(self, img):
        """
        Cropps tier seven unit building

        :param img: input image
        :return: image with text and color
        """
        img_copy = img[765:765 + self.textbox_height, 1079:1079 + self.textbox_width]
        return self.give_text_and_color(img_copy)

    def action(self, player, hero):
        """
        Action buffer function

        :param player: player object
        :param hero: hero object
        """
        pass

    def __eq__(self, other):
        if issubclass(type(other), City):
            return self.name_of_city == other.name_of_city
        else:
            return False







