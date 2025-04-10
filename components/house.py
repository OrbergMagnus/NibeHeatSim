class SimpleHouse:
    def __init__(self, dot_temp, dot_power, initial_temp=20, indoor_design_temp=21,
                 room_mass=1000, room_cp=1000, radiator_k=200):
        self.dot_temp = dot_temp
        self.dot_power = dot_power
        self.room_temp = initial_temp
        self.indoor_design_temp = indoor_design_temp

        self.radiator_temp = initial_temp
        self.radiator_k = radiator_k
        self.outdoor_temp = 0

        self.room_thermal_mass = room_mass * room_cp
        self.R_house = (indoor_design_temp - dot_temp) * 1000 / dot_power

        self.external_heat_sources = []

    def set_outdoor_temp(self, temp):
        self.outdoor_temp = temp

    def set_radiator_temp(self, temp):
        self.radiator_temp = temp

    def add_passive_heat(self, Q_watt):
        self.external_heat_sources.append(Q_watt)

    def update(self, dt):
        Q_rad = self.radiator_k * (self.radiator_temp - self.room_temp)
        Q_loss = (self.room_temp - self.outdoor_temp) / self.R_house
        Q_external = sum(self.external_heat_sources)
        self.external_heat_sources = []

        net_Q = Q_rad - Q_loss + Q_external
        delta_T = (net_Q * dt) / self.room_thermal_mass
        self.room_temp += delta_T

    def get_room_temperature(self):
        return self.room_temp