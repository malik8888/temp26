#!/usr/bin/python
import smbus
import time
import math

bus = smbus.SMBus(1)
address = 0x68
powermgmt_1=0x6b
powermgmt_2=0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def write_byte(adr, value):
    bus.write_byte_data(address, adr, value)
while True:
     bus.write_byte_data(address,powermgmt_1,0)
     temp=read_word_2c(0x41)
     t=(temp/340)+36.53
     print("temp:",t)
     time.sleep(2)
