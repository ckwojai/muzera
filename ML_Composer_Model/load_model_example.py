import ML_Load_Model
import time
import joblib


start = time.time()
joblib_file = "joblib_model_composer.pkl"
model = joblib.load(joblib_file)
FILE_DIRECTORY = "L'Estro_Armonico,_Op._3,_Concerto_No._2_in_G_minor_for_two_violins,_cello_and_strings,_RV_578.ogg.mp3"

era_predicted, confidence = ML_Load_Model.predict(FILE_DIRECTORY, model)

print(era_predicted, confidence)





