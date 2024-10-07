#!/usr/bin/python

# adapted from https://github.com/peteshadbolt/spectrogram
import numpy as np
import matplotlib.image as mpimg
import wave
from array import array
from scipy.io import wavfile


def make_wav(image_filename):
    """ Make a WAV file having a spectrogram resembling an image """
    # Load image
    image = mpimg.imread(image_filename)
    image = np.sum(image, axis = 2).T[:, ::-1]
    image = image**3 # ???
    w, h = image.shape

    # Load sound
    samplerate, sound = wavfile.read('sound.wav')

    # Fourier transform, normalize, remove DC bias
    data = np.fft.irfft(image, h*2, axis=1).reshape((w*h*2))
    data -= np.average(data)
    data *= (2**15-1.)/np.amax(data)
    data *= .15
    data = data[:len(sound)]
    data = np.concatenate((np.zeros(samplerate * 60, dtype='int16'), data))
    # data += sound[:len(data)]
    data = data.copy()
    data.resize(len(sound))
    data += sound
    data = array("h", np.int_(data)).tobytes()

    # Write to disk
    output_file = 'song.wav'
    output_file = wave.open(output_file, "w")
    output_file.setparams((1, 2, 44100, 0, "NONE", "not compressed"))
    output_file.writeframes(data)
    output_file.close()


if __name__ == "__main__":
    my_image = "outer_password.png"
    make_wav(my_image)
