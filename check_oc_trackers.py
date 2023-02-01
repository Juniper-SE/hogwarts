"""
Author: Pranav Sharma
v1: 1/31/23
Comments: Initial Draft

README
Outputs the scrubbed internal tracker which is meant to include data from internal tracker which corresponds to OC paths present in external tracker, 
that are not explicitly excluded as per the rules we defined previously. 

Process:
1.	For each OC path in external tracker, check the internal tracker to see if that path exists, 
    if not, path will be listed in second “untracked” sheet
2.	Exclude entry if value in “Supported Status” is one of follows, added in a separate “dropped path” sheet
Exclude exclusions=['Supported', 'Support Status', 'D31', 'D32', 'D30']
3.	Remove all entries from internal tracker which are NOT present in external tracker
"""

import pandas as pd


internal='/Users/pranavs/Documents/google-docs/xpaths-trackers/internal-tracker.xlsx'
external='/Users/pranavs/Documents/google-docs/xpaths-trackers/external-tracker.xlsx'
int_pd=pd.read_excel(internal, "Overall Check")
ext_pd=pd.read_excel(external, "WBBv1-paths")
original_ext_pd = ext_pd
untracked_paths=[]
dropped_paths=pd.DataFrame(columns=['path','support status'])
untracked_pd=pd.DataFrame()
tracked_paths={}
exclusions=['Supported', 'Support Status', 'D31', 'D32', 'D30']
output_internal='/Users/pranavs/Documents/google-docs/xpaths-trackers/scrubbed_internal_tracker.xlsx'

for path in ext_pd['path']:
    if(int_pd.loc[int_pd['xpath'] == path].empty):
        print(f'Path - {path} IS NOT PRESENT IN INTERNAL TRACKER')
        untracked_paths.append(path)
    else:
        eng_s   =   int_pd.loc[  int_pd['xpath'] == path, 'Support Status' ].values[0]
        test_s  =   int_pd.loc[  int_pd['xpath'] == path, 'Tested? Yes-No' ].values[0]
        ext_s   =   ext_pd.loc[  ext_pd['path'] == path, 'JunOS Support'   ].values[0]
        if (eng_s in exclusions):
            int_pd.drop( int_pd[int_pd['xpath'] == path].index, inplace=  True   )
            print(f'============= Dropping path = {path}')
            dropped_paths.loc[len(dropped_paths)]=[path, eng_s]
        else:
            tracked_paths [path] = {
                'eng_status'    :   eng_s,
                'test_status'   :   test_s
            }

trim=[]
for line in ext_pd['path']:
    trim.append(line)

for entry in int_pd['xpath']:
    if entry in trim:
        continue
    else:
        int_pd.drop( int_pd[int_pd['xpath'] == entry].index, inplace=  True   )
        dropped_paths.loc[len(dropped_paths)]=[path, 'not requested']
        print(f'============= Non-requested path = {entry}')

untracked_pd["Un-Tracked Paths"]=pd.Series(untracked_paths)

with pd.ExcelWriter(output_internal) as writer:
    int_pd.to_excel(writer, sheet_name='internal')
    untracked_pd.to_excel(writer, sheet_name='untracked')
    dropped_paths.to_excel(writer, sheet_name='dropped')
