import soundfile as sf
from subprocess import Popen, PIPE, STDOUT
import os


currentPath = os.path.dirname(os.path.realpath(__file__)) 

# check if audio is mono channel
def check_mono(audio_file):
    audio = sf.SoundFile(audio_file)
    if audio.channels is 2:
        audio.close()
        return 2
    else:
        audio.close()
        return 1

# convert stereo audio to mono
def convert_to_mono(stereo_path, audio_file, mono_path):

    # Create ffmpeg command
    command = "ffmpeg -i " + stereo_path + "/" + audio_file + " -ac 2 " + mono_path + "/" + audio_file

    # Run ffmpeg command as terminal command through Python
    p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
    output, errors = p.communicate()

    # print(output)
    if errors:
	    print(errors)
    # print(command)