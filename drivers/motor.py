from gpiozero import Motor

class Drivetrain:
    def __init__(self, motorLeftIN1, motorLeftIN2, motorRightIN1, motorRightIN2):
        self.motorLeft = Motor(forward = motorLeftIN1, backward = motorLeftIN2)
        self.motorRight = Motor(forward = motorRightIN1, backward = motorRightIN2)

    def brake(self):
        self.motorLeft.stop()
        self.motorRight.stop()

    def leftMove(self, speed):
        if speed < 0:
            self.motorLeft.backward(speed * -1)
        elif speed > 0:
            self.motorLeft.forward(speed)
        else:
            self.motorLeft.stop()

    def rightMove(self, speed):
        if speed < 0:
            self.motorRight.backward(speed * -1)
        elif speed > 0:
            self.motorRight.forward(speed)
        else:
            self.motorRight.stop()

    def move(self, speed):
        self.leftMove(speed)
        self.rightMove(speed)

    def reverseLeft(self):
        self.motorLeft.reverse()

    def reverseRight(self):
        self.motorRight.reverse()

    def reverse(self):
        self.reverseLeft()
        self.reverseRight()

    def getLeftSpeed(self):
        return self.motorLeft.value
    
    def getRightSpeed(self):
        return self.motorRight.value

    def isMoving(self):
        return self.motorLeft.is_active or self.motorRight.is_active