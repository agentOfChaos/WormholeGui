import configparser
import string
import random


def default_config_params(config: configparser.ConfigParser):
    if not config.has_section("wormhole"): config.add_section("wormhole")
    if not config.has_section("app"): config.add_section("app")

    if not config.has_option("wormhole", "relay"): config["wormhole"]["relay"] = "ws://relay.magic-wormhole.io:4000/v1"
    if not config.has_option("wormhole", "transit"): config["wormhole"]["transit"] = "tcp:transit.magic-wormhole.io:4001"
    #if not config.has_option("wormhole", "appid"): config["wormhole"]["appid"] = "wormhole-gui.io/app-" + ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(32))
    if not config.has_option("wormhole", "appid"): config["wormhole"]["appid"] = "lothar.com/wormhole/text-or-file-xfer"
    if not config.has_option("app", "download_folder"): config["app"]["download_folder"] = ""
    if not config.has_option("app", "language"): config["app"]["language"] = "systemdefault"
    if not config.has_option("app", "num_codewords"): config["app"]["num_codewords"] = "3"


