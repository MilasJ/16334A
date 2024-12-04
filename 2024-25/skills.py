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
left = MotorGroup(Motor(Ports.PORT11, GearSetting.RATIO_18_1, True), Motor(Ports.PORT14, GearSetting.RATIO_18_1, True))
right = MotorGroup(Motor(Ports.PORT12),Motor(Ports.PORT13))
drivetrain = DriveTrain(left, right, 4*pi,10, 8, INCHES, 3/7)
lifterator = Motor(Ports.PORT1)
c15 = Controller()
myVariable = 0

needStopLeft = False
needStopRight = False
lifteratorStopped = True
#infinite loop for motors
def rc_auto_loop_function_controller_1():
    global needStopLeft, needStopRight, lifteratorStopped, remote_control_code_enabled
    while True:
        if remote_control_code_enabled:
            leftPos = c15.axis3.position() + c15.axis1.position()
            rightPos = c15.axis3.position() - c15.axis1.position()
            if -5 < leftPos < 5:
                if needStopLeft:
                    left.stop()
                    needStopLeft = False
            else:
                needStopLeft = True
            if -5 < rightPos < 5:
                if needStopRight:
                    right.stop()
                    needStopRight = False
            else:
                needStopRight = True
            if needStopLeft:
                left.set_velocity(((leftPos/100)**3)*100, PERCENT)#exponential drive for fine-tuning
                left.spin(FORWARD)
            if needStopRight:
                right.set_velocity(((rightPos/100)**3)*100, PERCENT)
                right.spin(FORWARD)
            if c15.buttonA.pressing(): #if pressing the A button
                lifterator.spin(FORWARD)#translation: lift goes up
                lifteratorStopped = False
            elif c15.buttonB.pressing(): #if pressing the B button
                lifterator.spin(REVERSE)#translation: lift goes down
                lifteratorStopped = False
            elif not lifteratorStopped: #if neither button is pressed
                lifterator.stop()#translation: lift stops moving
                lifteratorStopped = True
        wait(20,MSEC)
remote_control_code_enabled = True
rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)
def when_started1():
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.set_turn_velocity(100, PERCENT)
    lifterator.set_velocity(100, PERCENT)
def autonomousTasks():
    #TODO: push mobile goals to corners
    lifterator.spin(FORWARD)
    drivetrain.drive(FORWARD)
    wait(.5, SECONDS)
    drivetrain.stop()
    lifterator.spin(REVERSE)
    wait(.5, SECONDS)
    drivetrain.turn(RIGHT)
    wait(.5, SECONDS)
    lifterator.stop()
    drivetrain.drive(FORWARD)
def driverTasks():
    pass

def autonomousFunction():
    auton_task_0 = Thread(autonomousTasks)
    while(competition.is_autonomous() and competition.is_enabled()):
        wait(10, MSEC)
    auton_task_0.stop()
def driverFunction():
    driver_control_task_0 = Thread(driverTasks)
    while(competition.is_driver_control() and competition.is_enabled()):
        wait(10, MSEC)
    driver_control_task_0.stop()

competition = Competition(driverFunction, autonomousFunction)
when_started1()
