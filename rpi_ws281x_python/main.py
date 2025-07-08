import RPi.GPIO as GPIO
import websocket
import json
from rpi_ws281x import PixelStrip, Color
import time

# IP and port of Godot side server
SERVER_URI = "ws://<IP Address>:9080"

# LED setting
LED_COUNT = 144       # Number of LEDs
LED_PIN = 18          # GPIO pins (18 supports PWM)
LED_FREQ_HZ = 800000  # LED Signal Frequency
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return r, g, b

def laser(strip, color, wait_ms=10):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 3000.0)
        strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()

def colorWipe(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def colorOff():
    colorWipe(strip, Color(0, 0, 0))

def on_message(ws, message):
    if isinstance(message, bytes):
        message = message.decode('utf-8')

    try:
        data = json.loads(message)
        if data.get("type") == "color":
            hex_color = data.get("value", "#000000")
            r, g, b = hex_to_rgb(hex_color)
            print("color received: R={} G={} B={}".format(r, g, b))
            colorWipe(strip, Color(r, g, b))
    except Exception as e:
        print("error:", e)

def on_open(ws):
    print("WebSocket server connection succeeded")

def on_error(ws, error):
    print("error:", error)
    colorOff()

def on_close(ws, code, reason):
    print("end of connection")
    colorOff()

laser(strip, Color(255, 255, 255))
ws = websocket.WebSocketApp(SERVER_URI,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.run_forever()
