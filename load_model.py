import librosa
import numpy
import joblib
import sklearn

# def get_subdirectories(a_dir):
#     return [name for name in os.listdir(a_dir)
#             if os.path.isdir(os.path.join(a_dir, name))]


def get_sample_array(dataset_dir, samp_rate):
    # path_of_audios = librosa.util.find_files(dataset_dir + "/" + folder_name)
    #path_of_audios = librosa.util.find_files(dataset_dir)
    
    # audios = []
    # labels = []
    
    # ds = pandas.read_csv("ds_labeled_with_midi.csv")
    x, _ = librosa.load(dataset_dir, sr=samp_rate, duration=60.0)
    
    """
    for audio in path_of_audios:
        x, sr = librosa.load(audio, sr=samp_rate, duration=60.0)
        audios.append(x)
        # print(audio)
        audio_name = audio.split("\\")[5][:-8]
        label = ds.loc[ds['audio_name'] == audio_name]['era'].values[0]
        
        labels.append(label)
    """
        
    audio_numpy = numpy.array(x)

    return audio_numpy


def extract_features(signal, sample_rate, frame_size, hop_size):
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y=signal, frame_length=frame_size, hop_length=hop_size)
    spectral_centroid = librosa.feature.spectral_centroid(y=signal, sr=sample_rate, n_fft=frame_size,
                                                          hop_length=hop_size)
    spectral_contrast = librosa.feature.spectral_contrast(y=signal, sr=sample_rate, n_fft=frame_size,
                                                          hop_length=hop_size)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=signal, sr=sample_rate, n_fft=frame_size,
                                                            hop_length=hop_size)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=signal, sr=sample_rate, n_fft=frame_size, hop_length=hop_size)
    mfccs = librosa.feature.mfcc(y=signal, sr=sample_rate, n_fft=frame_size, hop_length=hop_size)

    return [

        numpy.mean(zero_crossing_rate),
        numpy.std(zero_crossing_rate),
        numpy.mean(spectral_centroid),
        numpy.std(spectral_centroid),
        numpy.mean(spectral_contrast),
        numpy.std(spectral_contrast),
        numpy.mean(spectral_bandwidth),
        numpy.std(spectral_bandwidth),
        numpy.mean(spectral_rolloff),
        numpy.std(spectral_rolloff),

        numpy.mean(mfccs[1, :]),
        numpy.std(mfccs[1, :]),
        numpy.mean(mfccs[2, :]),
        numpy.std(mfccs[2, :]),
        numpy.mean(mfccs[3, :]),
        numpy.std(mfccs[3, :]),
        numpy.mean(mfccs[4, :]),
        numpy.std(mfccs[4, :]),
        numpy.mean(mfccs[5, :]),
        numpy.std(mfccs[5, :]),
        numpy.mean(mfccs[6, :]),
        numpy.std(mfccs[6, :]),
        numpy.mean(mfccs[7, :]),
        numpy.std(mfccs[7, :]),
        numpy.mean(mfccs[8, :]),
        numpy.std(mfccs[8, :]),
        numpy.mean(mfccs[9, :]),
        numpy.std(mfccs[9, :]),
        numpy.mean(mfccs[10, :]),
        numpy.std(mfccs[10, :]),
        numpy.mean(mfccs[11, :]),
        numpy.std(mfccs[11, :]),
        numpy.mean(mfccs[12, :]),
        numpy.std(mfccs[12, :]),
        numpy.mean(mfccs[13, :]),
        numpy.std(mfccs[13, :]),
    ]

def create_array(file_dir):
    samp_rate = 44100
    frame_size = 2048
    hop_size = 512
    dataset_dir = file_dir

    rows = []
    # is_created = False

    sample_array = get_sample_array(dataset_dir, samp_rate)
    row = extract_features(sample_array, samp_rate, frame_size, hop_size)
    rows.append(row)

    dataset_numpy = numpy.array(rows)

    """ 
    for sample_array in sample_arrays:

        row = extract_features(sample_array, samp_rate, frame_size, hop_size)
        if not is_created:
            dataset_numpy = numpy.array(row)
            is_created = True
        elif is_created:
            dataset_numpy = numpy.vstack((dataset_numpy, row)) 
    """

    joblib_file = "joblib_scaler.pkl"

    scaler = joblib.load(joblib_file)
    dataset_numpy = scaler.transform(dataset_numpy)

    """
    Feature_Names = ['meanZCR', 'stdZCR', 'meanSpecCentroid', 'stdSpecCentroid', 'meanSpecContrast', 'stdSpecContrast',
                     'meanSpecBandwidth', 'stdSpecBandwidth', 'meanSpecRollof', 'stdSpecRollof',
                     'meanMFCC_1', 'stdMFCC_1', 'meanMFCC_2', 'stdMFCC_2', 'meanMFCC_3', 'stdMFCC_3',
                     'meanMFCC_4', 'stdMFCC_4', 'meanMFCC_5', 'stdMFCC_5', 'meanMFCC_6', 'stdMFCC_6',
                     'meanMFCC_7', 'stdMFCC_7', 'meanMFCC_8', 'stdMFCC_8', 'meanMFCC_9', 'stdMFCC_9',
                     'meanMFCC_10', 'stdMFCC_10', 'meanMFCC_11', 'stdMFCC_11', 'meanMFCC_12', 'stdMFCC_12',
                     'meanMFCC_13', 'stdMFCC_13'
                     ]
    dataset_pandas = pandas.DataFrame(dataset_numpy, columns=Feature_Names)

    dataset_pandas["genre"] = labels
    dataset_pandas.to_csv("data_set.csv", index=False)
    print("Data set has been created and sent to the project folder!")
    """

    return dataset_numpy


def predict(file_dir):
    X_test = create_array(file_dir)
    joblib_file = "joblib_model.pkl"

    model = joblib.load(joblib_file)
    result = model.predict(X_test)

    return result[0]
