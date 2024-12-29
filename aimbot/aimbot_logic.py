import numpy as np

def calculate_angle(source, target):
    delta = np.array(target) - np.array(source)
    yaw = np.arctan2(delta[1], delta[0]) * (180 / np.pi)
    pitch = np.arctan2(delta[2], np.linalg.norm(delta[:2])) * (180 / np.pi)
    return yaw, pitch

def aim_at_target(current_angle, target_angle, sensitivity=1.0):
    diff_yaw = target_angle[0] - current_angle[0]
    diff_pitch = target_angle[1] - current_angle[1]

    adjusted_yaw = current_angle[0] + diff_yaw * sensitivity
    adjusted_pitch = current_angle[1] + diff_pitch * sensitivity

    return adjusted_yaw, adjusted_pitch
