'''
This script generates short urls based on the given input length within the range of 1-6
Before inserting into the ShortURL db it checks if the short url already exists, if yes then it doesn't insert it
'''

from models import *

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
added_count = 0
error_count = 0

#Recursive function to generate all combinations of short urls
def combos(prefix,char_len,remaining):
	global added_count, error_count
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
		combos(prefix+characters[i],char_len,remaining-1)
    

try:
	code_length = int(input("Enter the length of short codes you want to generate\n"))
	if code_length<1 or code_length>6:
		print("Please enter a number >0 and <= 6")
		quit()
except ValueError:
	print("Invalid input, please enter a valid number")
except Exception as e:
	print("An error :"+str(e)+" occurred")
else:
	print("Please wait, adding new ShortURLs to the database...")
	combos('',len(characters),code_length)
	print("Successfully added : "+str(added_count)+" short URLs")
	print("Error adding : "+str(error_count)+" short URLs")
	print("Script completed its operation")