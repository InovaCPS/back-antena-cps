#   Date: 2018-08-11
#   Author: Lucas Nadalete
#
#   License: GPL v3


"""
    Config helper implemments a common methods used to load configuration.
"""

from configparser import RawConfigParser


class ConfigHelper:

    def __init__(self, filename):
        """Method used to load properties file.

        :param filename: The properties file absolute or relative path.
        :type filename: str.
        :returns:  ConfigHelper -- The instance of the ConfigHelper object.

        """
        self.config = RawConfigParser()
        self.config.read(filename)

    def get_property_by_section(self, section, prop):
        """Method used to get a specific property based in you section.

        :param section: The property's section.
        :type section: str.
        :param prop: The property's name.
        :type prop: str.
        :returns:  str -- The property's value.

        """
        return self.config.get(section, prop)
