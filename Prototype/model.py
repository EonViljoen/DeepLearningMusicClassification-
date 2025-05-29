import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator as IDG
from keras.models import model_from_json

def train_model(spectrogram_path, class_nr, epoch_nr, drop_out, hidden_layer_nr, convolution_filter_1_nr, convolution_filter_2_nr, convolution_filter_3_nr):
    # Preprocessing the Training set
    train_datagen = IDG(rescale = 1./255,
                                    shear_range = 0.2,
                                    zoom_range = 0.2,
                                    horizontal_flip = True)
    training_set = train_datagen.flow_from_directory(spectrogram_path,
                                                    target_size = (64, 64),
                                                    batch_size = 32,
                                                    class_mode = 'categorical')

    # Preprocessing the Test set
    test_datagen = IDG(rescale = 1./255)
    test_set = test_datagen.flow_from_directory('Data/Testing',
                                                target_size = (64, 64),
                                                batch_size = 32,
                                                class_mode = 'categorical')
    #Building the CNN

    # Initialising the CNN
    cnn = tf.keras.models.Sequential()

    # Convolution
    cnn.add(tf.keras.layers.Conv2D(filters=convolution_filter_1_nr, kernel_size=3, activation='relu', input_shape=[64, 64, 3]))

    # Pooling
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

    # Adding a second convolutional layer
    cnn.add(tf.keras.layers.Conv2D(filters=convolution_filter_2_nr, kernel_size=3, activation='relu'))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

    # Adding a third convolutional layer
    cnn.add(tf.keras.layers.Conv2D(filters=convolution_filter_3_nr, kernel_size=3, activation='relu'))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

    # Flattening
    cnn.add(tf.keras.layers.Flatten())

    # Full Connection
    cnn.add(tf.keras.layers.Dense(units=hidden_layer_nr, activation='relu'))
    cnn.add(tf.keras.layers.Dropout(drop_out))

    # Output Layer
    cnn.add(tf.keras.layers.Dense(units=class_nr, activation='softmax'))

    # Training the CNN

    # Compiling the CNN
    cnn.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

    # Training the CNN on the Training set and evaluating it on the Test set
    cnn.fit(x = training_set, validation_data = test_set, epochs = epoch_nr)

    # Save model
    # serialize model to JSON
    model_json = cnn.to_json()

    with open("trained_model.json", "w") as json_file:
        json_file.write(model_json)

    # serialize weights to HDF5
    cnn.save_weights("weights.h5")
    # print("Saved model to disk")

    accuracy = cnn.evaluate(x=test_set,batch_size=32)
    # print('Model accuracy: ', accuracy[1])

    return accuracy[1]
