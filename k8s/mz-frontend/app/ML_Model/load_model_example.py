import Era_Classifier
import Composer_Classifier
import time
import joblib


start = time.time()
joblib_file1 = "joblib_model.pkl"
joblib_file2 = "joblib_model_composer.pkl"
model1 = joblib.load(joblib_file1)
model2=joblib.load(joblib_file2)
FILE_DIRECTORY = "Liszt, Franz, Historische ungarische Bildnisse, S.205, SZFW9MWC27E.mid.wav"

era_predicted, era_confidence = Era_Classifier.predict(FILE_DIRECTORY, model1)
composer_predicted, composer_confidence = Composer_Classifier.predict(FILE_DIRECTORY, model2)
print(era_predicted, era_confidence)
print (composer_predicted, composer_confidence)





