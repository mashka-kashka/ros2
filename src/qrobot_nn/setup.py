from setuptools import find_packages, setup
from glob import glob

package_name = 'qrobot_nn'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Maria Muravieva',
    maintainer_email='maria.muravieva@mail.ru',
    description='Пакет для работы с нейронными сетями',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'gesture_recognizer_node = qrobot_nn.gesture_recognizer_node:main'
        ],
    },
)
