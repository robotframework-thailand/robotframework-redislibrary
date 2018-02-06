# -*- coding: utf-8 -*-
from .RedisLibraryKeywords import RedisLibraryKeywords
from .version import VERSION

__author__ = 'Traitanit Huangsri'
__email__ = 'traitanit.hua@gmail.com'
__version__ = VERSION


class RedisLibrary(RedisLibraryKeywords):

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "ROBOT"
