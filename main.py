#!/usr/bin/env pybricks-micropython
# (c) Simen Eilevstjønn 2021

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import acc


# Create your objects here.
ev3 = EV3Brick()

# Initialise the motors.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Create instance of acc class
adaptivecc = AdaptiveCruiseControl(DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104), UltrasonicSensor(Port.S4), ev3.speaker)

# Start driving at 200 mm/s
adaptivecc.drive(200)

