import hashlib
import os

file_path = "/home/kali/test.txt"
def hash_calc(file_path):
	sha256_hash = hashlib.sha256()
	with open(file_path, "rb") as f:
		# hash the file in blocks of 4K bits; effective in handling large files 
		for byte_block in iter(lambda: f.read(4096), b""):
			sha256_hash.update(byte_block)
		print (sha256_hash.hexdigest())
		return sha256_hash.hexdigest()

def get_filenames(file_path):
	files = os.listdir(file_path)
	files = [file_path+'/'+f for f in files if os.path.isfile(file_path+'/'+f)]  # making sure to only read files and not directories
	return (files)
	print(*files, sep="\n")

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


#hash_calc("/home/kali/test.txt")

print ("What would you like to do? Enter A or B")
print ("(A) Collect new baseline!")
print ("(B) Begin monitoring files with saved baseline?")

user_input = input()

if (user_input.lower() == "a"):
	print ("Calculate new baseline \n")

	file_names = get_filenames("/home/kali/fim-tool/Files")
	create_baseline(file_names)
else: print ("Begin monitoring")

# Reference
# https://www.quickprogrammingtips.com/python/how-to-calculate-sha256-hash-of-a-file-in-python.html

#df