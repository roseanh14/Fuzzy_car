import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

distance = ctrl.Antecedent(np.linspace(0, 120, 121), 'distance')

rel_speed = ctrl.Antecedent(np.linspace(-100, 100, 201), 'rel_speed')

traffic = ctrl.Antecedent(np.linspace(0, 10, 101), 'traffic')

accel = ctrl.Consequent(np.linspace(-5, 5, 201), 'accel')

distance['very_close'] = fuzz.trimf(distance.universe, [0, 0, 30])
distance['close']      = fuzz.trimf(distance.universe, [10, 30, 60])
distance['medium']     = fuzz.trimf(distance.universe, [40, 70, 100])
distance['far']        = fuzz.trimf(distance.universe, [80, 120, 120])

rel_speed['closing_fast']  = fuzz.trimf(rel_speed.universe, [-100, -100, -40])
rel_speed['closing']       = fuzz.trimf(rel_speed.universe, [-80, -40, 0])
rel_speed['stable']        = fuzz.trimf(rel_speed.universe, [-10, 0, 10])
rel_speed['opening']       = fuzz.trimf(rel_speed.universe, [0, 40, 80])
rel_speed['opening_fast']  = fuzz.trimf(rel_speed.universe, [40, 100, 100])

traffic['low']    = fuzz.trimf(traffic.universe, [0, 0, 3])
traffic['medium'] = fuzz.trimf(traffic.universe, [2, 5, 8])
traffic['high']   = fuzz.trimf(traffic.universe, [7, 10, 10])

accel['strong_brake']      = fuzz.trimf(accel.universe, [-5, -5, -2.5])
accel['brake']             = fuzz.trimf(accel.universe, [-4, -2, -0.5])
accel['zero']              = fuzz.trimf(accel.universe, [-1, 0, 1])
accel['accelerate']        = fuzz.trimf(accel.universe, [0.5, 2, 4])
accel['strong_accelerate'] = fuzz.trimf(accel.universe, [2.5, 5, 5])

rule_list = [

    ctrl.Rule(distance['very_close'] & rel_speed['closing_fast'],
              accel['strong_brake']),
    ctrl.Rule(distance['very_close'] & rel_speed['closing'],
              accel['strong_brake']),
    ctrl.Rule(distance['very_close'],
              accel['strong_brake']),

    ctrl.Rule(distance['close'] & rel_speed['closing_fast'],
              accel['strong_brake']),
    ctrl.Rule(distance['close'] & rel_speed['closing'] & traffic['high'],
              accel['strong_brake']),
    ctrl.Rule(distance['close'] & rel_speed['closing'] & traffic['medium'],
              accel['brake']),

    ctrl.Rule(distance['close'] & rel_speed['stable'] & traffic['high'],
              accel['brake']),
    ctrl.Rule(distance['close'] & rel_speed['stable'] & traffic['low'],
              accel['zero']),

    ctrl.Rule(distance['medium'] & rel_speed['closing_fast'],
              accel['brake']),
    ctrl.Rule(distance['medium'] & rel_speed['closing'],
              accel['brake']),

    ctrl.Rule(distance['medium'] & rel_speed['stable'] & traffic['low'],
              accel['accelerate']),
    ctrl.Rule(distance['medium'] & rel_speed['stable'] & traffic['medium'],
              accel['zero']),

    ctrl.Rule(distance['medium'] & rel_speed['opening'] & traffic['low'],
              accel['strong_accelerate']),
    ctrl.Rule(distance['medium'] & rel_speed['opening'] & traffic['medium'],
              accel['accelerate']),
    ctrl.Rule(distance['medium'] & rel_speed['opening'] & traffic['high'],
              accel['zero']),

    ctrl.Rule(distance['far'] & rel_speed['opening'] & traffic['low'],
              accel['strong_accelerate']),
    ctrl.Rule(distance['far'] & rel_speed['opening_fast'] & traffic['low'],
              accel['strong_accelerate']),
    ctrl.Rule(distance['far'] & traffic['high'],
              accel['accelerate']),
    ctrl.Rule(distance['far'] & traffic['medium'],
              accel['accelerate']),
]


accel_ctrl = ctrl.ControlSystem(rule_list)
