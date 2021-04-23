from setuptools import setup
from FourierDrawing_brd import __version__ as current_version

setup(
  name='FourierDrawing_brd',
  version=current_version,
  description='Fourier drawing',
  url='https://github.com/StephaneSadddio/packaging_tutorial',
  author='Stephane SADIO',
  author_email='stephane.sadio@etu.umontpellier.fr',
  license='MIND',
  packages=['FourierDrawing_brd','FourierDrawing_brd.Image', 'FourierDrawing_brd.FourierApproximation',
   'FourierDrawing_brd.Circles','FourierDrawing_brd.Animate_FT'],
  zip_safe=False
)