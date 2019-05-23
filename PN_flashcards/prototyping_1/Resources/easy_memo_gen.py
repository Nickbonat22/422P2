import os
current =  os.getcwd()
search_dir = input("Which directory in Resources/ you want to generate a memos.ini: ")
search_dir = os.path.join(current, search_dir)
os.chdir(search_dir)

print("Striping files' names...")
for f in os.listdir(search_dir):
    src = f
    dst = f.strip()
    if not src == dst:
        os.rename(src, dst)
print("Done!")

print("Generating memos.ini...")
files = filter(os.path.isfile, os.listdir(search_dir))
files = [os.path.join(search_dir, f) for f in files] # add path to each file
files.sort(key=lambda x: os.path.getmtime(x))
files = [os.path.basename(f).strip().split('.')[0] for f in files]

with open("memos.ini", 'w') as output:
    for filename in files:
        memo = input("Memo for " + filename + " : ")
        output.write(filename + '\t' + memo + '\n')
print("Done!")