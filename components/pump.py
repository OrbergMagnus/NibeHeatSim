class CirculationPump:
    def __init__(self, max_flow_l_min, speed_percent):
        self.max_flow = max_flow_l_min
        self.speed = speed_percent

    def compute_flow(self):
        return self.max_flow * (self.speed / 100)  # l/min