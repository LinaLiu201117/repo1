# Add your Python code here. E.g.
from microbit import *
import music
import neopixel

# define
RGB_LED_NUM = 30
RGB_COLOR_NUM = 8
RGB_COLOR = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (255, 255, 255),
]

# RGB
rgbLedUpdateTime = 100
rgbLedTimeCnt = 0
rgbLedCurIndex = 0
rgbLedColorIndex = 1

# LIGHT
LIGHT_VALUE_MAX = 10
lightCurValue = 0
lightLastValue = 0
lightTimeCnt = 0
lightValuebuf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lightValueIndex = 0

# MUSIC
musicCurPlaySta = 0
musicExpectPlaySta = 0

# DISPLAY
curPicIndex = 0
expectPicIndex = 0

# CFG
lightThreshold = 50
np = neopixel.NeoPixel(pin2, RGB_LED_NUM)

# turn on led
def rgbLedCtrlOn(ledIndex, colorIndex):
    global nb
    for i in range(0, RGB_LED_NUM):
        if i == ledIndex:
            # on
            np[i] = RGB_COLOR[colorIndex]
        else:
            # off
            np[i] = RGB_COLOR[0]
    # show
    np.show()
    return

# rgb time modify
def rgbLedTimeSet(value):
    # var declare
    global rgbLedUpdateTime
    # cpy
    rgbLedUpdateTime = value
    return


# rgb led task
def rgbLedTask():
    # var declare
    global rgbLedTimeCnt
    global rgbLedCurIndex
    global rgbLedColorIndex

    # time cal
    rgbLedTimeCnt += 1
    if rgbLedTimeCnt < rgbLedUpdateTime:
        return
    # restart cal
    rgbLedTimeCnt = 0

    # rgb update
    rgbLedCtrlOn(rgbLedCurIndex, rgbLedColorIndex)

    # switch to next led
    rgbLedCurIndex += 1
    if RGB_LED_NUM <= rgbLedCurIndex:
        rgbLedCurIndex = 0
        # switch to next color
        rgbLedColorIndex += 1
        if RGB_COLOR_NUM <= rgbLedColorIndex:
            # start from one
            rgbLedColorIndex = 1
    return


# music task
def musicCtrl(value):
    # var declare
    global musicCurPlaySta
    global musicExpectPlaySta

    # light chk
    if value < lightThreshold:
        musicExpectPlaySta = 1
    else:
        musicExpectPlaySta = 0

    # chk change
    if musicExpectPlaySta != musicCurPlaySta:
        musicCurPlaySta = musicExpectPlaySta
        # music ctrl
        if musicCurPlaySta == 1:
            # play
            print("music start..")
            music.play(music.RINGTONE)
        else:
            # stop
            print("music stop..")
            music.stop()
    return

# display ctrl
def displayCtr(value):
    # var declare
    global curPicIndex
    global expectPicIndex

    # chk light value
    if value < lightThreshold:
        expectPicIndex = 1
    else:
        expectPicIndex = 0

    # change
    if expectPicIndex != curPicIndex:
        # cpy
        curPicIndex = expectPicIndex
        # show
        if curPicIndex == 0:
            display.show(Image.HAPPY)
        else:
            display.show(Image.SAD)

    return

# light task
def lightTask():
    # var declare
    global lightTimeCnt
    global lightCurValue
    global lightLastValue
    global lightValuebuf
    global lightValueIndex

    # time 1s
    lightTimeCnt += 1
    if lightTimeCnt < 100:
        return

    lightValuebuf[lightValueIndex] = pin1.read_analog()
    lightValuebuf.sort()
    lightValueSum = 0
    for i in range(1, LIGHT_VALUE_MAX-2):
        lightValueSum = lightValueSum + lightValuebuf[i]
    lightCurValue = lightValueSum/(LIGHT_VALUE_MAX-2)

    lightValueIndex += 1
    if lightValueIndex >= LIGHT_VALUE_MAX:
        lightValueIndex = 0

    if lightCurValue != lightLastValue:
        if abs(lightCurValue - lightLastValue) < 20:
            return
        # light value update
        lightLastValue = lightCurValue
        # print for debug
        # print("\r\n", lightLastValue)
        # change rgb time
        rgbLedTimeSet(lightLastValue / 100)
        # change music
        musicCtrl(lightLastValue)
        # change display
        displayCtr(lightLastValue)
    return


while True:
    # var
    # power voice
    music.play(music.JUMP_UP)

    # display init
    display.show(Image.HAPPY)

    while True:
        # rgb led task
        rgbLedTask()

        # light task
        lightTask()

        # sleep
        sleep(10)
