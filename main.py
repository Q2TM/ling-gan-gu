import time
import statistics
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

while True:
    time.sleep(1)
    value = ls.get_sensor_reading(channel)
    measurements.append(value)
    if len(measurements) > 10:
        measurements.pop(0)
    print(value, "ohm")
    if len(measurements) == 10:
        avg = statistics.mean(measurements)
        std = statistics.stdev(measurements)
        print(f"Average (last 10): {avg:.4f} ohm, Std Dev: {std:.4f} ohm")