# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals
# @copyright ©2013, Rodrigo Cacilhας <batalema@cacilhas.info>

from os import path
import sys

sys.path.append(path.realpath(path.join(path.dirname(__file__), path.pardir)))

from unittest import main
from tests.test_lazy import *
from tests.test_context import *


if __name__ == '__main__':
    main()
