import wave
import struct

# Define the audio format

bitstream = '110000011111010001111100000101110000011001110110111111001010101'

nchannels = 1  # Mono
sample_width = 2  # 16-bit audio
sample_rate = 44100  # Sampling frequency
nframes = len(bitstream) // sample_width  # Calculate the number of frames

# Create a new WAV file
with wave.open('output.wav', mode='wb') as wav_file:
    # Set the WAV file parameters
    wav_file.setparams((nchannels, sample_width, sample_rate, nframes, 'NONE', 'not compressed'))
    
    # Convert the bit stream into audio data
    audio_data = []
    for i in range(0, len(bitstream), sample_width):
        # Extract the 16-bit integer from the bit stream
        bits = bitstream[i:i+sample_width]
        int_val = int(''.join(map(str, bits)), 2)

        # Convert the integer to a binary string and pack it as a signed short
        sample = struct.pack('<h', int_val)
        audio_data.append(sample)

    # Write the audio data to the WAV file
    wav_file.writeframes(b''.join(audio_data))