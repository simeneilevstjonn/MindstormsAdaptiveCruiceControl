#!/usr/bin/env pybricks-micropython
# (c) Simen Eilevstjønn 2021

# Imports
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import asyncio

# Global variables
poll_delay = 0.01
distancing = 3
track_threshold = 10

# ACC class
class AdaptiveCruiceControl:
    # Constructor
    def __init__(self, drive_base, ultrasonic_sensor, speaker):
        # Store variables
        self.drive_base = drive_base
        self.ultrasonic_sensor = ultrasonic_sensor
        self.speaker = speaker

    # Check if tracking
    def is_tracking(self):
        # Read the sensor and check wether it is within the threshold for the set speed
        return self.ultrasonic_sensor.distance() < self.set_speed * track_threshold

    # Get speed of tracking object. Assumes robot velocity stays the same for the entire period.
    async def track_speed(self, relative = False):
        # Get the initial distance to the tracked object
        initial_dist = self.ultrasonic_sensor.distance()

        # Wait for poll_delay period
        await asyncio.sleep(poll_delay)

        # Get the current distance to the tracked object
        current_dist = self.ultrasonic_sensor.distance()

        # Calculate speed differnce
        tracked_diff = (current_dist - initial_dist) / poll_delay

        # Return diff if param is true
        if relative:
            return tracked_diff
        # Else calculate and return absolute speed
        else:
            return tracked_diff + self.speed

    # Drive method. Call this to start cruice control
    async def drive(self, speed):
         # Start driving at given speed
        self.drive_base.drive(speed, 0)

        # Set speed variables
        self.set_speed = speed
        self.speed = speed

        # Set drive variable
        self.drive = True

        # While driving
        while self.drive:
            # Check if we are tracking an object
            if self.is_tracking():
                # Beep to signal we are tracking
                self.speaker.beep()

                # Get current relative speed
                relative_speed = await self.track_speed(True)

                # Loop until no longer tracking
                while self.is_tracking():
                    # Get the speed of tracked object
                    relative_speed = self.track_speed(True)

                    # Check if the relative speed is positive or negative
                    # If negative or positive but less than set speed
                    if relative_speed < 0 OR (relative_speed >= 0 AND (relative_speed + self.speed) < self.set_speed):
                        # Set speed to object's speed
                        self.drive_base.drive(relative_speed, 0)
                        self.speed = relative_speed
                    # Else
                    else:
                        # Set speed to set speed
                        self.drive_base.drive(self.set_speed, 0)
                        self.speed = self.set_speed

                    # Check if the distance should be corrected
                    if (distancing * self.speed) < self.ultrasonic_sensor.distance():
                        # Reduce speed by 5%. Increase should be handled by tracker
                        self.speed *= 0.95
                        self.drive_base.drive(self.set_speed, 0)
                    
                    # Delay
                    await asyncio.sleep(poll_delay)
                
                # Beep twice to signal we are no longer tracking
                self.speaker.beep()
                await asyncio.sleep(0.05)
                self.speaker.beep()

    # Set speed
    def set_speed(self, speed):
        self.set_speed = speed
    
    # Stop driving
    def stop_drive(self):
        self.drive = False  