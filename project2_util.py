import numpy as np

EPSILON = 0.0001

def initialize():

    amplitude = int(input('Enter amplitude: '))
    frequency = float(input('Enter frequency: '))
    phase_in_degree = float(input('Enter phase (in degree): '))
    duration = float(input('Enter duration: '))
    number_of_bits = int(input('Enter number of bits: '))
    sample_rate = float(input('Enter sample rate: '))
    
    number_of_levels = 2 ** number_of_bits
    phase_in_rad = np.deg2rad(phase_in_degree)

    return [amplitude, frequency, phase_in_rad, duration, number_of_bits, number_of_levels, sample_rate]


def produce_binary_stream(number_of_bits, decimal_number):
    output = ''

    binary_str = bin(decimal_number)[2:]
    num_of_zeros_must_be_added = number_of_bits - len(binary_str)
    for i in range(0, num_of_zeros_must_be_added):
        output += '0'
    output += binary_str

    return output

def quantize_samples(levels_ys, y_samples, t_samples):
    output = []

    from_index = 0
    to_index = len(levels_ys) - 1

    index_sample = -1
    for y_sample in y_samples:
        index_sample += 1
        map_ysamples_to_ylevels_util(y_sample, t_samples, index_sample, levels_ys, output, from_index, to_index)

    return output

def map_ysamples_to_ylevels_util(y_sample, t_samples, index_sample, y_levels, output, from_index, to_index):
    
    if to_index - from_index == 1:

        dist_above = y_levels[to_index] - y_sample
        dist_below = y_sample - y_levels[from_index]

        newY_and_index = None
        if dist_below < dist_above:
            newY_and_index = (y_levels[from_index], t_samples[index_sample], from_index)
        else:
            newY_and_index = (y_levels[to_index], t_samples[index_sample], to_index)
        
        output.append(newY_and_index)

        return


    middle = (to_index + from_index) // 2

    if y_sample < y_levels[middle]:
        to_index = middle
        map_ysamples_to_ylevels_util(y_sample, t_samples, index_sample, y_levels, output, from_index, to_index)

    elif y_levels[middle] < y_sample:
        from_index = middle
        map_ysamples_to_ylevels_util(y_sample, t_samples, index_sample, y_levels, output, from_index, to_index)

    else:
        newY_and_index = (y_levels[middle], t_samples[index_sample], middle)
        output.append(newY_and_index)

        return
def generate_bit_stream(quantized_samples, number_of_bits):
    bit_stream = ''
    for y_x_index in quantized_samples:
        decimal_num = y_x_index[2]
        bit_stream += produce_binary_stream(number_of_bits, decimal_num) + ' '
    
    return bit_stream

def cal_SNR(number_of_bits):
    return 6.02 * number_of_bits + 1.76  


def format_func(value, tick_number):
    # find number of multiples of pi/2
    N = int(np.round(2 * value / np.pi))

    if N == 0:
        return "0"
    elif N == 1:
        return r"$\pi/2$"
    elif N == 2:
        return r"$\pi$"
    elif N % 2 > 0:
        return r"${0}\pi/2$".format(N)
    else:
        return r"${0}\pi$".format(N // 2)
