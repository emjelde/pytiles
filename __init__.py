"""
  _______
 |       |
 |       |  _______
 |    ___|_|       |
 |___|     |       |
     |     |       |
     |     |_______|
     |_______|

 pytiles : Template layout FTW!
"""
__version__ = "0.1"
__authors__ = ["Evan Mjelde <evan@mjel.de>"]
__license__ = "MIT"

from pytiles.container import Container
from pytiles.components import String, List, Page, Definition
from pytiles.errors import TilesError

__all__ = ['Container','String','List','Page','Definition','TilesError']
