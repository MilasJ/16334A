#region VEXcode Generated Robot Configuration
from vex import *
from os import urandom

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
lifterator = MotorGroup(Motor(Ports.PORT19, 0), Motor(Ports.PORT20, 0, True))
c15 = Controller()
myVariable = 0

needStopLeft = False
needStopRight = False
lifteratorStopped = True
#infinite loop for motors
#TODO: #3 change drivetrain to RC controls
def rc_auto_loop_function_controller_1():
    global needStopLeft, needStopRight, lifteratorStopped, remote_control_code_enabled
    while True:
        if remote_control_code_enabled:
            leftPos = c15.axis3.position()#we're using tank controls for now, will change later
            rightPos = c15.axis2.position()
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
            if c15.buttonR1.pressing() or c15.buttonR2.pressing():
                #if either or both right shoulder buttons pressed
                lifterator.spin(FORWARD)#translation: lift goes up
                lifteratorStopped = False
            elif c15.buttonL1.pressing() or c15.buttonL2.pressing():
                #if either or both left shoulder buttons pressed
                lifterator.spin(REVERSE)#translation: lift goes down
                lifteratorStopped = False
            elif not lifteratorStopped:
                #if no shoulder buttons pressed
                lifterator.stop()#translation: lift stops moving
                lifteratorStopped = True
        wait(20,MSEC)
remote_control_code_enabled = True
rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)
def when_started1():
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.set_turn_velocity(100, PERCENT)
    lifterator.set_max_torque(100, PERCENT)
    lifterator.set_stopping(HOLD)#lift stops immediately and locks in place
def autonomousTasks(): #TODO #4 change direction
    lifterator.spin(FORWARD)#lifterator goes up
    drivetrain.drive(FORWARD)#robot moves forward
    wait(1.5,SECONDS)#time it takes to bump into the ladder
    drivetrain.stop()
def driverTasks():
    pass #we have nothing here

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