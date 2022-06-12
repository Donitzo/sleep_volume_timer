__version__ = '0.1.0'
__author__  = 'Donitz'
__license__ = 'MIT'
__repository__ = 'https://github.com/Donitzo/sleep_volume_timer'

import sys
import time
import os

from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pynput.mouse import Listener

class UnsupportedVersion(Exception):
    pass

MIN_VERSION, VERSION_LESS_THAN = (3, 5), (4, 0)
if sys.version_info < MIN_VERSION or sys.version_info >= VERSION_LESS_THAN:
    raise UnsupportedVersion('requires Python %s,<%s' % ('.'.join(map(str, MIN_VERSION)), '.'.join(map(str, VERSION_LESS_THAN))))

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

EARLY_MAX_VOLUME = 0.07 # volume.GetMasterVolumeLevelScalar()
LATE_MAX_VOLUME = 0.05

EARLY_MIN_VOLUME = 0
LATE_MIN_VOLUME = 0

EARLY_TO_LATE_SECONDS = 60 * 60
EARLY_MAX_TO_MIN_SECONDS = 60 * 60
LATE_MAX_TO_MIN_SECONDS = 60 * 30

RESET_WITH_MOUSE = True

start_seconds = time.time()
reset_seconds = start_seconds

os.system('mode con: cols=43 lines=3')

def reset(x, y, button, pressed):
    global reset_seconds

    reset_seconds = time.time()

if RESET_WITH_MOUSE:
    listener = Listener(on_click=reset)
    listener.start()

while True:
    seconds_since_start = max(1, time.time() - start_seconds)
    seconds_since_reset = max(1, time.time() - reset_seconds)

    late_t = max(0.0, min(1.0, float(seconds_since_start) / EARLY_TO_LATE_SECONDS))
    max_to_min_seconds = EARLY_MAX_TO_MIN_SECONDS * (1.0 - late_t) + LATE_MAX_TO_MIN_SECONDS * late_t
    max_volume = EARLY_MAX_VOLUME * (1.0 - late_t) + LATE_MAX_VOLUME * late_t
    min_volume = EARLY_MIN_VOLUME * (1.0 - late_t) + LATE_MIN_VOLUME * late_t
    min_t = max(0.0, min(1.0, float(seconds_since_reset) / max_to_min_seconds))
    current_volume = max(0.0, min(EARLY_MAX_VOLUME, max_volume * (1.0 - min_t) + min_volume * min_t))

    volume.SetMasterVolumeLevelScalar(current_volume, None)

    os.system('cls')

    print('            SLEEP VOLUME TIMER')
    print('EARLY [%s] LATE' % ('#' * int(1 + late_t * 28.99) + ' ' * (28 - int(late_t * 28.99))))
    print('LOUD  [%s] QUIET' % ('#' * int(1 + min_t * 28.99) + ' ' * (28 - int(min_t * 28.99))), end='', flush=True)

    time.sleep(1)
