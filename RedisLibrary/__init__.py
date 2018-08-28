# -*- coding: utf-8 -*-
import pkg_resources  # part of setuptools
from .RedisLibraryKeywords import RedisLibraryKeywords

__author__ = 'Traitanit Huangsri'
__email__ = 'traitanit.hua@gmail.com'
__version__ = pkg_resources.require("robotframework-redislibrary")[0].version


class RedisLibrary(RedisLibraryKeywords):

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "ROBOT"
