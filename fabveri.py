import os, requests, tarfile, shutil, json, colorama, platform, zipfile, pyfiglet
from tqdm import tqdm
from sys import exit
from time import sleep

print(pyfiglet.figlet_format("fabveri", font="alligator"))

# OS Detect
if platform.system() != "Linux":
    if platform.system() != "Windows":
        print("Unsupported system.")
        exit()

# Download warning
print(f"{colorama.Fore.YELLOW}Downloading 3 prerequisites, do not close the application while this is occuring. It may seem like the program is frozen. Starting in 3 seconds.{colorama.Fore.WHITE}")
sleep(3)

# Get latest links
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
    open('fabricinstaller.jar', 'wb').write(r.content)
    print("Successfully downloaded fabric installer.")

# Getting java
if platform.system() == "Linux":
    if os.path.isdir("java"):
        print("Java already exists.")
    else:
        r = requests.get(javaURL, stream=True)
        open('java.tar.gz', 'wb').write(r.content)
        java = tarfile.open('java.tar.gz') 
        java.extractall('./java')
        java.close()
        print("Successfully downloaded java.")

elif platform.system() == "Windows":
    if os.path.isdir("java"):
        print("Java already exists.")
    else:
        r = requests.get(javaURL, stream=True)
        open('java.zip', 'wb').write(r.content)
        with zipfile.ZipFile("java.zip", 'r') as zip_ref:
            zip_ref.extractall("java")
        print("Successfully downloaded java.")

def modLocalInstall():
    if os.path.isdir("mods") == False:
        os.mkdir("mods")
    if platform.system() == "Windows":
        input("Press ENTER when you have all your mods in the mods folder.")
        if os.path.isdir(f"{os.getenv('APPDATA')}\\.minecraft\\mods"):
            if os.path.isdir(f"{os.getenv('APPDATA')}\\.minecraft\\mods"):
                shutil.rmtree(f"{os.getenv('APPDATA')}\\.minecraft\\mods")
            os.system(f"xcopy {os.getcwd()}\\mods {os.getenv('APPDATA')}\\.minecraft\\mods /E /C /H /I")
        #shutil.copytree("mods", f"{os.getenv('APPDATA')}\\.minecraft\\mods")
    else:
        print(f"Local mod install is not supported for your platform ({platform.system()}) yet.")

req_snapshot = input(f"{colorama.Fore.BLUE}Use a snapshot version? (y or n)\n{colorama.Fore.WHITE}")

req_ver = input(f"{colorama.Fore.BLUE}What version of Minecraft?{colorama.Fore.WHITE}\n")

ask_install_mods = input(f"{colorama.Fore.BLUE}Do you want to install mods automatically?\n{colorama.Fore.YELLOW}THIS WILL DELETE ALL EXISTING MODS INSIDE THE MODS FOLDER{colorama.Fore.WHITE}\n")

def ifSnapshot():
    if req_snapshot.lower() == "y":
        return "-snapshot"
    else:
        return ""
    
def cleanup():
    if platform.system() == 'Linux':
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
    elif platform.system() == "Windows":
        # Fabric installer
        try:
            os.remove("fabricinstaller.jar")
        except Exception as e:
            print(f"\n{colorama.Fore.RED}There was an error deleting the fabric installer.\n{e}{colorama.Fore.WHITE}\n")
        
        # Java archive
        try:
            if os.path.isfile("java.zip"):
                os.remove("java.zip")
            else:
                print("Java.zip doesn't exist so not deleting.")
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
    print(f"Running system ({platform.system()}) command: {operation}")
    os.system(operation)
elif platform.system() == "Windows":
    operation = f"java\\jdk-17.0.9\\bin\\java.exe -jar fabricinstaller.jar client {ifSnapshot()} -mcversion {req_ver}"
    print(f"Running system ({platform.system()}) command: {operation}")
    os.system(operation)
    if ask_install_mods.lower()[:1] == "y":
        modLocalInstall()
        print("Installed mods.")

cleanup()
print(f"Cleaned up.\n{colorama.Fore.GREEN}Now closing.{colorama.Fore.WHITE}")
exit()
