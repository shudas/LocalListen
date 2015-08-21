import ConfigParser

config_file = "config"
_config = None


def get_config():
    global _config
    if _config is not None:
        return _config
    _config = read_config()
    return _config


def read_config():
    # config was already loaded
    ret = dict()
    conf_parser = ConfigParser.ConfigParser()
    conf_parser.read(config_file)
    for section in conf_parser.sections():
        dict1 = dict()
        options = conf_parser.options(section)
        for option in options:
            try:
                dict1[option] = conf_parser.get(section, option)
                if dict1[option] == -1:
                    print("skipping: %s" % option)
            except:
                print("exception on %s! Setting %s value to None" % option)
                dict1[option] = None
        ret[section] = dict1
    return ret
