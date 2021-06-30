import os
from csv import writer
import csv
from datetime import datetime
import sounddevice as sd
import scipy.io.wavfile as wav
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras
from time import sleep, perf_counter
from threading import Thread

print(tf.version.VERSION)

# Load the trained tensorflow Model
# Define the class array
model = tf.keras.models.load_model('saved_model/model')
class_names = ['motorbike', 'city', 'multiple-cars', 'single-cars']


# Method that returns the current date & time to sort the collected data
def get_date_time():
    now = datetime.now()
    return now.strftime("%d-%m---%H-%M-%S")


# Define all Folders
# wav_dir:          collected audio files
# png_dir:          spectrograms as png of the audio file
# classified_dir:   spectrograms with label as name
# csv_file:         csv file to organize the collected data
wav_dir = 'snippets/wav/' + get_date_time() + '/'
png_dir = 'snippets/png/' + get_date_time() + '/'
classified_dir = 'snippets/classified/' + get_date_time() + '/'
csv_file = 'snippets/snippets.csv'


def get_current_couter(csvfilename):
    with open(csvfilename, "r", encoding="utf-8", errors="ignore") as scraped:
        line = scraped.readlines()[-1]
        return int(line[:1])


# Snippet counter to give each audio file an ID
snippet_counter = get_current_couter(csv_file)


# Create the needed folders to save the collected data
os.mkdir(wav_dir)
os.mkdir(png_dir)
os.mkdir(classified_dir)


# Get the current timestamp that is stored in the csv file
def get_timestamp():
    now = datetime.now()
    return now.strftime("%H:%M:%S %d-%m-%y")


# Write new collected data to the csv
# Structure: TODO
def append_to_csv(list):
    with open(csv_file, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list)


# Rename the collected file, so that the label is in the filename
def rename_file(file, label):
    name = os.path.splitext(os.path.basename(file))[0]
    updated_name = classified_dir + name + '_' + label + '.png'
    os.rename(file, updated_name)
    return updated_name


# Record a 2 seconds wav file with 44100Hz
def record(file):
    fs = 44100
    seconds = 2
    print('recording...')
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    write(file, fs, recording)


# Convert the recorded wav file to spectrogram with matplotlib
def wav_to_spectrogram(audio_path, save_path, dimensions=(128, 128), noverlap=16, cmap='gray_r'):
    sample_rate, samples = wav.read(audio_path)
    fig = plt.figure()
    fig.set_size_inches(
        (dimensions[0]/fig.get_dpi(), dimensions[1]/fig.get_dpi()))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.specgram(samples, Fs=2, noverlap=noverlap)
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())
    fig.savefig(save_path, bbox_inches="tight", pad_inches=0)
    plt.close(fig)


# Get the prediction of a wav audio file that was recorded
def get_prediction(file, name_wav):
    img = keras.preprocessing.image.load_img(file, target_size=(128, 128))
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print('-----------------------------------------------------------')
    print('')
    print(
        "snippet {}: {} [{:.2f}]"
        .format(snippet_counter, class_names[np.argmax(score)], 100 * np.max(score))
    )
    print('')
    label = class_names[np.argmax(score)]
    updated_name = rename_file(file, label)

    csv_list = [snippet_counter, get_timestamp(), name_wav,
                updated_name, label, 0]
    append_to_csv(csv_list)


# Recording Task start of the script
# 1. Record 2 second audio file
# 2. Convert it to a spectrogram
# 3. Get the AI prediction and save the label
def task():
    print('Starting record task...')

    while True:
        global snippet_counter
        snippet_counter += 1

        name_wav = wav_dir + 'snippet_' + str(snippet_counter) + '.wav'
        name_png = png_dir + 'snippet_' + str(snippet_counter) + '.png'

        record(name_wav)
        wav_to_spectrogram(name_wav, name_png)
        print(f'snippet {snippet_counter} done')

        Thread(target=get_prediction(name_png, name_wav)).start()


# Start a new thread that records the audio data
def main():
    Thread(target=task).start()


if __name__ == "__main__":
    main()
