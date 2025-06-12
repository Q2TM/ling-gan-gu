from flask import request, Response

from app import app
from lakeshore import Model240
from lakeshore.model_240 import Model240InputParameter, Model240Enums

ls = Model240()
CHANNEL = 1

rtd_config = Model240InputParameter(sensor=Model240Enums.SensorTypes.NTC_RTD,
                                    current_reversal_enable=True,
                                    auto_range_enable=False,
                                    units=Model240Enums.Units.SENSOR,
                                    input_enable=True,
                                    input_range=Model240Enums.InputRange.RANGE_NTCRTD_100_KIL_OHMS)

ls.set_input_parameter(CHANNEL, rtd_config)


def get_amps(irange: int):
    if irange == Model240Enums.InputRange.RANGE_NTCRTD_10_OHMS:
        return 10 ** -3
    elif irange == Model240Enums.InputRange.RANGE_NTCRTD_30_OHMS:
        return 300 * 10 ** -6
    elif irange == Model240Enums.InputRange.RANGE_NTCRTD_100_OHMS:
        return 100 * 10 ** -6
    # elif irange == Model240Enums.InputRange.RANGE_NTCRTD_300_OHMS:
    #     return 30 * 10 ** -6
    elif irange == Model240Enums.InputRange.RANGE_NTCRTD_1_KIL_OHMS:
        return 10 * 10 ** -6
    elif irange == Model240Enums.InputRange.RANGE_NTCRTD_3_KIL_OHMS:
        return 3 * 10 ** -6
    elif irange == Model240Enums.InputRange.RANGE_NTCRTD_10_KIL_OHMS:
        return 1 * 10 ** -6
    elif irange == Model240Enums.InputRange.RANGE_NTCRTD_30_KIL_OHMS:
        return 300 * 10 ** -9
    elif irange == Model240Enums.InputRange.RANGE_NTCRTD_100_KIL_OHMS:
        return 100 * 10 ** -9

    return 0


@app.route("/", methods=["GET"])
def get_index():
    return "Hello World!", 200


@app.route("/data", methods=["GET"])
def get_data():
    name = ls.get_sensor_name(CHANNEL)
    value = ls.get_sensor_reading(CHANNEL)

    input_param = ls.get_input_parameter(CHANNEL)

    amps = get_amps(input_param.input_range)
    # if input_param.units == Model240Enums.Units.SENSOR:
    #     value = value * amps
    # elif input_param.units == Model240Enums.Units.CELSIUS:
    #     value = ls.convert_kelvin_to_celsius(value)
    # elif input_param.units == Model240Enums.Units.FAHRENHEIT:
    #     value = ls.convert_kelvin_to_fahrenheit(value)

    voltage = value * amps
    power = voltage * amps

    return {
        "channel": CHANNEL,
        "name": name,
        "value": value,
        "input_param": input_param.__dict__,
        "kelvin": ls.get_kelvin_reading(CHANNEL),
        "identification": ls.get_identification(),
        "voltage": voltage,
        "amps": amps,
        "power": power,
    }, 200


@app.route("/health", methods=["GET"])
def get_health():
    return "OK", 200
