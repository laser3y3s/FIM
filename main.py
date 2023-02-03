import hashlib
import os
from time import time, ctime, sleep
import stat
import sys


# file_path = "/home/kali/test.txt"

def logger(msg):
	f = open(log_file_path, "a")
	f.write(ctime(time()) + " : " + msg + " \n")
	f.close()

def check_file_privileges(file_paths):
	for file_path in file_paths:
	    st = os.stat(file_path)
	    if (st.st_mode & (stat.S_IRWXG + stat.S_IRWXO)) != 0:
	    	return False
	return True 					# returns TRUE if neither the 'group' nor 'others' of the file have any permissions

def ifFileExistsChecker(file_to_check):
	match file_to_check:
		case "baseline":
			if os.path.isfile(baseline_file_path):
				return True
			else:
				return False

		case "global_variables":
			text_to_print = "The global_variables.py file does not exist. Please download it from our GitHub Repo and place it in the same directory as main.py"
			print (text_to_print)
			logger(text_to_print)
			sys.exit()

		case "log_file":
			if os.path.isfile(log_file_path):
				return True
			else:
				return False

try:
	from global_variables import *
except:
	ifFileExistsChecker("global_variables")
else:
	True

def create_baseline(file_names):
	print ("File names --->", file_names)
	# baseline_path = "/home/kali/fim-tool/baseline.txt"
	f = open(baseline_file_path, "w")
	f.write("")
	f.close()
	for file in file_names:
		baseline_file = open(baseline_file_path, "a")
		baseline_file.write(file+"|"+hash_calc(file)+"\n")
		baseline_file.close()

def add_baseline():
	file_names = get_filenames(monitoring_files_folder_path)
	create_baseline(file_names)
	print ("New Baseline.txt is Created \n")


def hash_calc(file_path):
	sha256_hash = hashlib.sha256()
	with open(file_path, "rb") as f:
		# hash the file in blocks of 4K bits; effective in handling large files 
		for byte_block in iter(lambda: f.read(4096), b""):
			sha256_hash.update(byte_block)
		return sha256_hash.hexdigest()

def get_filenames(file_path):
	files = os.listdir(file_path)
	files = [file_path+'/'+f for f in files if os.path.isfile(file_path+'/'+f)]  # making sure to only read files and not directories
	return (files)
	#print(*files, sep="\n")

def read_baseline():
	fileHashDictionary = {}
	with open(baseline_file_path,"r") as f:
		for line in f:
			print("line -->", line)
			# split baseline.txt into key and value and store them in a dictionary
			key,value = line.strip().split("|")
			fileHashDictionary[key] = value

	print ("dict --->", fileHashDictionary)
	return fileHashDictionary

def calcLatestFileHashes():
	newHashDictionary = {}
	files = get_filenames(monitoring_files_folder_path)
	for file in files:
		newHashDictionary[file] = hash_calc(file)
	return newHashDictionary


def checkAgainstBaseline(baselineDictionary):
	while True:
		newHashDictionary = calcLatestFileHashes()
		sleep(1)
		if (set(baselineDictionary.keys()) - set(newHashDictionary.keys()) != set()):
			missing_keys = set(baselineDictionary.keys()) - set(newHashDictionary.keys())
			print ("Deleted Files ----> ", missing_keys)
		elif (set(newHashDictionary.keys()) - set(baselineDictionary.keys()) != set()):
			missing_keys = set(newHashDictionary.keys()) - set(baselineDictionary.keys())
			print ("Added files ------>", missing_keys)
		missing_keys = [key for key in baselineDictionary if baselineDictionary[key] != newHashDictionary[key]]
		if missing_keys:
			print ("File Edited ----->", missing_keys)

def start_monitoring():
	baselineDictionary = read_baseline()
	checkAgainstBaseline(baselineDictionary)

def user_exection():

	if check_file_privileges(['./main.py', baseline_file_path, './global_variables.py']) == False:
		text_to_print = "###############    Check the file permission of main.py, baseline.txt and global_variables.py . Make sure they have ONLY owner privileges!  ###############"
		print (text_to_print)
		logger(text_to_print)

	print ("\n")
	print ("What would you like to do? Enter A or B")
	print ("(A) Collect new baseline!")
	print ("(B) Begin monitoring files with saved baseline?")
	print ("Press Ctrl+C to exit")

	user_input = input()

	if (user_input.lower() == "a"):
		if ifFileExistsChecker("baseline"):
			print ("A baseline.txt file already exist. Would you like to replace it? \n")
			user_input = input ("Enter y to proceed or press an other key to go back to Home menu \n")
			if user_input.lower() == "y":
				add_baseline()
			else:
				user_exection()
		else:
			print ("Baseline.txt file does not exist \n")
			user_input = input ("Would you like to create one? Enter y to create and n to exit script ? \n")
			if user_input.lower() == "y":
				add_baseline()
				user_exection()
			else:
				print ("Script Exited") 
			sys.exit()

		
	elif (user_input.lower() == "b"):
		if ifFileExistsChecker("baseline") == False:
			print ("Baseline.txt file does not exist \n")
			user_input = input ("Would you like to create one? Enter y to create and n to exit script ? \n")
			if user_input.lower() == "y":
				add_baseline()
				user_exection()
		print ("Begin monitoring")
		start_monitoring()

def cron_execution():
	if ifFileExistsChecker("baseline") == False:
		logger("Baseline file does not exist! Please create one by running the script in terminal")
		sys.exit()
	logger("Monitoring Started! Well, not really ....")
	f.close()
	# start_monitoring()   if I uncomment this function the monitoring will run in the background

try:
	sys.argv[1] == "22"
except:
	user_exection()
else:
	print ("Cron job execution")
	cron_execution()

# Reference
# https://www.quickprogrammingtips.com/python/how-to-calculate-sha256-hash-of-a-file-in-python.html