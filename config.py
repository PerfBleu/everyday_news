from configparser import RawConfigParser, NoOptionError
import os
from pathlib import Path

working_path = Path(os.path.dirname(__file__))
cfgpath = working_path / 'config.ini'
config = RawConfigParser()
config.read(cfgpath)
default_setting = [True]

def get_group_config_byindex(gid: int, index: int) -> bool:
    return get_group_config(gid=gid)[index]

def set_group_config_byindex(gid: int, index: int, setting: bool):
    cfg =  get_group_config(gid)
    cfg[index] = setting
    write_group_config(gid, encode_setting(cfg))
    
def set_default_config(gid: int):
    write_group_config(gid, encode_setting(default_setting))

def get_group_config(gid: int) -> list:
    try:
        setting_str = config.get('GROUP_CONFIG', str(gid))
    except NoOptionError:
        set_default_config(gid)
        return default_setting
    return(parse_setting(settingstr=setting_str))

def write_group_config(gid: int, setting_str: str):
    config.set('GROUP_CONFIG', str(gid), setting_str)
    with open(cfgpath, 'w') as f:
        config.write(f)

def parse_setting(settingstr: str) -> list:
    setting_list = []
    for i in settingstr:
        setting_list.append(True if i == 1 else False)
    return(setting_list)

def encode_setting(cfglist: list) -> str:
    string = ''
    for cfg in cfglist:
        string += ('1' if cfg else '0')
    return(string)