
import math
from scipy.interpolate import interp1d

class CirculationPump:
    def __init__(self):
        self.speed = 100  # 0–100 %

        self.pump_curves = {
            100: [(0.1, 7.6), (0.5, 7.5), (1.0, 7.2), (2.0, 6.0), (3.0, 4.2), (4.0, 2.5)],
            80:  [(0.1, 6.4), (0.5, 6.3), (1.0, 6.0), (2.0, 4.8), (3.0, 3.0), (4.0, 1.5)],
            60:  [(0.1, 4.8), (0.5, 4.7), (1.0, 4.5), (2.0, 3.2), (3.0, 1.8), (4.0, 0.5)],
            40:  [(0.1, 3.2), (0.5, 3.1), (1.0, 2.8), (2.0, 1.8), (3.0, 0.9), (4.0, 0.2)],
            20:  [(0.1, 1.5), (0.5, 1.4), (1.0, 1.2), (2.0, 0.7), (3.0, 0.3), (4.0, 0.0)],
        }

        self.interpolators = {}
        for speed, points in self.pump_curves.items():
            x, y = zip(*points)
            self.interpolators[speed] = interp1d(x, y, kind='cubic', fill_value='extrapolate')

    def set_speed(self, speed_percent):
        self.speed = max(20, min(100, speed_percent))

    def get_head(self, flow_m3h):
        speed_levels = sorted(self.pump_curves.keys())
        spd = self.speed

        lower = max([s for s in speed_levels if s <= spd])
        upper = min([s for s in speed_levels if s >= spd])

        if lower == upper:
            return float(self.interpolators[lower](flow_m3h))

        h_lower = float(self.interpolators[lower](flow_m3h))
        h_upper = float(self.interpolators[upper](flow_m3h))
        ratio = (spd - lower) / (upper - lower)
        return h_lower + ratio * (h_upper - h_lower)

    def get_pressure_output(self, flow_m3h):
        head_m = self.get_head(flow_m3h)
        rho = 983.2
        g = 9.81
        pressure = rho * g * head_m  # [Pa]
        print(f"[Pump] Speed: {self.speed}%, Flow: {flow_m3h:.3f} m³/h → Head: {head_m:.2f} m → Pressure: {pressure:.2f} Pa")
        return pressure
