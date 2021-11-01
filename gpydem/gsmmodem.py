#!/usr/bin/env python
'''
GPy modem - 3G GSM USB modem handler.
Base GSM modem.
'''
import sys
import datetime
import time
import abc
import serial

class ModemError(RuntimeError):
	pass

class ModemMessage(object):
	'''
	USB GSM modem device message object.
	'''
	def __init__(self, index, modem, number, date, text):
		self.index = index
		self.modem = modem
		self.number = number
		if date is not None:
			# modem incorrectly reports UTC time rather than local time so ignore time zone info
			date = date[:-3]
			self.date = datetime.datetime.strptime(date, "%y/%m/%d,%H:%M:%S")
		self.text = text

	def delete(self):
		'''
		Delete message from SIM card.
		'''
		response = self.modem.command("AT+CMGD=%d" % self.index)
		ok = False
		for line in response:
			if "OK" in line:
				ok = True
		if not ok:
			raise ModemError("Deletion of message #%d failed!" % self.index)

class ModemBase(object):
	'''
	USB GSM modem device base object.
	'''
	__metaclass__ = abc.ABCMeta

	def __init__(self, dev_id, baudrate=9600, PIN=None, re_timeout=1):
		self.conn = serial.Serial(dev_id, baudrate, timeout=1, rtscts=1)
		self.command("AT")
		if PIN:
			# check whether PIN is already set
			results = self.command("AT+CPIN?")
			for line in results:
				if "CPIN: READY" in line:
					break	# PIN is already set
			else:
				self.command("AT+CPIN=%s" % str(PIN))
				self.reboot(timeout=re_timeout)
		self.command("AT+CMGF=1")

	def __del__(self):
		try:
			self.close()
		except AttributeError:
			pass

	def command(self, atcommand, flush=True):
		'''
		Execute given AT command.
		@param atcommand: [str] Command
		@param flush: [bool] Flush the message or not
		@return [list] Results of the given command
		'''
		if sys.version_info[0] == 3:
			atcommand = str.encode(atcommand)
		self.conn.write(atcommand)
		if flush:
			at_flush = "\r\n"
			if sys.version_info[0] == 3:
				at_flush = str.encode(at_flush)
			self.conn.write(at_flush)
		results = [line.strip() for line in  self.conn.readlines()]
		if sys.version_info[0] == 3:
			results = [r.decode() for r in results if r]
		for line in results:
			if "ERROR" in line:
				raise ModemError(line)
		return results

	def wait(self, timeout=None):
		'''
		Wait for at least one result to be available.
		@param timeout: [float] Timeout for reading
		'''
		old_timeout = self.conn.timeout
		self.conn.timeout = timeout
		results = self.conn.read()
		self.conn.timeout = old_timeout
		results = self.conn.readlines()

	def close(self):
		'''
		Close serial connection to the USB modem.
		'''
		self.conn.close()

	def reboot(self, timeout=1.0):
		'''
		Restart USB modem.
		@param timeout: [float] Timeout to wait between turn off and on
		'''
		self.command("AT+CFUN=0")
		time.sleep(timeout)
		self.command("AT+CFUN=1")

	@abc.abstractmethod
	def sendSMS(self, number, message):
		pass

	@abc.abstractmethod
	def messages(self):
		return []	# [ModemMessage]
