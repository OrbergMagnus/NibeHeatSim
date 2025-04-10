
import math

class Pipe:
    def __init__(self, inlet, outlet, length_m, diameter_m=0.028, roughness=0.0001):
        self.inlet = inlet
        self.outlet = outlet
        self.length = length_m
        self.diameter = diameter_m
        self.roughness = roughness
        self.rho = 1000  # kg/m3
        self.mu = 0.001  # Pa·s

    def update(self):
        dp = self.inlet.pressure - self.outlet.pressure
        radius = self.diameter / 2

        if dp <= 0:
            flow = 0
        else:
            flow = (math.pi * radius**4 * dp) / (8 * self.mu * self.length)

        self.inlet.flow = flow
        self.outlet.flow = flow
        self.outlet.temperature = self.inlet.temperature

        print(f"[Pipe] Inlet: {self.inlet.pressure:.2f} Pa, Outlet: {self.outlet.pressure:.2f} Pa "
              f"→ ΔP = {dp:.2f} Pa → Flow = {flow:.6f} m³/s")
