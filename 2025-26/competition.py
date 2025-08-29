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

left = MotorGroup(Motor(Ports.PORT1, GREEN, True), Motor(Ports.PORT2, GREEN, True), Motor(Ports.PORT3, GREEN))
right = MotorGroup(Motor(Ports.PORT4, GREEN), Motor(Ports.PORT5, GREEN), Motor(Ports.PORT6, GREEN, True))
drivetrain = DriveTrain(left, right, 2.75*pi, 13, 10.5, INCHES, 4/3)

controller= Controller()
intake = Motor(Ports.PORT7, BLUE)

def drive_function():
    drive_left = 0
    drive_right = 0

    while True:
        drive_left = controller.axis3.position() + controller.axis1.position()
        drive_right = controller.axis3.position() - controller.axis1.position()
        move_intake = 100 if controller.buttonA.pressing() else -100 if controller.buttonB.pressing() else 0

        deadband = 15
        drive_left *= int(abs(drive_left) >= deadband)
        drive_right *= int(abs(drive_right) >= deadband)

        left.spin(FORWARD, drive_left, PERCENT)
        right.spin(FORWARD, drive_right, PERCENT)
        intake.spin(FORWARD, move_intake, PERCENT) if abs(move_intake) else intake.stop(COAST)
        sleep(10)

drive = Thread(drive_function)

def setup():
    drivetrain.set_drive_velocity(50, PERCENT)
    intake.set_velocity(100, PERCENT)
setup()