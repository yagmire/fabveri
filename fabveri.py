import os, requests, sys, tarfile, shutil
print("Fabveri\n")
fabricURL = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.0.1/fabric-installer-1.0.1.jar"
javaURL = "https://download.oracle.com/java/17/archive/jdk-17.0.9_linux-x64_bin.tar.gz"
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

req_snapshot = input("Use a snapshot version? (y or n)\n")

req_ver = input("What version of Minecraft?\n")

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