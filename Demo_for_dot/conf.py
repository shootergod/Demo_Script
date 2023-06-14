# ============================================================
# Import
# ============================================================
import os, json

# ============================================================
# Constant
# ============================================================
CWD = os.path.dirname(__file__)
CONF_FP = os.path.join(CWD, 'conf.json')

# ============================================================
# Class
# ============================================================
class Config():
    def __init__(self, fp: str = CONF_FP) -> None:
        if not os.path.isfile(fp):
            info = 'Config Init Failed @ {}'.format(fp)
            raise Exception(info)

        self.__fp = fp
        self.__conf: dict = None

        self.__read_conf()

    def __read_conf(self):
        with open(self.__fp, 'r', encoding='utf-8') as fid:
            self.__conf = json.load(fid)

    def __put_conf(self):
        with open(self.__fp, 'w', encoding='utf-8') as fid:
            json.dump(self.__conf, fid, indent=4, sort_keys=True, ensure_ascii=False)

    def get_opt(self, opt_name: str):
        return self.__conf.get(opt_name)

    def set_opt(self, opt_name: str, opt_val):
        if opt_name in self.__conf:
            self.__conf[opt_name] = opt_val
            self.__put_conf()
        else:
            info = 'Invalid Key: {}'.format(opt_name)
            raise Exception(info)