#!/usr/bin/env python

from __future__ import print_function
import sys
import argparse
import gpydem

def main():
	parser = argparse.ArgumentParser(description="Manage SIM card")
	parser.add_argument("-t", "--modem-type", type=str,   default="HuaweiE220",   help="Modem type")
	parser.add_argument("-i", "--dev-id",     type=str,   default="/dev/ttyUSB0", help="Modem serial device ID")
	parser.add_argument("-b", "--baudrate",   type=int,   default=9600,           help="Modem serial device baudrate")
	parser.add_argument("-p", "--PIN",        type=str,   default="",             help="SIM card PIN code")
	parser.add_argument(      "--re-timeout", type=float, default="1",            help="Modem reboot timeout")
	parser_op = parser.add_mutually_exclusive_group(required=True)
	parser_op.add_argument("-r", "--read",    action="store_true",                help="Read SMS messages")
	parser_op.add_argument("-s", "--send",    action="store_true",                help="Send SMS messages")
	parser.add_argument("-d", "--delete",     action="store_true",                help="Delete read SMS message")
	parser.add_argument("-n", "--number",     type=str,   default="",             help="Phone number")
	parser.add_argument("-m", "--message",    type=str,   default="",             help="SMS message")
	opt = parser.parse_args()
	# start to operate
	gsm = gpydem.Modem.get(opt.modem_type, opt.dev_id, baudrate=opt.baudrate, PIN=opt.PIN, re_timeout=opt.re_timeout)
	if opt.read:
		msgs = gsm.messages()
		if not msgs:
			print("No any UnRead message...")
			return
		for msg in msgs:
			print("UnRead message #%d: %s" % (msg.index, msg.text))
			if opt.delete:
				msg.delete()
	elif opt.send:
		if not opt.number or not opt.message:
			raise Exception("Please add phone number and SMS message.")
		gsm.sendSMS(opt.number, opt.message)

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(str(e))
		sys.exit(1)
