# Dyslexia Overlay
A lightweight easily toggle-able and customisable screen overlay to aid the reading of text for people with dyslexia.

![Example usage of this tool](https://github.com/patterson-tom/Dyslexia-Overlay/blob/master/example-image.png)

# Setup
Only tested with Python 3.8 and on Windows, but may work with earlier versions of Python and/or other operating systems.
The following packages are also required:
- [pynput](https://pypi.org/project/pynput/)
- [pyqt5](https://pypi.org/project/PyQt5/)

These are both installable using `pip install <package-name>`

# Usage
When run, the overlay is by default not shown. To show/hide the overlay use win+shift+o (or OS-equivalent although see above about OS-support). The overlay can be dragged around
the screen by clicking and dragging anywhere on the overlay, and resized as you would any other window. To adjust the colour and/or opacity of the window, right-click and a color
choosing dialog will be shown.
