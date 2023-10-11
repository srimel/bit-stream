# Stuart Rimel
# Wireless Networks & Apps
# Fall 2023

import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction

########################################################################################
# Assume a source (transmitter) sends a bit-stream 1 0 1.
# Assume a repetition code with 1/2 coding rate.
# Assume a carrier frequency of 2Hz and QPSK mnodulation with an amplitude of 2.
# Assume a 1 second symbol duration.
# Plot in time domain the transmitted signal corresponding to the bit-stream.
########################################################################################

BIT_STREAM = [1, 0, 1]
CODING_RATE = 1 / 2
CARRIER_FREQUENCY = 2
AMPLITUDE = 2
SYMBOL_DURATION = 1
PHASE_SHIFT = 0


def apply_coding_rate(bit_stream, coding_rate):
    """Applies coding rate to bit stream."""
    coded_bit_stream = []
    frac = Fraction(coding_rate).limit_denominator()
    n = frac.numerator
    m = frac.denominator
    i = 1
    for bit in bit_stream:
        if i % n == 0:  # repeat symbol
            for j in range(m):
                coded_bit_stream.append(bit)
        else:
            coded_bit_stream.append(bit)
        i += 1
    return coded_bit_stream


def calculate_signal_value(t, bits):
    """Calculates value of carier signal at time `t` given `bits`.
    Applies QPSK modulation to `bits`."""
    if bits == [1, 1]:
        return AMPLITUDE * np.cos(2 * np.pi * CARRIER_FREQUENCY * t + (np.pi / 4))
    elif bits == [0, 1]:
        return AMPLITUDE * np.cos(2 * np.pi * CARRIER_FREQUENCY * t + (3 * np.pi / 4))
    elif bits == [0, 0]:
        return AMPLITUDE * np.cos(2 * np.pi * CARRIER_FREQUENCY * t - (3 * np.pi / 4))
    else:
        return AMPLITUDE * np.cos(2 * np.pi * CARRIER_FREQUENCY * t - (np.pi / 4))


def rf_up_conversion(bit_stream, step=0.001):
    """Converts bit stream to RF signal."""
    rf_up_conversion = []
    stream_length = len(bit_stream)
    symbol_count = stream_length // 2  # two bits for one symbol (QPSK modulation)
    time_series = [
        round(i * step, 3) for i in range(symbol_count * int(SYMBOL_DURATION / step))
    ]
    bs = 0
    for b in range(0, stream_length, 2):
        t = bs * int(SYMBOL_DURATION / step)
        bits = bit_stream[b : b + 2]
        while t < len(time_series) and time_series[t] < (bs + 1):
            rf_up_conversion.append(calculate_signal_value(time_series[t], bits))
            t += 1
        bs += 1
    return rf_up_conversion, time_series


signal, time = rf_up_conversion(apply_coding_rate(BIT_STREAM, CODING_RATE))

plt.plot(time, signal)
plt.xlabel("Time (s)")
plt.ylabel("Signal")
plt.title("Signal vs. Time")
plt.show()
