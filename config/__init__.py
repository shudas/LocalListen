from collections import namedtuple
import ConfigParser
import os
__config_file = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))), "app.config")

config = None


def read_config():
    print "CALLING READ_CONFIG"
    # app.config was already loaded
    d = dict()
    conf_parser = ConfigParser.ConfigParser()
    conf_parser.read(__config_file)
    sections = conf_parser.sections()
    test_nt = namedtuple('config', sections)
    for section in conf_parser.sections():
        dict1 = dict()
        options = conf_parser.options(section)
        test_nt1 = namedtuple(section, options)
        for option in options:
            dict1[option] = conf_parser.get(section, option)
        nt1 = test_nt1(**dict1)
        d[section] = nt1
    return test_nt(**d)

if config is None:
    config = read_config()