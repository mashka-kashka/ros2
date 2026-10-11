from setuptools import find_packages, setup
from glob import glob

package_name = 'qrobot_gui'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/icons', glob('icons/*.png')),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Maria',
    maintainer_email='maria.muravieva@mail.ru',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
    },
    entry_points={
        'console_scripts': [
            'control = qrobot_gui.control_node:main',
            'train = qrobot_gui.train_node:main',
        ],
    },
)
