#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame

from Controller.Basic_Controller import Controller

__author__ = "Diego Bano"
__license__ = "GPL"
__version__ = "2.0.0"
__email__ = "diego.bano@ug.uchile.cl"

program = Controller()

while True:
    program.update()
    pygame.time.wait(1000 / 50)
