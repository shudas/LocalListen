import ConfigParser

config_file = "config"
config = dict()


def read_config():
    conf_parser = ConfigParser.ConfigParser()
    conf_parser.read(config_file)
    global config
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
        config[section] = dict1

if __name__ == '__main__':
    read_config()