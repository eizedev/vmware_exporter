from setuptools import setup, find_packages
from pathlib import Path
import vmware_exporter

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='vmware_exporter',
    version=vmware_exporter.__version__,
    author=vmware_exporter.__author__,
    description='VMWare VCenter Exporter for Prometheus',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/pryorda/vmware_exporter',
    download_url=("https://github.com/pryorda/vmware_exporter/tarball/%s" %
                  vmware_exporter.__version__),
    keywords=['VMWare', 'VCenter', 'Prometheus'],
    license=vmware_exporter.__license__,
    packages=find_packages(exclude=['*.test', '*.test.*']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'vmware_exporter=vmware_exporter.vmware_exporter:main'
        ]
    },
)
