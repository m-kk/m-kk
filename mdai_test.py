import mdai
from pathlib import Path
from pandas.core.frame import DataFrame
import pyinputplus as pyip

DOMAIN = 'philips.md.ai'
AUTH_TOKEN = '47bef9d52243027bee102328b014796b'
PROJ_ID_MAP = { #these are the MD.ai project ID assigned
    1: 'gaq3pBlV', #COVID
    2: 'glBE9BVE', #SI Animal
    3: 'rLRAXB2k', #SI Clinical
    4: 'W7qygRnP', #"FAST EPIQ X5-1 3D Swine"
    5: '3VB59Bov'  #FAST Clinical (Healthy Human)
}


# input: valid datafile in MD.ai file format as of 7/27/21
# output: df in format fit for output to Excel for input into Smartsheet
def format_df(df) -> DataFrame:
    # TODO

    return df

# input: valid datafile, valid output filename
def write_df_to_csv(df, outFile):
    df.to_csv(outFile, index=False)
    print('wrote csv file to: ', outFile)

# input: valid json filename ending in ".json"
# dataCategory could be "annotations", "studies", or "labels"
def df_from_json(json_file, dataCategory='annotations'):
    # read in JSON file to results as a df
    results = mdai.common_utils.json_to_dataframe(json_file)

    # pull 'dataCategory' data from the df and write to csv
    if(dataCategory == 'annotations'):
        df = results['annotations']
    elif(dataCategory == 'studies'):
        df = results['studies']
    elif(dataCategory == 'labels'):
        df = results['labels']
    else:
        print('Error: no such dataCategory: ', dataCategory)

    # create output filename by stripping .json off of filepath
    outFile = str(json_file)[:-5]
    outFile += '.csv'
    write_df_to_csv(df, outFile)

# user input handler
# important: change PROJ_ID_MAP <--> change menu order
def get_project() -> str:
    print('=============================')
    print('MD.ai project data downloader')
    print('=============================')
    print('')
    print('Enter project: ')
    print('\t1: COVID')
    print('\t2: SI Animal')
    print('\t3: SI Clinical')
    print('\t4: FAST Animal X5-1')
    print('\t5: FAST Clinical (6a Healthy Human)')

    selection = pyip.inputInt(min=1, max=5)
    return PROJ_ID_MAP[selection]


project_ID = get_project()
###mdai_client = mdai.Client(domain=DOMAIN, access_token=AUTH_TOKEN)

# Download the project data
# downloads to path given in format "mdai_philips_project_gaq3pBlV_annotations_2021-07-27-223645.json"
###mdai_client.project(project_ID, path='.',  annotations_only=True)

# find & open json file
filePath_candidates = list(Path('./').glob('mdai_philips_project_*.json'))

if(filePath_candidates): #not an empty list
    if(len(filePath_candidates) > 1): #more than one .json file here
        print('error: more than one json file here')
    else:
        print('found json file: ', filePath_candidates[0])
        df_from_json(filePath_candidates[0], 'annotations')
else:
    print('failure')

