from setuptools import setup

setup(name='python-audio-test',
      version='0.1',
      description='playground for audio processing in python',
      url='https://github.com/throni3git/python-audio-test',
      author='Thomas Thron',
      license='',
      install_requires=[
          'autopep8',
          'numpy',
          'PyAudio',
          'pylint',
          'scipy',
          'samplerate',
          'soundfile',
          'soundcard',
          'sounddevice',
      ],
      python_requires='>=3.6'
      )
