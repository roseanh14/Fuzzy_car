from skfuzzy import control as ctrl
from fuzzy_system_config import accel_ctrl  


def evaluate_fis(distance_val: float, rel_speed_val: float, traffic_val: float) -> float:

    sim = ctrl.ControlSystemSimulation(accel_ctrl)

    sim.input['distance'] = distance_val
    sim.input['rel_speed'] = rel_speed_val
    sim.input['traffic'] = traffic_val

    sim.compute()

    return float(sim.output['accel'])


def verbal_description(a: float) -> str:

    if a < -3:
        return "strong braking"
    elif a < -1:
        return "mild braking"
    elif a < 1:
        return "keep current speed"
    elif a < 3:
        return "mild acceleration"
    else:
        return "strong acceleration"
