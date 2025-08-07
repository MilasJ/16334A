#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration
from math import pi

RED = 0
GREEN = 1
BLUE = 2

left = MotorGroup(Motor(Ports.Port1, GREEN, True), Motor(Ports.Port2, GREEN, True), Motor(Ports.Port3, GREEN, True))
right = MotorGroup(Motor(Ports.Port4, GREEN, True), Motor(Ports.Port5, GREEN, True), Motor(Ports.Port6, GREEN, True))
drivetrain = DriveTrain(left, right, 2.75*pi, 13, 10.5, INCHES, 4/3)

controller= Controller()

def drive():
    drive_left = 0
    drive_right = 0

    while True:
        pass