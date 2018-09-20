import os
from setuptools import setup



setup(
    name="axis-and-allies",
    version="1.0.0",
    author="Per-Arne Andersen",
    author_email="per@sysx.no",
    description="gym bindings for FlashRL",
    license="MIT",
    keywords="axis-and-allies strategy-game reinforcement-learning deep-learning machine-learning research educational",
    url="https://github.com/cair/Axis_and_Allies",
    install_requires=[
        'numpy', "pygame", "pillow"
    ],

    packages=[
        'axis_and_allies',
        'axis_and_allies.map_generator',
        'gym_aa',
        'gym_aa.envs'
    ],
    package_data={'': []},
    classifiers=[],
)