from gpiozero import Motor
from gpiozero import RotaryEncoder

class motor_driver:
    def __init__(
        self,
        pin1,
        pin2,
        enc_phase1,
        enc_phase2,
        circumference,
        max_speed,
        pulses_per_revolution=64,
        freq=20000
    ):
       # initialize variables and objects. 
        self.freq = freq
        self.circumference = circumference
        self.max_speed = max_speed
        self.pulses_per_revolution = pulses_per_revolution
        
        # pin1 is IN1 and pin2 is IN2.
        self.motor = Motor(pin1, pin2)
        
        # enc_phase1 is phase A and enc_phase2 is phase B.
        self.encoder = RotaryEncoder(enc_phase1, enc_phase2) 
        self.encoder.steps = 0

    '''
    The speed parameter should be a float between -negative max_speed and positive max_speed. 
    A positive speed value will rotate the motor in one direction, while a negative speed value will rotate it in the opposite direction. 
    A speed of 0 will stop the motor.
    Most of the time, the motor is controlled by move_distance, which uses the encoder to determine when to stop.
    Speed is in METRIC units of m/s.
    '''
    def set_speed(self, speed):
        if speed > 0:
            self.motor.forward(speed / self.max_speed)
            self.motor.backward(0)
        elif speed < 0:
            self.motor.backward(-speed / self.max_speed)
            self.motor.forward(0)
        else:
            self.motor.forward(1)
            self.motor.backward(0)

    '''
    For other scripts to check the current encoder pulse count.
    '''
    def get_encoder_position(self):
        return self.encoder.steps
    
    '''
    Yields for other subsystems, drivers, and checks to run as the motor rotates.
    '''
    def motor_yielder(self, pulses_needed):
        try:
            while abs(self.get_encoder_position()) < abs(pulses_needed):
                yield
        finally:
            self.set_speed(0)
            self.encoder.when_rotated = None
        
    '''
    This function moves the motor a specified distance in meters (can be negative).
    speed is a MAGNITUDE value that determines how fast the motor should move. 
    The speed parameter should be a float between 0 and max_speed. (m/s)
    '''
    def move_distance(self, distance, speed):
        pulses_needed = int((distance / self.circumference) * self.pulses_per_revolution)
        self.encoder.steps = 0

        if pulses_needed < 0:
            speed = -speed

        self.set_speed(speed)
        self.encoder.when_rotated = self.motor_yielder(pulses_needed)