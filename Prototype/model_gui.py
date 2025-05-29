# Import libraries
import PySimpleGUI as sg  
import os 

# Import components
import pre_processing
import model
import predict
import spectrogram_forge

# Get current working directory
currentPath = os.path.dirname(os.path.realpath(__file__)) 

def main():
    # Global variables
    global stereo_genre_path
    global nr_classes
    global spectrogram_store_path
    global nr_epoch
    global drop_out_rate
    global nr_hidden_nodes
    global nr_filters_1
    global nr_filters_2
    global nr_filters_3
    global model_path
    global weight_path
    global predict_path
    global accuracy
    
    # Select theme
    sg.ChangeLookAndFeel('DarkBlue6')

    # Path selection section for pre-processing
    path_sect = [[  sg.Text('Path to Genre Folders containing dataset'), 
                            sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), 
                            sg.FolderBrowse()], [  sg.Text('Path to Spectrogram Folders to save      '), 
                            sg.In(size=(25,1), enable_events=True ,key='-SPECTROGRAM-PATH-', justification='right'), 
                            sg.FolderBrowse()]
                            ]

    # Number of genre variable display
    dataset_variables = sg.Frame('Data Variables retrieved', layout=[
        [sg.Text('Number of genres detected: ', key='-CLASSES-', size=(30,1))],
    ])

    # Spectrogram viewer component
    spectrogram_viewer = [
        [sg.Text(size=(115, 1), key="-TOUT-")],
        [sg.Image(key="-IMAGE-")],
    ]

    # Prediction path selection fields
    prediction_sect = [[sg.Text('Select pre-compiled model    '), sg.In(size=(25,1), enable_events=True ,key='-MODEL-'), sg.FileBrowse()],
            [sg.Text('Select pre-compiled weights '), sg.In(size=(25,1), enable_events=True ,key='-WEIGHT-'), sg.FileBrowse()],
            [sg.Text('Audio Track to Predict Genre'), sg.In(size=(25,1), enable_events=True ,key='-PREDICT-'), sg.FileBrowse()]]

    # First section compilation
    first_sect = [  sg.Column(path_sect),
                    sg.Button('Perform Pre-proccesing'),
                    sg.VSeparator(),
                    dataset_variables
                    ]

    # Second section compilation of CNN hyperparameters
    second_sect = [sg.Frame('Data Variables retrieved', layout=[
        [sg.Text('Number of Epochs                                     '), sg.In(size=(5,1), enable_events=False, default_text=10)], #1
        [sg.Text('Drop out Rate                                            '), sg.In(size=(5,1), enable_events=False, default_text=0.5)], #2
        [sg.Text('Amount of Hidden Layer Nodes                   '), sg.In(size=(5,1), enable_events=False, default_text=128)], #3
        [sg.Text('Number of filters in first convolution layer     '), sg.In(size=(5,1), enable_events=False, default_text=32)], #4
        [sg.Text('Number of filters in sedond convolution layer'), sg.In(size=(5,1), enable_events=False, default_text=32)], #5
        [sg.Text('Number of filters in third convolution layer    '), sg.In(size=(5,1), enable_events=False, default_text=64)] #6
        ]), sg.Button('Train Model')
    ]

    # Third section compilation
    third_sect = [  sg.Column(prediction_sect),
                    sg.Button('Perform Prediction'),
                    sg.VSeparator(),
                    sg.Column(spectrogram_viewer)
                    ]


    # Layout manager
    layout =    [first_sect,
                [sg.Text('_'  * 80)],
                second_sect,
                [sg.Text('_'  * 80)],
                third_sect
                ]

    # Window parameters
    window = sg.Window('Music Genre Identification', layout, grab_anywhere=False, element_justification='c')

    while True:
            # Window information
            event, values = window.read()
            # Close button
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            
            # Pre-processing event 
            if event == '-FOLDER-':
                stereo_genre_path = os.path.abspath(values['-FOLDER-'])
                nr_classes = len(os.listdir(stereo_genre_path))
                window['-CLASSES-'].update('Number of genres detected: ' + str(nr_classes))

            elif event == '-SPECTROGRAM-PATH-':
                spectrogram_store_path = os.path.abspath(values['-SPECTROGRAM-PATH-'])

            elif event == 'Perform Pre-proccesing':
                pre_processing.pre_process_data(stereo_genre_path + '/', spectrogram_store_path + '/')

            # CNN training event 
            elif event == 'Train Model':
                nr_epoch = int(values[1])
                drop_out_rate = float(values[2])
                nr_hidden_nodes = int(values[3])
                nr_filters_1 = int(values[4])
                nr_filters_2 = int(values[5])
                nr_filters_3 = int(values[6])

                sg.popup('Model is training')

                accuracy = model.train_model(spectrogram_store_path, int(nr_classes),
                nr_epoch, drop_out_rate, nr_hidden_nodes, 
                nr_filters_1, nr_filters_2, nr_filters_3)

                sg.popup('Model Trained', 'Accuracy: {:.2f}'.format(accuracy*100))

            # Prediction event
            elif event ==  '-MODEL-':
                model_path = os.path.abspath(values['-MODEL-'])

            elif event ==  '-WEIGHT-':
                weight_path = os.path.abspath(values['-WEIGHT-'])
                
            elif event == '-PREDICT-':
                try:
                    predict_path = os.path.abspath(values['-PREDICT-'])

                    spectrogram_forge.create_spectrogram(predict_path, '/spect' ,22050, 0, '', currentPath)

                
                    window["-TOUT-"].update(predict_path)
                    window["-IMAGE-"].update(filename=currentPath + '/' +'spect' + ".png")

                except:
                    pass
            elif event == 'Perform Prediction':    
                loaded_model = predict.load_model(model_path, weight_path)
                prediction_spectrograms = predict.prediction_spectrograms(predict_path, 'pred', 'Defualt', 'Defualt', predict_path, nr_classes)
                decision_matrix = predict.make_decision(prediction_spectrograms, nr_classes, loaded_model)

                sg.popup('Genre predicted was ' +  predict.most_frequent(decision_matrix), title='Results')

    window.close()

# Driver
if __name__ == "__main__":
    main()