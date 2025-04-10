def init_simulation(house, heat_source, node_supply, flow_l_min, initial_temp=20.0):
    house.room_temp = initial_temp
    house.set_radiator_temp(initial_temp)
    heat_source.inlet_temp = initial_temp
    node_supply.temperature = initial_temp
    node_supply.flow = flow_l_min

from components import Node, HeatSource, CirculationPump, SimpleHouse
import matplotlib.pyplot as plt

# --- Skapa komponenter ---
pump = CirculationPump(max_flow_l_min=10, speed_percent=100)
heat_source = HeatSource(max_power_watt=9000)
heat_source.set_speed(100)
house = SimpleHouse(dot_temp=-15, dot_power=5000, initial_temp=20)

# --- Skapa noder ---
node_supply = Node("supply")
flow_l_min = pump.compute_flow()

# --- Simuleringsparametrar ---
timesteps = 3600  # sekunder (1 timme)
dt = 1  # sekunder
times = []
temps = []

# --- Simuleringsloop ---
for t in range(0, timesteps, dt):
    inlet_temp = house.get_room_temperature()
    heat_source.update(inlet_temp=inlet_temp, flow_l_min=flow_l_min, outlet_node=node_supply)
    house.set_radiator_temp(node_supply.temperature)
    house.set_outdoor_temp(-5)
    house.update(dt)

    times.append(t)
    temps.append(house.get_room_temperature())

# --- Plotta resultat ---
plt.plot(times, temps)
plt.xlabel("Tid (s)")
plt.ylabel("Rumstemperatur (°C)")
plt.title("Rummets temperatur över tid (värmekälla med maxeffekt)")
plt.grid(True)
plt.tight_layout()
plt.show()