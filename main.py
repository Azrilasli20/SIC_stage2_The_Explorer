from umqtt.robust import MQTTClient
from machine import Pin, SoftI2C
from machine import ADC
import machine as m
import ssd1306
import dht

ubidotsToken = "BBUS-pCxGOtGH2ItfCdtidQtG79BsVq3JcM"
clientID = "man3medan"
client = MQTTClient("clientID", "industrial.api.ubidots.com", 1883, user = ubidotsToken, password = ubidotsToken)
print("Loading...")

def checkwifi():
    while not sta_if.isconnected():
        time.sleep_ms(500)
        print(".")
        sta_if.connect()

# Inisialisasi OLED
i2c = SoftI2C(scl=Pin(15), sda=Pin(4))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Inisialisasi LED pada GPIO 2
led = Pin(18, Pin.OUT)

# Inisialisasi DHT11 pada GPIO 16
dht11 = dht.DHT11(Pin(16))

# Inisialisasi LDR
adc = ADC(Pin(33, mode=Pin.IN))
adc.atten(ADC.ATTN_11DB)

def publish():
    while True:
        checkwifi()
        client.connect()
        lat = 3.63755
        lng = 98.665721
        ldr_value = adc.read()
        
        try:
            # Mengambil data dari sensor DHT11
            dht11.measure()
            suhu = dht11.temperature()  # Suhu dalam Celsius
            kelembaban = dht11.humidity()  # Kelembaban dalam %

            # Menampilkan data ke OLED
            oled.fill(0)  # Bersihkan layar
            oled.text("DHT11 Sensor", 20, 5)
            oled.text("Temp: {} C".format(suhu), 10, 25)
            oled.text("Humidity: {}%".format(kelembaban), 10, 40)

            # Cek kelembaban dan kontrol LED
            if kelembaban > 65:
                led.on()  # LED menyala jika kelembaban > 65%
            else:
                led.off()  # LED mati jika kelembaban <= 65%

            oled.show()

        except OSError as e:
            oled.fill(0)
            oled.text("Error reading DHT11", 10, 20)
            oled.show()
            print(f"Error Reading sensor")
            time.sleep(1)
            
        var = 4
        msg = b'{"location": {"value":%s, "context":{"lat":%s, "lng":%s}}}' % (var, lat, lng)
        print(msg)
        client.publish(b"/v1.6/devices/esp32", msg)
        
        msg = b'{"suhu": {"value":%s}}' % (suhu)
        print(msg)
        client.publish(b"/v1.6/devices/esp32", msg)
        
        msg = b'{"kelembaban": {"value":%s}}' % (kelembaban)
        print(msg)
        client.publish(b"/v1.6/devices/esp32", msg)
        
        msg = b'{"ldr": {"value":%s}}' % (ldr_value)
        print(msg)
        client.publish(b"/v1.6/devices/esp32", msg)
        
        time.sleep(2)
publish()
