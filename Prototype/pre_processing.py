# Import libraries
import os

# Import components
from spectrogram_forge import spectrogram_handler

# Rename files into correct format
def change_filename(audio_file_url, new_file_url):
    os.rename(audio_file_url, new_file_url)

# Create spectrogram directories
def create_directory_struct(path ,genre):
    if not os.path.exists(path + genre):
        os.mkdir(path + genre)

# Call spectrogram creation method
def spectrogram_interface(audio_path, filename, output_path):
    spectrogram_handler(audio_path, filename, 'Defualt', 'Defualt', output_path)

# Main method
def pre_process_data(stereo_genre_path, spectrogram_path):
    # Compile genre list and songs dictionary
    genre_list = os.listdir(stereo_genre_path)

    song_dict = dict()
    formated_song_dict = dict()

    for x in genre_list:
        song_dict[x] = os.listdir(stereo_genre_path + x)


    # Dictionary object with formatted audio names
    for x in genre_list:
        formated_song_dict[x] = []
        for y in song_dict[x]:
            formated_song_dict[x].append(y.replace(' ','_'))

    # Rename files
    for x in genre_list:
        for y in song_dict[x]:
            change_filename(stereo_genre_path + x + "/" + y, stereo_genre_path + x + "/" + y.replace(' ','_'))       

    # Make Spectrograms and Directories
    for x in genre_list:
        create_directory_struct(spectrogram_path, x)
        for y in formated_song_dict[x]:
            spectrogram_interface(stereo_genre_path + x + "/" + y, y, spectrogram_path + x + '/')
            # print(mono_genre_path + x + "/" + y)

    # Revert file names
    for x in genre_list:
        for y in formated_song_dict[x]:
            change_filename(stereo_genre_path + x + "/" + y, stereo_genre_path + x + "/" + y.replace('_',' '))       




