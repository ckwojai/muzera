import pandas as pd

# From GiantMIDI's github, they somehow chose tab as their delimiter instead of the traditional ","
metadata = pd.read_csv("../full_music_pieces_youtube_similarity_pianosoloprob_split.csv", sep='\t')
composers = pd.read_excel("../Composers.xlsx", usecols=['name', 'era']) # only read name and era for now as only these columns are used

# Helper function to do apply() on metadata dataframe
def findEra(x):
    era = 'unclear'
    name = x['firstname']+' '+x['surname']

    # Extract the era label from Composers.xlsx dataframe
    composer = composers.loc[composers['name']==name, 'era']

    if not composer.empty:
        era = composer.iloc[0]

    return era


metadata['era'] = metadata.apply(findEra, axis=1) 
metadata.to_csv("../metadata_labeled.csv")
