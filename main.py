import numpy as np
import matplotlib.pyplot as plt

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


# TODO: Not sure if this is the correct way to apply the coding rate
#       Doesn't work for other rates...
def apply_coding_rate(bit_stream, coding_rate):
    return np.repeat(bit_stream, int(1 / coding_rate))


def calculate_signal_value(t, bit):
    """Calculates value of carier signal at time `t` given `bit`."""
    return (
        0
        if bit == 0
        else AMPLITUDE * np.sin(2 * np.pi * CARRIER_FREQUENCY * t + PHASE_SHIFT)
    )


def rf_up_conversion(bit_stream, step=0.001):
    """Converts bit stream to RF signal."""
    rf_up_conversion = []
    stream_length = len(bit_stream)
    time_series = [
        round(i * step, 3) for i in range(stream_length * int(SYMBOL_DURATION / step))
    ]
    i = 0
    for b in range(stream_length):
        t = b * int(SYMBOL_DURATION / step)
        while t < len(time_series) and time_series[t] < (b + 1):
            i += 1
            rf_up_conversion.append(
                calculate_signal_value(time_series[t], bit_stream[b])
            )
            t += 1
    return rf_up_conversion, time_series


signal, time = rf_up_conversion(apply_coding_rate(BIT_STREAM, CODING_RATE))

plt.plot(time, signal)
plt.xlabel("Time (s)")
plt.ylabel("Signal")
plt.title("Signal vs. Time")
plt.show()
