# region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain = Brain()

# Robot configuration code


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = (
        brain.battery.voltage(MV)
        + brain.battery.current(CurrentUnits.AMP) * 100
        + brain.timer.system_high_res()
    )
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

# endregion VEXcode Generated Robot Configuration
from math import pi

# These are assigned for readability regarding motor cartridges.
RED = 0
GREEN = 1
BLUE = 2

controller = Controller()  # We only use a primary controller.

# Ports are pretty much assigned sequentially in order of necessity:
# The first six ports are the drivetrain,
left = MotorGroup(
    Motor(Ports.PORT1, GREEN, True),
    Motor(Ports.PORT2, GREEN, True),
    Motor(Ports.PORT3, GREEN, False),
)
right = MotorGroup(
    Motor(Ports.PORT4, GREEN, False),
    Motor(Ports.PORT5, GREEN, False),
    Motor(Ports.PORT6, GREEN, True),
)
drivetrain = DriveTrain(left, right, 2.75 * pi, 13, 10.5, INCHES, 4 / 3)

controller = Controller()
# The next two ports are the intake,
intake = MotorGroup(Motor(Ports.PORT7), Motor(Ports.PORT8, GREEN, True))
# The next port is scoring,
scoring = Motor(Ports.PORT9, BLUE)
# And our only three-wired port is the match loader de-loader.
match_loader = DigitalOut(brain.three_wire_port.a)  # Pneumatics! Yay!


def drive_function():
    """Read controller input and move parts accordingly."""
    drive_left = 1
    drive_right = 0
    button_free = {"A": True, "B": True}
    intake_moving = False
    intake_reverse = False

    # This big forever loop runs one hundred times a second.
    while True:
        # The drivetrain uses rc controls:
        # the left joystick drives forward and backward,
        # and the right joystick steers
        drive_left = controller.axis3.position() + controller.axis1.position()
        drive_right = controller.axis3.position() - controller.axis1.position()
        deadband = 15
        drive_left *= int(abs(drive_left) >= deadband)
        drive_right *= int(abs(drive_right) >= deadband)
        left.spin(FORWARD, drive_left, PERCENT)
        right.spin(FORWARD, drive_right, PERCENT)

        # The intake has some interesting settings:
        # the A button makes it spin, and the B button makes it stop.
        # If the intake is already spinning when A is pressed,
        # it reverses, expelling blocks instead of receiving them.
        # In this file, for skills, expulsion is set to half the speed as intake.
        # I also have it set to always start by spinning inward.
        if button_free["A"] and controller.buttonA.pressing():
            brain.screen.print("A")
            intake_reverse = not intake_reverse if intake_moving else False
            intake_moving = True
        elif button_free["B"] and controller.buttonB.pressing():
            intake_moving = False
            brain.screen.print("B")
        intake.spin(
            FORWARD if not intake_reverse else REVERSE,
            int(intake_moving) * (50 if intake_reverse else 100),
            PERCENT,
        )
        button_free = {
            "A": not controller.buttonA.pressing(),
            "B": not controller.buttonB.pressing(),
        }

        # The match loader needs to be able to move out of the way
        # Thus, {button} makes it move out of the way,
        # and {button} makes it come back to do its job
        if controller.buttonX.pressing():
            match_loader.set(False)
        elif controller.buttonY.pressing():
            match_loader.set(True)

        # The scoring is rather simple:
        # the up button makes the conveyor belt move blocks up,
        # and the down button makes the conveyor belt move down.
        if controller.buttonUp.pressing():
            scoring.spin(FORWARD)
        elif controller.buttonDown.pressing():
            scoring.spin(REVERSE)
        elif controller.buttonLeft.pressing():
            scoring.stop()
        sleep(10)


drive = Thread(drive_function)


# The following three functions are integral to running matches.
def setup():
    """Runs before the match starts."""
    drivetrain.set_drive_velocity(50, PERCENT)
    intake.set_velocity(100, PERCENT)
    scoring.set_velocity(100, PERCENT)
    match_loader.set(False)  # for size purposes


def auton():
    """Runs during the fifteen second autonomous period."""
    match_loader.set(True)  # might not need this. determine auton later


def driver():
    """Runs during the driving period."""
    while True:
        wait(10, MSEC)


comp = Competition(auton, driver)
setup()
