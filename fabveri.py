import os, requests, tarfile, shutil, json, colorama, platform
from tqdm import tqdm

print("Fabveri\n")

# Get latest links
if os.path.isfile("links.json"):
    os.remove("links.json")
links = json.loads(requests.get("https://raw.githubusercontent.com/yagmire/fabveri/main/links.json").text)
fabricURL = links["fabric"]
javaURL = links["java"]
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

req_snapshot = input(f"{colorama.Fore.BLUE}Use a snapshot version? (y or n)\n")

req_ver = input(f"What version of Minecraft?{colorama.Fore.WHITE}\n")

def ifSnapshot():
    if req_snapshot.lower() == "y":
        return "-snapshot"
    else:
        return ""
    
def cleanup():
    os.remove("fabricinstaller.jar")
    os.remove("java.tar.gz")
    shutil.rmtree("java")

print(f"Fabric installer: {os.path.isfile('fabricinstaller.jar')}")
print(f"Java: {os.path.isdir('./java')}")

if platform.platform() == "Linux":
    os.system(f"./java/jdk-17.0.9/bin/java -jar fabricinstaller.jar client {ifSnapshot()} -mcversion {req_ver}")
elif platform.platform() == "Windows":
    os.system(f"java/jdk-17.0.9/bin/java -jar fabricinstaller.jar client {ifSnapshot()} -mcversion {req_ver}")

cleanup()
print("Cleaned up.")
