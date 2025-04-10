
class HeatSource:
    def __init__(self, max_power_watt, inlet_temp=20):
        self.max_power = max_power_watt
        self.speed = 100
        self.inlet_temp = inlet_temp
        self.cp = 4186
        self.rho = 1000

    def set_speed(self, percent):
        self.speed = max(0, min(100, percent))

    def update(self, inlet_temp, flow_l_min, outlet_node):
        self.inlet_temp = inlet_temp
        flow_m3_s = flow_l_min / 1000 / 60
        mass_flow = flow_m3_s * self.rho
        P = self.max_power * (self.speed / 100)
        delta_T = P / (mass_flow * self.cp) if mass_flow > 0 else 0
        outlet_node.temperature = self.inlet_temp + delta_T
