#!/usr/bin/env python
'''
GPy modem - 3G GSM USB modem handler.
Huawei E220 devide-specific.
'''
import re
from .gsmmodem import ModemBase, ModemMessage

class ModemHuaweiE220(ModemBase):
	'''
	USB GSM modem Huawei E220 device-specific object.
	'''
	def sendSMS(self, number, message):
		'''
		Send SMS message - through SIM card.
		@param number: [int] Phonenumber to send the message
		@param message: [str] Message to send
		'''
		self.command("AT+CMGS=\"%s\"" % number)
		self.command(message + "\x1A", flush=False)

	def messages(self):
		'''
		Give back actual messages - read from SIM card.
		@return [list] Messages
		'''
		msgs = []
		pat = re.compile(r'\+CMGL: (?P<index>\d+),'
			'"(?P<status>.+?)",'
			'"(?P<number>.+?)",'
			'("(?P<name>.+?)")?,'
			'("(?P<date>.+?)")?'
		)
		text = None
		index = None
		date = None
		for line in self.command("AT+CMGL=\"ALL\"")[:-1]:
			m = pat.match(line)
			if m is not None:
				if text is not None:
					msgs.append(ModemMessage(index, self, number, date, text))
				#status = m.group("status")
				index = int(m.group("index"))
				number = m.group("number")
				date = m.group("date")
				text = ""
			elif text is not None:
				if line == "\r\n":
					text += "\n"
				else:
					text += line.strip()
		if text is not None:
			msgs.append(ModemMessage(index, self, number, date, text))
		return msgs
