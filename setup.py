from setuptools import setup, find_packages, Extension
import os
import numpy

version = "0.0.3"

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

extra_requirements = [
    "hidapi",
    "hid==1.0.4",
    "pyglm",
    "scipy",
    "ansitable",
    "progress",
    "typing_extensions",
    "ipykernel",
    "matplotlib",
    "pynput==1.7.7",
    "numpy==1.24.4",
    "spatialmath-python>=1.1.5",
    "spatialgeometry>=1.0.0",
    "tqdm",
    "feetech-servo-sdk",
    "mujoco==3.2.5"
]

install_requires = extra_requirements

extra_folders = [
    "bocon/kinematics/core",
]

def package_files(directory):
    paths = []
    for (pathhere, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", pathhere, filename))
    return paths


extra_files = []
for extra_folder in extra_folders:
    extra_files += package_files(extra_folder)

frne = Extension(
    "bocon/kinematics.frne",
    sources=[
        "./bocon/kinematics/core/vmath.c",
        "./bocon/kinematics/core/ne.c",
        "./bocon/kinematics/core/frne.c",
    ],
    include_dirs=["./bocon/kinematics/core/"],
)

fknm = Extension(
    "bocon/kinematics.fknm",
    sources=[
        "./bocon/kinematics/core/methods.cpp",
        "./bocon/kinematics/core/ik.cpp",
        "./bocon/kinematics/core/linalg.cpp",
        "./bocon/kinematics/core/fknm.cpp",
    ],
    include_dirs=["./bocon/kinematics/core/", numpy.get_include()],
)

setup(
    name='bocon',
    version=version,
    description='Bimanual Open Controller for Affordable Embodied AI Teleoperation',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='boxjod, Huanxu Lin',
    author_email=', '.join([
        'boxjod@163.com',
        "linhxforeduct@outlook.com"
    ]),
    url='https://github.com/box2ai-robotics/bocon',
    license=license,
    packages=find_packages(),
    install_requires=install_requires,  
    classifiers=[
        'Programming Language :: Python :: 3.7'
    ],
    ext_modules=[frne, fknm],
    package_data={"bocon/kinematics": extra_files},
)

