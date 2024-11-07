import sys
import os
import serial
import time
import re
import subprocess

def main():
	if len(sys.argv) != 7:
		print(sys.argv)
		print_usage()
		sys.exit()
	if sys.argv[1]!='-d' or sys.argv[3]!='-b' or sys.argv[5]!='-w':
		print_usage()
		sys_exit()	

	# variables
	device = sys.argv[2]
	baudrate = sys.argv[4]
	wordlist = sys.argv[6]
	print(f"\nDEVICE: {device}\nBAUDRATE: {baudrate}\nWORDLIST: {wordlist}\n")

	if not validate_flags(device, baudrate, wordlist):
		sys.exit()

	# serial connection
	try:
		ser=serial.Serial(device, baudrate, timeout=0.07)	
	except PermissionError:
		print("Permission Error")
		sys.exit()
	try:
		time.sleep(1)
		print(f"serial connection: {ser.name}\n\n")

		with open(wordlist, 'r') as file:
			for line in file:
				# ACTIVATE PASSWORD PROMPT
				#print("sending newline character, activating prompt...")
				ser.write(b'\n')
				
				response_data = ser.read(60) # "enter password" prompt TODO: hardcoded
				#response = response_data.decode()
				
				#print(f"\n[ {response[(len(response)-17):(len(response)-3)]} ]\n") #TODO: hardcoded
				#print(response_data)			

				# TRY PASSWORD
				password = line.strip().encode()
				print(f"trying password: {password.decode()}")

				ser.write(password)
				ser.write(b'\r') # send enter character
				response_data = ser.read(100) # TODO: hardcoded
				response = response_data.decode()
				
				#print(f"[ {response[(len(response)-23):]} ]\n") #TODO: hardcoded
				print(response_data)

				if re.search(r'X', response) == None:
					path = '/usr/share/sounds/LinuxMint/stereo/phone-incoming-call.ogg'
					if os.path.isfile(sound):
						os.system(f"xdg-open {sound}") # ring a bell
					key = line.strip()
					print(f"key found: {key}")
					break
	finally:
		ser.close()





# --------------- functions ----------------

def print_usage():
	print('''
usage: serialbrute -d [DEVICE] -b [BAUDRATE] -w [WORDLIST]
check the number of arguments, the order, or the flags''')

def validate_flags(device, baudrate, wordlist):
	# validate baudate
	try:
		if int(baudrate) > 4000000 or int(baudrate) < 50:
			print(f"baudrate need to be between 50-4000000")
			return False
	except (TypeError, ValueError):
		print(f"baudrate: {baudrate} is not valid")
		return False

	# validate wordlist exists and can be read
	try:
		with open(wordlist, 'r') as file:
			print(f"reading wordlist: {wordlist}")

	except (FileNotFoundError, IsADirectoryError):
		print(f"wordlist {wordlist} not found")
		return False

	# validate device serial tty exists
	if not os.path.exists(device):
		print(f"device {device} not valid")
		return False

	# TODO:need to check device is a valid serial TTY device
	return True

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		sys.exit("\nkeyboard interrupt, goodbye")
	
