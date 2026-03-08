import smbus2d
import bme280
import time

# Default I2C address for BME280 (use 0x77 if SDO pin is HIGH)
PORT = 1          # I2C port (use 0 for older Pi models)
ADDRESS = 0x76    # BME280 I2C address

def read_bme280():
    bus = smbus2.SMBus(PORT)
    calibration_params = bme280.load_calibration_params(bus, ADDRESS)

    data = bme280.sample(bus, ADDRESS, calibration_params)

    temperature = data.temperature       # °C
    pressure = data.pressure             # hPa
    humidity = data.humidity             # %RH

    return temperature, pressure, humidity

def main():
    print("BME280 Sensor Readings")
    print("=" * 35)

    while True:
        try:
            temp, pressure, humidity = read_bme280()

            print(f"Temperature : {temp:.2f} °C  ({(temp * 9/5) + 32:.2f} °F)")
            print(f"Pressure    : {pressure:.2f} hPa")
            print(f"Humidity    : {humidity:.2f} %RH")
            print("-" * 35)

            time.sleep(2)

        except KeyboardInterrupt:
            print("\nStopped by user.")
            break
        except Exception as e:
            print(f"Error reading sensor: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()