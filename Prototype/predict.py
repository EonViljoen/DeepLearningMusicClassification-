# Import libraries
from keras.models import model_from_json
import numpy as np
from keras.preprocessing import image
import os

# Import components
import spectrogram_forge

# Get current working directory
currentPath = os.path.dirname(os.path.realpath(__file__)) 

# load json and create model
def load_model(mdel_json, model_h5):
    json_file = open(mdel_json, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    # load weights into new model
    loaded_model.load_weights(model_h5)

    return loaded_model

# Spectrogram creation method for predictions
def prediction_spectrograms(audio_path, filename, sample_rate, duration, output_path, nr_classes):
    if sample_rate is 'Defualt':
        sample_rate = 22050 
    if duration is 'Defualt':
        duration = 3
    total_duration = spectrogram_forge.audio_length(audio_path)

    spectrogram_dir = []

    for i in range(1, nr_classes + 3):
        spectrogram_forge.create_spectrogram_for_predict(audio_path, filename + 'Predict_' + str(i), sample_rate, duration,  ((total_duration*(i/(nr_classes+3)))-1), output_path)

        spectrogram_dir.append(output_path + filename + 'Predict_' + str(i) + ".png")

    return spectrogram_dir


def make_prediction(loaded_model, filepath):
    # Making a single prediction
    test_image = image.load_img(filepath, target_size = (64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = loaded_model.predict(test_image)

    # Genre identification array
    genre_num = np.argmax(np.max(result, axis=0))
    genre_prediction =  {0: 'Classical',
                        1: 'Metal',
                        2: 'Rap'}

    return genre_prediction[genre_num]

# Use prediction spectrograms to make prediction, compiling array of predictions
def make_decision(spectrogram_dir, nr_classes, loaded_model):
    decision_arr = []


    for i in range(len(spectrogram_dir)):
        decision_arr.append(make_prediction(loaded_model, spectrogram_dir[i]))

    return decision_arr

# Most frequent entry in decision array
def most_frequent(List): 
    return max(set(List), key = List.count) 
