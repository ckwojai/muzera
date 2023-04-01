import load_model

FILE_DIRECTORY = ".\wavs\Beethoven, Ludwig van, Fantasia for Piano, Op.77, cr2SukqCdKs.mid.wav"

era_predicted = load_model.predict(FILE_DIRECTORY)

print(era_predicted)