
import wpilib.xboxcontroller
import hal
from rev import MotorType
class RobotMap():
    """
    Robot map gathers all the hard coded values needed to interface with 
    hardware into a single location
    """
    def __init__(self):
        """intilize the robot map"""
        self.motorsMap = CANMap()
        self.pneumaticsMap = PneumaticsMap()
        self.controllerMap = ControllerMap()

        
        
        

class CANMap():
    def __init__(self):
        '''
        holds mappings to all the motors in the robot
        '''
        rampRate = .2
        shooterRampRate = .2
        #rotRampRate = .2
        pid = None
        shooterPid = None
        rotPid = None
        shooterMotors = {}
        driveMotors = {}
        '''The code below is an example of code for the SparkMax motor controllers'''
        shooterMotors['RotMotor'] = {'channel':4, 'inverted':False, 'type':'SparkMax', 'pid':rotPid, 'motorType':MotorType.kBrushless}
        '''The code below is for controlling TalonSRX motor controllers as well as their followers'''
        shooterMotors['LeftFlyWheel'] = {'channel':5, 'inverted':False, 'type':'CANTalon', 'pid':shooterPid, "rampRate":shooterRampRate}
        shooterMotors['RightFlyWheel'] = {'channel':6, 'inverted':True, 'type':'CANTalonFollower', 'masterChannel':5, "rampRate":shooterRampRate}
        #shooterMotors['RotMotor'] = {'channel': 4, 'inverted':False, 'type':'CANTalon', 'pid': rotPid, "rampRate":rotRampRate}
        driveMotors['leftMotor'] = {'channel':0, 'inverted':False, 'type':'CANTalon', 'pid':pid, "rampRate":rampRate}
        driveMotors['leftFollower'] = {'channel':3, 'inverted':False, 'type':'CANTalonFollower', 'masterChannel':0, "rampRate":rampRate}
        driveMotors['rightMotor'] = {'channel':1, 'inverted':False, 'type':'CANTalon', 'pid':pid, "rampRate":rampRate}
        driveMotors['rightFollower'] = {'channel':2, 'inverted':False, 'type':'CANTalonFollower', 'masterChannel':1, "rampRate":rampRate}
        
        self.driveMotors = driveMotors
        self.shooterMotors = shooterMotors

class PneumaticsMap():
    def __init__(self):
        pass
    
class ControllerMap():
    def __init__(self):
        '''creates two controllers and assigns
        axis and buttons to joysticks'''
        driverController = {}
        auxController = {}
        
        driverController['controllerId'] = 0
        auxController['controllerId'] = 1
        
        driverController['leftTread'] = 1
        if hal.isSimulation():
            driverController['rightTread'] = 3
        else:
            driverController['rightTread'] = 5
        
        driverController['ledToggle'] = wpilib.XboxController.Button.kX
        driverController['alignButton'] = wpilib.XboxController.Button.kA
        driverController['leftButton'] = wpilib.XboxController.Button.kBumperLeft
        driverController['rightButton'] = wpilib.XboxController.Button.kBumperRight
        
        auxController['rotAxis'] = 1
        auxController['flyWheelTrigger'] = 3
        auxController['intakeButton'] = wpilib.XboxController.Button.kBumperLeft
        
        driverController['voltRumble'] = 8.0
        
        self.driverController = driverController
        self.auxController = auxController
        
