'''
This script generates short urls of length 6
Before inserting into the ShortURL db it checks if the short url already exists, if yes then it doesn't insert it
The operation can be paused, resumed and stopped by entering p,r and s respectively.
'''

from models import *

import threading
import os

pause_flag = False
stop_flag = False
added_count = 0
error_count = 0
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


#Recursive function to generate all combinations of short urls
def combos(prefix,char_len,remaining):
	global pause_flag, stop_flag, added_count, error_count
	if stop_flag:
		quit()
	if remaining == 0:
		try:
			already_exists = ShortURL.objects(short_code=prefix).first()
			if not already_exists:
				status = ShortURL.objects(short_code=prefix).update_one(set__used=False, upsert=True)
				added_count = added_count + 1
		except Exception as e:
			error_count = error_count + 1
			print("An error :"+str(e)+" occurred while trying to insert a short url")
		return

	for i in range(char_len):
	    while(pause_flag):
	    	pass
	    combos(prefix+characters[i],char_len,remaining-1)

#To keep checking if the combos function has completed execution and then stop the script
def checkCombosFunction():
	global added_count,error_count
	while(True):
		if not thread1.is_alive():
			print("Successfully added : "+str(added_count)+" short URLs")
			print("Error adding : "+str(error_count)+" short URLs")
			print("Script completed its operation")
			os._exit(1)
	return


thread1 = threading.Thread(target=combos, args=('',len(characters),6), kwargs={})
thread1.start()

thread2 = threading.Thread(target=checkCombosFunction, args=(), kwargs={})
thread2.start()

while(True):
	user_input = input("Enter S to stop operation\nR to resume insertion to database\nP to pause insertion to database:\n\n").strip().lower()
	if user_input == 's':
		stop_flag = True
		break
	if user_input == 'r':
		pause_flag = False
		print("Resumed")
	if user_input == 'p':
		pause_flag = True
		print("Paused")
		