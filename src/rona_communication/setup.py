from setuptools import find_packages, setup

package_name = 'rona_communication'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/keyboard_to_velocity.launch.py'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='alberto',
    maintainer_email='alberto.vicentechacon@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'keyboard_to_velocity = rona_communication.keyboard_to_velocity:main',
            'xbox_controller_to_velocity = rona_communication.xbox_controller_to_velocity:main'
        ],
    },
)
