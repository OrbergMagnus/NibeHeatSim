
from components.node import Node
from components.pump import CirculationPump
from components.pipe import Pipe
from components.house import SimpleHouse
from components.heat_source import HeatSource
import matplotlib.pyplot as plt

# Skapa noder
node_source_out = Node("HeatSourceOut")
node_pump_in = Node("PumpIn")
node_pump_out = Node("PumpOut")
node_house_in = Node("HouseIn")       # <-- referensnod (0 Pa)
node_house_out = Node("HouseOut")

# Initflöde i m³/s
for node in [node_source_out, node_pump_in, node_pump_out, node_house_in, node_house_out]:
    node.flow = 0.0005

# Komponenter
heat_source = HeatSource(max_power_watt=9000)
pump = CirculationPump()
pump.set_speed(100)
house = SimpleHouse(dot_temp=-15, dot_power=5000)

# Rör
pipe1 = Pipe(inlet=node_source_out, outlet=node_pump_in, length_m=2, diameter_m=0.028)
pipe2 = Pipe(inlet=node_pump_out, outlet=node_house_in, length_m=10, diameter_m=0.028)
pipe3 = Pipe(inlet=node_house_out, outlet=node_source_out, length_m=10, diameter_m=0.028)

# Simulering
timesteps = 3600
dt = 1
times, temps, flows = [], [], []

for t in range(0, timesteps, dt):
    # === Tryckreferens ===
    node_house_in.pressure = 0  # Trycknollpunkt

    # === Iterativt: räkna baklänges tryck och flöde ===
    pipe2.update()  # ger pump_out.pressure
    pump_pressure = node_pump_out.pressure

    # pumpen genererar tryck utifrån flöde
    est_flow_m3h = node_pump_out.flow * 3600
    node_pump_out.pressure = pump.get_pressure_output(est_flow_m3h)

    # därefter räkna vidare tryck:
    pipe1.update()  # ger source_out.pressure
    pipe3.update()  # ger house_out.pressure

    # Värmekällan värmer vattnet
    flow_l_min = node_source_out.flow * 60 * 1000
    heat_source.update(inlet_temp=node_house_out.temperature, flow_l_min=flow_l_min, outlet_node=node_source_out)

    # Uppdatera husets temperatur
    house.set_radiator_temp(node_house_in.temperature)
    house.set_outdoor_temp(-5)
    house.update(dt)
    node_house_out.temperature = house.get_room_temperature()

    # Loggning
    times.append(t)
    temps.append(house.get_room_temperature())
    flows.append(node_pump_out.flow * 60 * 1000)

# Plotta
fig, ax1 = plt.subplots()
color = 'tab:blue'
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Room Temperature (°C)", color=color)
ax1.plot(times, temps, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel("Flow Rate (l/min)", color=color)
ax2.plot(times, flows, color=color)
ax2.tick_params(axis='y', labelcolor=color)

plt.title("NibeHeatLab – Pressure Reference Node (HouseIn = 0 Pa)")
plt.grid()
plt.tight_layout()
plt.show()
