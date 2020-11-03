from machine import I2C, Pin

import machine
import lvgl as lv
import lvgl_helper as lv_h
import lvesp32
import display
import time
import machine
import touchscreen as ts
import axp202
import random

from bbqkeyboard_micropython import BBQ10Keyboard, STATE_PRESS, STATE_RELEASE, STATE_LONG_PRESS


def screen_init():
    sda_pin = machine.Pin(23)
    scl_pin = machine.Pin(32)

    i2c = machine.I2C(id=1, scl=scl_pin, sda=sda_pin, speed=400000)
    ts.init(i2c)

    tft.init(tft.ST7789, width=240, invrot=3, rot=1, bgr=False, height=240, miso=2, mosi=19, clk=18, cs=5, dc=27,
             speed=40000000, color_bits=tft.COLOR_BITS16, backl_pin=12, backl_on=1)

    tft.clear(tft.RED)
    time.sleep(1)
    tft.clear(tft.GREEN)
    time.sleep(1)
    tft.clear(tft.BLUE)
    time.sleep(1)

    lv.init()
    disp_buf1 = lv.disp_buf_t()
    buf1_1 = bytes(240 * 10)
    lv.disp_buf_init(disp_buf1, buf1_1, None, len(buf1_1) // 4)
    disp_drv = lv.disp_drv_t()
    lv.disp_drv_init(disp_drv)
    disp_drv.buffer = disp_buf1
    disp_drv.flush_cb = lv_h.flush
    disp_drv.hor_res = 240
    disp_drv.ver_res = 240
    lv.disp_drv_register(disp_drv)

    indev_drv = lv.indev_drv_t()
    lv.indev_drv_init(indev_drv)
    indev_drv.type = lv.INDEV_TYPE.POINTER
    indev_drv.read_cb = lv_h.read
    lv.indev_drv_register(indev_drv)

    scr = lv.obj()
    btn = lv.btn(scr)
    btn.align(lv.scr_act(), lv.ALIGN.CENTER, 0, 0)
    label = lv.label(btn)
    label.set_text("Button")
    lv.scr_load(scr)


def keyboard_handler(keyboard_interrupt):
    key_count = kbd.key_count
    if key_count > 0:
        key = kbd.key
        state = 'pressed'
        if key[0] == STATE_LONG_PRESS:
            state = 'held down'
        elif key[0] == STATE_RELEASE:
            state = 'released'

        print("key: '%s' (dec %d, hex %02x) %s" % (key[1], ord(key[1]), ord(key[1]), state))


def t_watch_init():
    kbd.blacklight = 0.5
    pin_speaker = Pin(25, Pin.OUT)
    pin_motor = Pin(33, Pin.OUT)
    pin_speaker.value(1)
    pin_motor.value(1)
    time.sleep_ms(500)
    pin_speaker.value(0)
    pin_motor.value(0)
    # screen_init()
    print("finish init")


i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)

keyboard_interrupt = Pin(4, Pin.IN, trigger=Pin.IRQ_FALLING, handler=keyboard_handler)
# keyboard_interrupt.irq(trigger=Pin.IRQ_FALLING, handler=keyboard_handler)

kbd = BBQ10Keyboard(i2c)
# pmu = axp202.PMU(i2c)
# pmu.enablePower(axp202.AXP202_LDO2)
# pmu.setLDO2Voltage(3300)
# tft = display.TFT()

t_watch_init()