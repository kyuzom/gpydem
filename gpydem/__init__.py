from .gsmmodem import ModemError
from .huawei_e220 import ModemHuaweiE220

class Modem(object):
	@staticmethod
	def get(ftype, *args, **kwargs):
		if ftype == "HuaweiE220":
			return ModemHuaweiE220(*args, **kwargs)
		raise TypeError("Not supported type '%s'!" % (ftype))
