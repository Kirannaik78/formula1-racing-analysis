from enum import Enum

class SessionName(Enum):
    PRACTICE_SESSION_ONE='Practice 1'
    PRACTICE_SESSION_TWO='Practice 2'
    PRACTICE_SESSION_THREE='Practice 3'
    DAY_ONE = 'Day 1'
    DAY_TWO = 'Day 2'
    DAY_THREE = 'Day 3'
    QUALIFYING='Qualifying'
    RACE='Race'

class SessionType(Enum):
    PRACTICE='Practice'
    QUALIFYING='Qualifying'
    RACE='Race'

class CircuteShortName(Enum):
    SAKHIR = "Sakhir"
    JEDDAH = "Jeddah"
    MELBOURNE = "Melbourne"
    BAKU = "Baku"
    MIAMI = "Miami"
    MONTE_CARLO = "Monte Carlo"
    CATALUNYA = "Catalunya"
    MONTREAL = "Montreal"
    SPIELBERG = "Spielberg"
    SILVERSTONE = "Silverstone"
    HUNGARORING = "Hungaroring"
    SPA_FRANCORCHAMPS = "Spa-Francorchamps"
    ZANDVOORT = "Zandvoort"
    MONZA = "Monza"
    SINGAPORE = "Singapore"
    SUZUKA = "Suzuka"
    LUSAIL = "Lusail"
    AUSTIN = "Austin"
    MEXICO_CITY = "Mexico City"
    INTERLAGOS = "Interlagos"
    LAS_VEGAS = "Las Vegas"
    YAS_MARINA_CIRCUIT = "Yas Marina Circuit"
    SHANGHAI = "Shanghai"
    IMOLA = "Imola"