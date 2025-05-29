# Import libraries
from subprocess import Popen, PIPE, STDOUT
import os
from mutagen.flac import FLAC

# Get current working directory
currentPath = os.path.dirname(os.path.realpath(__file__)) 

def spectrogram_handler(audio_path, filename, sample_rate, duration, output_path):
    # Creation variables
    if sample_rate is 'Defualt':
            sample_rate = 22050 
    if duration is 'Defualt':
            duration = 3
    total_duration = audio_length(audio_path)

    # Get 3 seconds of start audio
    create_spectrogram(audio_path, filename + '01', sample_rate, duration,  ((total_duration*(1/4))-1), output_path)

    # Get 3 seconds of middle audio
    create_spectrogram(audio_path, filename + '02', sample_rate, duration, ((total_duration/2)-1), output_path)

    # Get 3 seconds of end audio
    create_spectrogram(audio_path, filename + '03', sample_rate, duration,  ((total_duration*(3/4))-1), output_path)

# Create spectrogram for training
def create_spectrogram(audio_path, filename, sample_rate, duration, offset, output_path):
    # Create terminal command
    command = "sox '" + audio_path + "' -n rate " + str(sample_rate) + " remix 2 trim " + str(offset) + " " + str(duration) + " spectrogram -r -o '" + output_path + filename + ".png'"

    # Format for shell use
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)

    # Pass to shell
    output, errors = p.communicate()
    

    if errors:
	    print(errors)

#  Special method for prediction spectrogram
def create_spectrogram_for_predict(audio_path, filename, sample_rate, duration, offset, output_path):
    command = "sox '" + audio_path + "' -n rate " + str(sample_rate) + " remix 2 trim " + str(offset) + " " + str(duration) + " spectrogram -r -o '" + output_path + filename + ".png'"

    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)

    output, errors = p.communicate()

    # print(output)

    if errors:
	    print(errors)

    return (output_path + filename + '.png')       

# Get full length of audio file in seconds
def audio_length(audio_path):
    audio_file = FLAC(audio_path)
    info = audio_file.info
    return info.length