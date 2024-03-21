#from sdcard_init_class import *
#from bmp280_init_class import *
from machine import ADC, Pin, I2C
#from time import sleep
import utime
from lsm6ds33 import LSM6DS33
import bmp280
from bmp280_configuration import BMP280Configuration
from bmp280_i2c import BMP280I2C


#instantiate objects corresponds to sensors
# pressure sensor object named bmp_sensor
#BMP_sensor = bmp_func('bmp_sensor')
# sd card object writes to and reads from bmp_sensor_vals.txt
#microsd = sdcard_init('microSD',5,7,4,6,0)
#BMP_sd2 = sdcard_init('bmp_sensor_vals',13,11,12,10,1)
#bmp_sdio = sdFileAccess('bmp280_data')
#pico_sdio = sdFileAccess('pico_temperature_data')

#------------------
#writes BMP280 sensor measurement values to file on sdcard
#bmp_sdio.write(BMP_sensor.read())



#adcpin = 26 # analog to digital convert pin number
#temp36 = ADC(4) 
#adc_value = temp36.read_u16()
#volt = (3.3/65535)*adc_value
#DegC = (100*volt) - 50


#pico_sdio.write(round(DegC,2))


#i2c1_sda = Pin(18)
#i2c1_scl = Pin(19)
#i2c1 = I2C(1, sda=i2c1_sda, scl=i2c1_scl, freq=400000)
    
#gyr = LSM6DS33(i2c1)
#gyr.a()
#gyr.g()

class BMP280Sensor:
    def __init__(self, i2c):
        self.bmp280 = BMP280I2C(0x77, i2c) #might need to adjust address

    def read_temperature(self):
        return self.bmp280.temperature

    def read_pressure(self):
        return self.bmp280.pressure

class TMP36Sensor:
    def __init__(self, pin):
        self.adc = ADC(pin)

    def read_temperature(self):
        adc_value = self.adc.read_u16()
        volt = (3.3 / 65535) * adc_value
        degC = (100 * volt) - 50
        return round(degC, 2)
    
class Gyro:
    def __init__(self, i2c):
        self.lsm6ds33 = LSM6DS33(i2c)

    def read_acceleration(self):
        return self.lsm6ds33.read_acceleration()

    def read_angular_rate(self):
        return self.lsm6ds33.read_angular_rate()

def read_data(bmp280_sensor, tmp36_sensor): #read data from sensors
    temperature_bmp280 = bmp280_sensor.read_temperature()
    pressure = bmp280_sensor.read_pressure()
    temperature_tmp36 = tmp36_sensor.read_temperature()
    acceleration = gyro.read_acceleration()
    angular_rate = gyro.read_angular_rate()
    return temperature_bmp280, pressure, temperature_tmp36, acceleration, angular_rate

class SDCard:
    def __init__(self, card_name, cs_pin, sck_pin, mosi_pin, miso_pin, spi_bus):

    def initialize(self):
        try:
            uos.mountsd(self.spi_bus, self.card_name)
            print(f"{self.card_name} initialized successfully.")
        except Exception as e:
            print(f"Error initializing {self.card_name}: {e}")

    def write_data(self, filename, data):
        try:
            with open(f"/{self.card_name}/{filename}", 'a') as file:
                file.write(data)
            print(f"Data written to {filename} on {self.card_name}.")
        except Exception as e:
            print(f"Error writing data to {filename} on {self.card_name}: {e}")

        #microsd = SDCard('microSD', 5, 7, 4, 6, 0)
        #microsd.initialize()

        #BMP_sd2 = SDCard('bmp_sensor_vals', 13, 11, 12, 10, 1)
        #BMP_sd2.initialize()

        #data_to_write = "SD card working!\n"
        #microsd.write_data('data.txt', data_to_write)
        #BMP_sd2.write_data('data.txt', data_to_write)

class Data:
    def __init__(self, filename):
        self.filename1 = filename1
        self.filename2 = filename2

    def save_data(self, temperature_bmp280, pressure, temperature_tmp36, acceleration, angular_rate):
        with open(self.filename1, 'a') as file1:
            file1.write(f'Time: {utime.time()}, Temperature BMP280: {temperature_bmp280}, Pressure: {pressure}, Temperature TMP36: {temperature_tmp36}, Acceleration: {acceleration}, Angular Rate: {angular_rate}\n')
        with open(self.filename2, 'a') as file2:
            file2.write(f'Time: {utime.time()}, Temperature BMP280: {temperature_bmp280}, Pressure: {pressure}, Temperature TMP36: {temperature_tmp36}, Acceleration: {acceleration}, Angular Rate: {angular_rate}\n')
    #data_log1 = Data('sensor_data.txt') 
    #data_log1.save_data(temperature_bmp280, pressure, temperature_tmp36, acceleration, angular_rate)

def RFtransmit(): #transmit data through RF
    pass

def check_temp():
    high_temp = False
    low_temp = False

    for sensor in temperature_sensors:
        temperature = sensor.read_temperature()
        if temperature > threshold_temperature_high:
            high_temp = True
            break
        elif temperature < threshold_temperature_low:
            low_temp = True
            break

    return high_temp, low_temp

class Peltier: 
    def __init__(self, relay_pin):
        self.relay_pin = Pin(relay_pin, Pin.OUT)

    def activate_cooler(self):
        self.relay_pin.value(1) 

    def deactivate_cooler(self):
        self.relay_pin.value(0)
    #cooler1 = PeltierCooler(relay_pin=...)
    #cooler1.activate_cooler()
    #cooler1.deactivate_cooler()

def PID(temperature_bmp280): #perform PID control depending on temperature
    pass

def main(): #create sensor objects from sensor class
    try:
        i2c0_sda = Pin(2)
        i2c0_scl = Pin(3)
        i2c0 = I2C(1, sda=i2c0_sda, scl=i2c0_scl, freq=400000)
    except Exception as e:
        print("Error found initializing I2C bus:", e)
        raise SystemExit
    
    try:
        bmp280_sensor = BMP280Sensor(i2c0)
        tmp36_sensor = TMP36Sensor(28) #might need to adjust pin number
        gyro = Gyro(i2c0)
    except Exception as e:
        print("Error initializing sensors:", e)
        raise SystemExit

    safety = True
    temp_high = False
    
    #define temperature thresholds
    threshold_temperature_high = 38
    threshold_temperature_low = 20

    #read and write data, safety protocols
    while safety:
        temperature_bmp280, pressure, temperature_tmp36, acceleration, angular_rate = read_data(bmp280_sensor, tmp36_sensor, gyro)
        save_data(temperature_bmp280, pressure, temperature_tmp36, acceleration, angular_rate)
        RFtransmit()
        temp_high, _ = check_temp([bmp280_sensor, tmp36_sensor], threshold_temperature_high, threshold_temperature_low)
        
        if temp_high:
            PID([temperature_bmp280])
            if temp_high:
                RFtransmit()  #stop transmission
                utime.sleep(1)  #delay to make sure transmission is complete
                safety = False
                break

        #check temperature to see whether to activate the cooler or not
        high_temp, low_temp = check_temp([bmp280_sensor, tmp36_sensor], threshold_temperature_high, threshold_temperature_low)
        
        if high_temp or low_temp:
            activate_cooler()
        else:
            deactivate_cooler()

    #error handling:


if __name__ == "__main__":
    main()