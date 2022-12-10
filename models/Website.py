from enum import Enum


class Website(str, Enum):
    Gidonline = "https://gidonline.io/page/{}"
    Kinokrad = "https://kinokrad.cc/page/{}"
    Kinogo = "https://kinogo-net.la/page/{}"
    Kinoprofi = "https://kinoprofi.vip/page/{}"