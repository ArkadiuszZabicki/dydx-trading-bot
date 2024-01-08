from constants import RESOLUTION
import numpy as np
from func_utils import get_ISO_times
import pandas as pd
import time
from pprint import pprint

# Get relevant time periods for ISO from and to
ISO_TIMES = get_ISO_times()

pprint(ISO_TIMES)

# Construct market prices
def construct_market_prices(client):
    pass