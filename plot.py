import time
import statistics
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from lakeshore import Model240
from lakeshore.model_240 import Model240InputParameter, Model240Enums

ls = Model240()
channel = 1

rtd_config = Model240InputParameter(sensor = Model240Enums.SensorTypes.NTC_RTD,
                                    current_reversal_enable = True,
                                    auto_range_enable = False,
                                    units = Model240Enums.Units.SENSOR,
                                    input_enable = True,
                                    input_range = Model240Enums.InputRange.RANGE_NTCRTD_100_KIL_OHMS)

ls.set_input_parameter(1, rtd_config)

measurements = []

fig, ax = plt.subplots()

# Function to update the histogram
def update(frame):
    value = ls.get_sensor_reading(channel)
    measurements.append(value)
    ax.clear()
    ax.hist(measurements, bins=10, color='blue', alpha=0.7)
    ax.set_title('Distribution of Measurements')
    ax.set_xlabel('Measurement (ohm)')
    ax.set_ylabel('Count')
    if len(measurements) >= 10:
        avg = statistics.mean(measurements)
        std = statistics.stdev(measurements)
        ax.text(0.95, 0.95, f'Avg: {avg:.2f}\nStd: {std:.2f}\nCount: {len(measurements)}',
                transform=ax.transAxes, ha='right', va='top', fontsize=10,
                bbox=dict(facecolor='white', alpha=0.5))
    plt.tight_layout()
    time.sleep(0.1)

ani = animation.FuncAnimation(fig, update, interval=100)
plt.show()
