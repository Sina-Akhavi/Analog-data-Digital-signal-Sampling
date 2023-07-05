import matplotlib.pyplot as plt
import numpy as np  
import project2_util
import sounddevice as sd
# import IPython.display as ipd

# project2_util.hello('HI')

def signal(amplitude, frequency, phase, t):
    return amplitude * np.cos(2 * np.pi * frequency * t + phase)


def configue_graph(ax, title, x_major_locator = np.pi / 2, y_major_locator = 0.25):
    ax.set_title(title)
    
    ax.axvline(0, color='black', lw=2)
    ax.axhline(0, color='black', lw=2)

    ax.xaxis.set_major_locator(plt.MultipleLocator(x_major_locator))
    ax.yaxis.set_major_locator(plt.MultipleLocator(y_major_locator))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(project2_util.format_func))

    ax.grid()

def draw_main_signal():
    
    fg_main_signal, ax_main_signal = plt.subplots()
    ax_main_signal.plot(t_vals, y_vals, 'blue')

    configue_graph(ax_main_signal, 'Main Signal')

    return [fg_main_signal, ax_main_signal]

def draw_sampling_and_mainsignal():
    fg_main_sampling, ax_main_sampling = draw_main_signal()
    ax_main_sampling.set_title('Sampling')

    global t_samples
    global y_samples

    # t_samples = [x for x in range(0, int(np.ceil(duration) + EPSILON), sample_rate)]
    t_samples = np.arange(0, duration + project2_util.EPSILON, sample_rate)
    y_samples = np.array([signal(amplitude, frequency, phase, t) for t in t_samples])

    ax_main_sampling.stem(t_samples, y_samples, 'red')

    return [fg_main_sampling, ax_main_sampling]

def draw_mainsignals_levels_samples():
    fg, ax = draw_sampling_and_mainsignal()
    draw_horizontal_levels(ax, fg)
    return [ax, fg]

def draw_horizontal_levels(axis = None, figure = None):

    ax = None
    fg = None
    if axis is None:
        fg, ax = plt.subplots()
    else:
        ax = axis
        fg = figure

    configue_graph(ax, 'Title')
    ax.grid()  

    global levels_xs
    global levels_ys

    levels_xs = np.linspace(0, duration)
    levels_ys = np.linspace(start=-1 * amplitude,stop=amplitude, num=number_of_levels , endpoint=True)
    
    for i in range(0, number_of_levels):
        y_vals = np.array([levels_ys[i] for x in levels_xs])
        ax.plot(levels_xs, y_vals)
        binary_stram = project2_util.produce_binary_stream(number_of_bits, i)
        ax.annotate(binary_stram, xy=(duration/2, y_vals[i]))
    
    return [fg, ax]


def draw_quantized_graph(quantized_samples):
    fg, ax = draw_horizontal_levels()
    ax.grid()

    ys_quantized_samples = [y[0] for y in quantized_samples]
    ax.set_title('Quantized Digital Signal')
    ax.stem(t_samples, ys_quantized_samples, 'purple')

def draw_the_difference():
    
    fg, ax = plt.subplots()
    differences_y = []

    for i in range(0, len(y_samples)):

        y_sample = y_samples[i]
        y_quantized = quantized_samples[i][0]

        differences_y.append(y_sample - y_quantized)
        # ax.stem(t_samples[i], difference)
    
    configue_graph(ax, 'Difference', y_major_locator=0.05)
    ax.stem(t_samples, differences_y)

if __name__ == '__main__':

    # amplitude, frequency, phase, duration, number_of_bits, number_of_levels, sample_rate = project2_util.initialize()
    amplitude = 2
    frequency = 1.3
    phase = 1
    duration = 10
    number_of_bits = 3
    number_of_levels = 8
    sample_rate = 1

    t_samples = None
    y_samples = None
    
    levels_ys = None

    t_vals = np.linspace(0, duration, 2000)
    y_vals = np.array([signal(amplitude, frequency, phase, t) for t in t_vals])

    draw_main_signal()
    draw_sampling_and_mainsignal()
    draw_mainsignals_levels_samples()

    quantized_samples = project2_util.quantize_samples(levels_ys, y_samples, t_samples)
    
    draw_the_difference()

    draw_quantized_graph(quantized_samples)

    bit_stream =  project2_util.generate_bit_stream(quantized_samples, number_of_bits)
    print('digital signal: ', bit_stream)
    print('SNR = 6.02n + 1.076 (db) = ', project2_util.cal_SNR(number_of_bits))

    sd.play(y_samples, samplerate=48000)

    plt.show()
