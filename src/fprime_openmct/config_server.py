from pynpm import NPMPackage
import time
import os
import webbrowser
import fprime_openmct
import sys 

class ServerConfig:

    def install_npm_package(self):
        openmct_dir = fprime_openmct.__file__.replace('__init__.py', 'javascript')
        ServerConfig.pkg = NPMPackage(openmct_dir)
        # Check if an installation already exists. If not, install the node packages
        if not os.path.exists(openmct_dir + '/node_modules'):
            print("[INFO] Existing OpenMCT Server not found. Installing F-Prime to OpenMCT Bridge, and OpenMCT.")
            ServerConfig.pkg.install()
        else:
            print("[INFO] Existing OpenMCT Server Found. New F-Prime to OpenMCT Bridge installation not required.")

    def start_npm_package(self, pkg, delay=5):
        pkg.run_script('start', wait=False)
        time.sleep(delay)
        webbrowser.open_new_tab('http://localhost:8080')

    def install_openmct_server(self):
        openmct_dir = fprime_openmct.__file__.replace('__init__.py', 'javascript')
        self.install_npm_package()

    def launch_openmct_server(self):
        openmct_dir = fprime_openmct.__file__.replace('__init__.py', 'javascript')
        if not os.path.exists(openmct_dir + '/node_modules'):
            print("[INFO] Existing OpenMCT Server not found. Please run fprime-openmct-setup to install the F-Prime to OpenMCT Bridge and OpenMCT Servers!")
            sys.exit() 
        ServerConfig.pkg = NPMPackage(openmct_dir)
        self.start_npm_package(ServerConfig.pkg, delay=5)

def main():
    npm_server = ServerConfig()
    npm_server.install_openmct_server()

if __name__ == '__main__':
    main()

