from enum import Enum

CHANNELS_NUMBER = 8
FILE_LOCATION = '../../../data/app/'  # FIle directory
DEBUG_SUBDIR = 'debug/'
KEYS_SUFFIX = "_KEYS"

class Device(Enum):
    EEG = 1,
    EMG = 2

# GUI constants
WINDOW_X = 1600
WINDOW_Y = 800
BACKGROUND_COLOR = "#808080"
# Graph constants
X_LIM = 200
DPI = 100
REDRAW_INTERVAL = 10  # new frame every REDRAW_INTERVAL milliseconds
GRAPH_PROPORTION = 0.1  # set y axis as 2 * GRAPH_PROPORTION * current_value

# Experiment defaults
DEFAULT_AGE = 25
DEFAULT_ELECTRODES = "[O1, O2, FP1, FP2, C3, C4, P7, P8]"
DEFAULT_GENDER = "male"
DEFAULT_NAME_PREFIX = "EEG"
DEFAULT_RECORD_DURATION = 30.
DEFAULT_SUBJECT = "patient0"
MAX_RECORD_DURATION = 280.

# Experiments options
_FLASH = 'Flash'
_EO = 'EO'
_EC = 'EC'
_SSVEP1 = 'SSVEP1 6.2,7.7,10'
_SSVEP2 = 'SSVEP2 27, 33, 35, 37, 43'
_SSVEP3 = 'SSVEP3 8.5, 12, 15'
_PINCODE_4_TRUE_SEQ_REP_3 = "PIN4CORR3REP"
_P300_SECRET_9 = "P300SECRETSPELLER9"
_P300_SECRET_4 = "P300SECRETSPELLER4"
_MI_CALIBRATION = "MICALIBRATION"
_MI_INPUT = "MIRANDOM"

# Experiment constants
EP_EO_DURATION = 180.
EP_SSVEP_DURATION = 10.
EP_FLASH_RECORD_DURATION = 5.

FLASH_START = 2000
FLASH_END = 2100

PINCODE_FLASH_INTERVAL = 2000  # Tile flashes every PINCODE_FLASH_INTERVAL milliseconds
PINCODE_FLASH_DURATION = 550  # Tile flashes after PINCODE_FLASH_DURATION milliseconds
PINCODE_TRUE_SEQ = [2, 5, 6, 8]
PINCODE_REPETITIONS = 3
PINCODE_LENGTH = 4

# MOTOR IMAGERY
MI_CALIBRATION_TRIALS = 3
MI_INPUT_LENGTH = 12
MI_LABELS = 4


class TRIAL_STEPS:
    CROSS_START = 0
    CUE_START = 2000
    CUE_END = 3250
    CROSS_END = 6000
    TRIAL_END = 8000


class EMG_TRIAL_STEPS:
    CROSS_START = 0
    CUE_START = 1000
    CUE_END = 2000
    CROSS_END = 2000
    TRIAL_END = 2500


# SSVEP
SSVEP_TIME_WINDOW = 5000
FREQ = [
    [6.2, 7.7, 10],
    [27, 33, 35, 37, 43],
    [8.5, 12, 15]
]


