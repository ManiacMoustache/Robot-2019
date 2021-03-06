    # -*- coding: utf-8 -*-

import rev
import ctre 


def createMotor(motorDescp):
    #Might want more motor types for set up
    '''This is where all motors are set up'''
    if motorDescp['type'] == 'CANTalon':
        #if we want to use the built in encoder set it here
        if('pid' in motorDescp) and motorDescp['pid'] != None:
            motor = WPI_TalonFeedback(motorDescp)
            motor.setupPid()
        else:
            motor = ctre.wpi_talonsrx.WPI_TalonSRX(motorDescp['channel'])

    elif motorDescp['type'] == 'CANTalonFollower':
        motor =ctre.wpi_talonsrx.WPI_TalonSRX(motorDescp['channel'])
        motor.set(ctre.wpi_talonsrx.ControlMode.Follower, motorDescp['masterChannel'])
        
    elif motorDescp['type'] == 'SparkMax':
        '''This is where SparkMax motor controllers are set up'''
        motor = rev.CANSparkMax(motorDescp['channel'], motorDescp['motorType'])
        
    else:
        print("Unknown Motor")
    
    if 'inverted' in motorDescp: 
        motor.setInverted(motorDescp['inverted'])
    
    if 'currentLimits' in motorDescp:
        currentLimits = motorDescp['currentLimits']
        absMax = currentLimits['absMax']
        absMaxTimeMs = currentLimits['absMaxTimeMs']
        nominalMaxCurrent = currentLimits['maxNominal']
        motor.configPeakCurrentLimit(absMax,10)
        motor.configPeakCurrentDuration(absMaxTimeMs,10)
        motor.configContinuousCurrentLimit(nominalMaxCurrent,10)
        motor.enableCurrentLimit(True)

    if 'rampRate' in motorDescp:
        motor.configOpenLoopRamp(motorDescp['rampRate'],10)    
    
    return motor
#motor=map.CAN.driveMotors[name]
#            motors[name]=ctre.wpi_talonsrx.WPI_TalonSRX(motor['channel'])
#            motors[name]=ctre.wpi_talonsrx.WPI_TalonSRX(motor['channel'])
#            
#            motors[name] = wpilib.PWMSpeedController(motor['channel'])
#            
        

class WPI_TalonFeedback(ctre.wpi_talonsrx.WPI_TalonSRX):
    def __init__(self,motorDescription):
        ctre.wpi_talonsrx.WPI_TalonSRX.__init__(self,motorDescription['channel'])
        self.motorDescription = motorDescription
    def setupPid(self,motorDescription = None):
        if not motorDescription:
            motorDescription = self.motorDescription
        if not 'pid' in self.motorDescription:
            print("Motor channel %d has no PID"%(self.motorDescription['channel']))
            return
        pid = self.motorDescription['pid']
        self.controlType = pid['controlType']
        self.configSelectedFeedbackSensor(pid['feedbackType'], 0, 10)
        self.setSensorPhase(pid['sensorPhase'])
        self.pidControlType = pid['controlType']
        
        self.kInput = pid['kInput']
        
        #/* set the peak, nominal outputs, and deadband */
        self.configNominalOutputForward(0, 10);
        self.configNominalOutputReverse(0, 10);
        self.configPeakOutputForward(1, 10);
        self.configPeakOutputReverse(-1, 10);
        
        
        self.configVelocityMeasurementPeriod(self.VelocityMeasPeriod.Period_1Ms,10);
        #/* set closed loop gains in slot0 */
        self.config_kF(0, pid['kF'], 10)
        self.config_kP(0, pid['kP'], 10)
        self.config_kI(0, pid['kI'], 10)
        self.config_kD(0, pid['kD'], 10)
        
        
    def set(self, speed):
        return ctre.wpi_talonsrx.WPI_TalonSRX.set(self, self.controlType, speed * self.kInput)
            
class SparkMaxFeedback(rev.CANSparkMax):
    def __init__(self, motorDescp):
        rev.CANSparkMax.__init__(self, motorDescp['channel'], motorDescp['motorType'])
        self.motorDescp = motorDescp
