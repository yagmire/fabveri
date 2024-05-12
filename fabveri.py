import os, requests, tarfile, shutil, json, colorama
print("Fabveri\n")

# Get latest links
print("Getting latest dependencies download links.")
if os.path.isfile("links.json"):
    os.remove("links.json")
links = json.loads(requests.get("https://raw.githubusercontent.com/yagmire/fabveri/main/links.json").text)
fabricURL = links["fabric"]
javaURL = links["java"]
print("Receieved latest links.")

# Getting fabric installer
if os.path.isfile("fabricinstaller.jar"):
    print("Fabric installer already exists.")
    pass
else:
    r = requests.get(fabricURL, allow_redirects=True)
    open('fabricinstaller.jar', 'wb').write(r.content)
    print("Successfully downloaded fabric installer.")

# Getting java
if os.path.isdir("java"):
    print("Java already exists.")
    pass
else:
    r = requests.get(javaURL, allow_redirects=True)
    open('java.tar.gz', 'wb').write(r.content)
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

os.system(f"./java/jdk-17.0.9/bin/java -jar fabricinstaller.jar client {ifSnapshot()} -mcversion {req_ver}")

cleanup()
print("Cleaned up.")