from distutils.core import setup

setup(name='fprime_openmct',
      version='1.1',
      description='An FPrime to OpenMCT Bridge for Broadcasting F-Prime Registered Telemetry in OpenMCT',
      author='Mohit Singh',
      author_email='mohit.singh@jpl.nasa.gov',
      url= 'https://github.com/fprime-community/fprime-openmct',
      package_dir={'fprime_openmct': '',
                   'fprime_openmct.src.fprime_openmct': 'src/fprime_openmct'},
      packages=['fprime_openmct', 'fprime_openmct.src.fprime_openmct'],
      install_requires=['fprime_gds', 'fprime_tools', 'pynpm'],
      include_package_data=True,
      )