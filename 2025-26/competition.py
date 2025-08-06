from vex import *
import urandom #type: ignore
from math import pi

brain = Brain()
wait(30,MSEC)

def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))

initializeRandomSeed()

def play_vexcode_sound(sound_name):
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

wait(200, MSEC)
print("\033[2J")

RED = 0
GREEN = 1
BLUE = 2

left = MotorGroup(Motor(Ports.Port1, GREEN, True), Motor(Ports.Port2, GREEN, True), Motor(Ports.Port3, GREEN, True))
right = MotorGroup(Motor(Ports.Port4, GREEN, True), Motor(Ports.Port5, GREEN, True), Motor(Ports.Port6, GREEN, True))
