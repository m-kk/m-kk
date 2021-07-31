import mdai
from pathlib import Path
from pandas.core.frame import DataFrame
import pyinputplus as pyip
import send2trash

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
def format_df(df, project_ID) -> DataFrame:
    df = df[['StudyInstanceUID', 'dataset', 'number', 'groupId', 'groupName', 'labelName', 'note']]
    df = df.sort_values(by=['dataset', 'number'])
    studyID = ''
    annoGroup = ''
    #annoGroupName = ''
    labelName = ''
    annoNote = ''

    if(project_ID == 'gaq3pBlV'):    #COVID
        #set up the output df to match tracker columns
        # columns = {
        #     'Study ID':[],
        #     'Site':[],
        #     'Day':[],
        #     'Transducer':[],
        #     'Exam #':[],
        #     'Lung Zone':[],
        #     'Orientation':[],
        #     'VA Read (MZ)':[],
        #     'VA Image Quality Comments (MZ)':[],
        #     'VA Comments (MZ)':[],
        #     'VA Read (NS)':[],
        #     'VA Image Quality Comments (NS)':[],
        #     'VA Comments (NS)':[],
        #     'VA Read (MK)':[],
        #     'VA Image Quality Comments (MK)':[],
        #     'VA Comments (MK)':[]
        # }
        columns = {
            'Dataset':[],
            'Exam #':[],
            'Lung Zone':[],
            'Orientation':[],
            'VA Read (MZ)':[],
            'VA Comments (MZ)':[],
            'VA Read (NS)':[],
            'VA Comments (NS)':[],
            'VA Read (MK)':[],
            'VA Comments (MK)':[]
        }
        working_df = DataFrame(columns)
        # next_row = {
        #     'Study ID':'',
        #     'Site':'',
        #     'Day':'',
        #     'Transducer':'',
        #     'Exam #':'',
        #     'Lung Zone':'',
        #     'Orientation':'',
        #     'VA Read (MZ)':'',
        #     'VA Image Quality Comments (MZ)':'',
        #     'VA Comments (MZ)':'',
        #     'VA Read (NS)':'',
        #     'VA Image Quality Comments (NS)':'',
        #     'VA Comments (NS)':'',
        #     'VA Read (MK)':'',
        #     'VA Image Quality Comments (MK)':'',
        #     'VA Comments (MK)':''
        # }
        working_row = {
            'Dataset': '',
            'Exam #': '',
            'Lung Zone': '',
            'Orientation': '',
            'VA Read (MZ)': '',
            'VA Comments (MZ)': '',
            'VA Read (NS)': '',
            'VA Comments (NS)': '',
            'VA Read (MK)': '',
            'VA Comments (MK)': ''
        }

        #pull input df data and put it in the output df
        for row in df.itertuples():

            if(row.StudyInstanceUID != studyID): #this is either a new exam or the very first row
                if(studyID != ''): #this is a new exam && not the very first row
                    #write previous exam's data
                    working_df = working_df.append(working_row, ignore_index=True)
                    #reset our working row
                    working_row['Dataset'] = ''
                    working_row['Exam #'] = ''
                    working_row['Lung Zone'] = ''
                    working_row['Orientation'] = ''
                    working_row['VA Read (MZ)'] = ''
                    working_row['VA Comments (MZ)'] = ''
                    working_row['VA Read (NS)'] = ''
                    working_row['VA Comments (NS)'] = ''
                    working_row['VA Read (MK)'] = ''
                    working_row['VA Comments (MK)'] = ''
                # else: #this is the very first row
                
                working_row['Orientation'] = 'longitudinal' #default is longi and is changed w/the below label
                studyID = row.StudyInstanceUID
                working_row['Dataset'] = row.dataset
                working_row['Exam #'] = str(row.number)

            #process the row
            annoGroup = row.groupId
            # annoGroupName = row.groupName
            labelName = row.labelName
            if(labelName == 'None'): labelName = ""
            annoNote = str(row.note)
            if(annoNote == 'None'): annoNote = ""

            #check for zone
            if(labelName == 'Zone'):
                #annoNote = annoNote.replace('t', '')
                #annoNote = annoNote.replace('T', '')
                working_row['Lung Zone'] = annoNote
            #handle orientation
            elif(labelName == 'Transverse'):
                working_row['Orientation'] = 'transverse'
            elif(annoGroup == 'G_dga6wY'): #MZ
                #add to mz columns (annotation label & annotation note)
                if(labelName != 'MZ Complete'):
                    if(working_row['VA Read (MZ)'] != ""):
                        labelName = "\n" + labelName
                    working_row['VA Read (MZ)'] += labelName
                    if(working_row['VA Comments (MZ)'] != "" and annoNote != ""):
                        annoNote = "; " + annoNote
                    working_row['VA Comments (MZ)'] += annoNote
            elif(annoGroup == 'G_jYoLjR'): #NS
                #add to ns columns
                if(labelName != 'NS Complete'):
                    if(working_row['VA Read (NS)'] != ""):
                        labelName = "\n" + labelName
                    working_row['VA Read (NS)'] += labelName
                    if(working_row['VA Comments (NS)'] != "" and annoNote != ""):
                        annoNote = "; " + annoNote
                    working_row['VA Comments (NS)'] += annoNote
            elif(annoGroup == 'G_zYPwag'): #MK
                #add to mk columns
                if(labelName != 'MK Complete'):
                    if(working_row['VA Read (MK)'] != ""):
                        labelName = "\n" + labelName
                    working_row['VA Read (MK)'] += labelName
                    if(working_row['VA Comments (MK)'] != "" and annoNote != ""):
                        annoNote = "; " + annoNote
                    working_row['VA Comments (MK)'] += annoNote
                

    elif(project_ID == 'glBE9BVE'): #SI Animal
        x = 1+2
    elif(project_ID == 'rLRAXB2k'): #SI Clinical
        x = 1+2
    elif(project_ID == 'W7qygRnP'): #"FAST EPIQ X5-1 3D Swine"
        x = 1+2
    elif(project_ID == '3VB59Bov'): #FAST Clinical (Healthy Human)
        x = 1+2
    else:
        print('Unknown project selected')
 
    return working_df

# input: valid datafile, valid output filename
def write_df_to_csv(df, outFile):
    df.to_csv(outFile, index=False)
    print('wrote csv file to: ', outFile)

# input: valid json filename ending in ".json"
# dataCategory could be "annotations", "studies", or "labels"
def df_from_json(json_file, dataCategory='annotations') -> DataFrame:
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

    return df

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
        jsonFilePath = filePath_candidates[0]
        print('found json file: ', jsonFilePath)
        source_df = df_from_json(jsonFilePath)

        # create output filename by stripping .json off of filepath
        outFilename = str(jsonFilePath)[:-5]
        outFilename += '.csv'

        output_df = format_df(source_df, project_ID)

        write_df_to_csv(output_df, outFilename)

        #delete downloaded json file
        ###send2trash.send2trash(jsonFilePath.name)
else:
    print('failure')

