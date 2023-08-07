from pynpm import NPMPackage
import time
import os
import webbrowser

"Registers Python object of Node Server given a package.json"
def register_npm_package(fpath="~"):
    pkg = NPMPackage(fpath)
    return pkg

def install_npm_package(pkg, openmct_path=''):
    # Check if an installation already exists. If not, install the node packages
    if not os.path.exists(openmct_path + 'node_modules'):
        print("[INFO] Existing OpenMCT Server not found. Installing F-Prime to OpenMCT Bridge, and OpenMCT.")
        pkg.install()
    else:
        print("[INFO] Existing OpenMCT Server Found. New F-Prime to OpenMCT Bridge installation not required.")

def start_npm_package(pkg, delay=2):
    pkg.run_script('start', wait=False)
    time.sleep(delay)
    webbrowser.open_new_tab('http://localhost:8080')
