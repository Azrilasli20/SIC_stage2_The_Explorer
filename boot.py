# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import time
import network
import machine as m
sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
sta_if.scan()
sta_if.connect("TP-Link_EB3A", "naqialfathur212121")
sta_if.isconnected()
time.sleep(3)
