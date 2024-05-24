import os, requests, tarfile, shutil, json, colorama, platform, zipfile
from tqdm import tqdm
from sys import exit
print("Fabveri\n")

# OS Detect
if platform.system() != "Linux":
    if platform.system() != "Windows":
        exit()

# Get latest links
if os.path.isfile("links.json"):
    os.remove("links.json")
links = json.loads(requests.get("https://raw.githubusercontent.com/yagmire/fabveri/main/links.json").text)
fabricURL = links["fabric"]
if platform.system() == "Linux":
    javaURL = links["java-linux"]
elif platform.system() == "Windows":
    javaURL = links["java-windows"]
print("Updated links.")

# Getting fabric installer
if os.path.isfile("fabricinstaller.jar"):
    print("Fabric installer already exists.")
else:
    r = requests.get(fabricURL, stream=True)
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024 
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open('fabricinstaller.jar', 'wb') as f:
        for data in r.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    print("Successfully downloaded fabric installer.")

# Getting java
if platform.system() == "Linux":
    if os.path.isdir("java"):
        print("Java already exists.")
    else:
        r = requests.get(javaURL, stream=True)
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open('java.tar.gz', 'wb') as f:
            for data in r.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()
        java = tarfile.open('java.tar.gz') 
        java.extractall('./java')
        java.close()
        print("Successfully downloaded java.")

elif platform.system() == "Windows":
    if os.path.isdir("java"):
        print("Java already exists.")
    else:
        r = requests.get(javaURL, stream=True)
        with zipfile.ZipFile("java.zip", 'r') as zip_ref:
            zip_ref.extractall("java")
        print("Successfully downloaded java.")


req_snapshot = input(f"{colorama.Fore.BLUE}Use a snapshot version? (y or n)\n{colorama.Fore.WHITE}")

req_ver = input(f"{colorama.Fore.BLUE}What version of Minecraft?{colorama.Fore.WHITE}\n")

def ifSnapshot():
    if req_snapshot.lower() == "y":
        return "-snapshot"
    else:
        return ""
    
def cleanup():
    # Fabric installer
    try:
        os.remove("fabricinstaller.jar")
    except Exception as e:
        print(f"\n{colorama.Fore.RED}There was an error deleting the fabric installer.\n{e}{colorama.Fore.WHITE}\n")
    
    # Java archive
    try:
        os.remove("java.tar.gz")
    except Exception as e:
        print(f"\n{colorama.Fore.RED}There was an error deleteing the java archive.\n{e}{colorama.Fore.WHITE}\n")

    # Java Folder
    try:
        shutil.rmtree("java")
    except Exception as e:
        print(f"\n{colorama.Fore.RED}There was an error deleting the java folder.\n{e}{colorama.Fore.WHITE}\n")

print(f"Fabric installer: {os.path.isfile('fabricinstaller.jar')}")
print(f"Java: {os.path.isdir('./java')}")

if platform.system() == "Linux":
    operation = f"./java/jdk-17.0.9/bin/java -jar fabricinstaller.jar client {ifSnapshot()} -mcversion {req_ver}"
    print(f"Running system command: {operation}")
    os.system(operation)
elif platform.system() == "Windows":
    operation = f"java/jdk-17.0.9/bin/java.exe -jar fabricinstaller.jar client {ifSnapshot()} -mcversion {req_ver}"
    print(f"Running system command: {operation}")
    os.system(operation)

cleanup()
print("Cleaned up.")
