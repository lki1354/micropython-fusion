# Simple test program for sensor fusion on Pyboard
# Author: Lukas K.
# coauthor: Peter Hinch
# V0.7 25th June 2015 Adapted for new MPU9x50 interface

from machine import I2C, Pin
import time
from mpu9250 import MPU9250
from fusion import Fusion

#sw_pin = Pin(Pin.exp_board.G17, mode=Pin.IN, pull=Pin.PULL_UP)

i2c = I2C(0, I2C.MASTER, baudrate=400000)
imu = MPU9250(i2c)

fuse = Fusion()

# Choose test to run
Calibrate = True
Timing = False

time_calibration = time.time() + 20

def getmag():
    """
    Return (x, y, z) tuple (blocking read)
    """
    return imu.mag.xyz


def switch():
    if time.time() > time_calibration:
        return True
    else:
        return False
    # todo can't use the button on the expander board because this is used for the I2C interface
    #pressed = Pin.exp_board.G17.value()
    #if pressed:
    #    pressed = False
    #else:
    #    pressed = True
    #return pressed


if Calibrate:
    print("Calibrating. Press switch when done.")
    fuse.calibrate(getmag, switch, lambda: time.sleep_ms(100))
    print(fuse.magbias)

if Timing:
    mag = imu.mag.xyz  # Don't include blocking read in time
    accel = imu.accel.xyz  # or i2c
    gyro = imu.gyro.xyz
    start = time.ticks_ms()
    fuse.update(accel, gyro, mag) # 1.65mS on Pyboard
    t = time.ticks_ms() - start
    print("Update time (uS):", t)

count = 0
while True:
    fuse.update(imu.accel.xyz, imu.gyro.xyz, imu.mag.xyz) # Note blocking mag read
    if count % 50 == 0:
        print("Heading, Pitch, Roll: {:7.3f} {:7.3f} {:7.3f}".format(fuse.heading, fuse.pitch, fuse.roll))
    time.sleep_ms(20)
    count += 1
