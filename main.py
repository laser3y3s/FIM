import hashlib
import os
import time

file_path = "/home/kali/test.txt"
def hash_calc(file_path):
	sha256_hash = hashlib.sha256()
	with open(file_path, "rb") as f:
		# hash the file in blocks of 4K bits; effective in handling large files 
		for byte_block in iter(lambda: f.read(4096), b""):
			sha256_hash.update(byte_block)
		#print (sha256_hash.hexdigest())
		return sha256_hash.hexdigest()

def get_filenames(file_path):
	files = os.listdir(file_path)
	files = [file_path+'/'+f for f in files if os.path.isfile(file_path+'/'+f)]  # making sure to only read files and not directories
	return (files)
	#print(*files, sep="\n")

def create_baseline(file_names):
	print ("File names --->", file_names)
	baseline_path = "/home/kali/fim-tool/baseline.txt"
	f = open(baseline_path, "w")
	f.write("")
	f.close()
	for file in file_names:
		baseline_file = open(baseline_path, "a")
		baseline_file.write(file+"|"+hash_calc(file)+"\n")
		baseline_file.close()

def read_baseline():
	fileHashDictionary = {}
	with open("baseline.txt","r") as f:
		for line in f:
			print("line -->", line)
			# split baseline.txt into key and value and store them in a dictionary
			key,value = line.strip().split("|")
			fileHashDictionary[key] = value

	print ("dict --->", fileHashDictionary)
	return fileHashDictionary

def calcLatestFileHashes():
	newHashDictionary = {}
	files = get_filenames("/home/kali/fim-files")
	for file in files:
		newHashDictionary[file] = hash_calc(file)
	return newHashDictionary


def checkAgainstBaseline(baselineDictionary):
	while True:
		newHashDictionary = calcLatestFileHashes()
		time.sleep(1)
		if (set(baselineDictionary.keys()) - set(newHashDictionary.keys()) != set()):
			missing_keys = set(baselineDictionary.keys()) - set(newHashDictionary.keys())
			print ("Deleted Files ----> ", missing_keys)
		elif (set(newHashDictionary.keys()) - set(baselineDictionary.keys()) != set()):
			missing_keys = set(newHashDictionary.keys()) - set(baselineDictionary.keys())
			print ("Added files ------>", missing_keys)
		missing_keys = [key for key in baselineDictionary if baselineDictionary[key] != newHashDictionary[key]]
		if missing_keys:
			print ("File Edited ----->", missing_keys)



#hash_calc("/home/kali/test.txt")

print ("What would you like to do? Enter A or B")
print ("(A) Collect new baseline!")
print ("(B) Begin monitoring files with saved baseline?")

user_input = input()

if (user_input.lower() == "a"):

	file_names = get_filenames("/home/kali/fim-files")
	create_baseline(file_names)
	print ("New Baseline is Created")

elif (user_input.lower() == "b"):

	print ("Begin monitoring")
	baselineDictionary = read_baseline()
	checkAgainstBaseline(baselineDictionary)



# Reference
# https://www.quickprogrammingtips.com/python/how-to-calculate-sha256-hash-of-a-file-in-python.html