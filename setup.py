from setuptools import setup, find_packages

setup(
    name='ghlog',
    version='1.1.3',
    description='A simple logbook that upload to github',
    url='https://github.com/lukew3/ghlog',
    author='Luke Weiler',
    author_email='lukew25073@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['pygithub', 'tqdm', 'click'],
    entry_points={
        'console_scripts': ['ghlog=ghlog.cli:cli'],
    },
)
