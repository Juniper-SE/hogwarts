"""
Author: Pranav Sharma
v1: 3/16/23
Comments: Initial Draft

README
Outputs the scrubbed INTERNAL tracker which is meant to include data from INTERNAL tracker which corresponds to OC PATHS present in external tracker, 
that are not explicitly excluded as per the rules we defined previously. 

Process:
    get_PATHS()
    scrub_PATHS()
    get_bugs()
    get_ondatra()

Upcoming:
Refer to spreadsheets in Sharepoint

Required Packages
#pip install Office365-REST-Python-Client
#pip install git+https://github.com/vgrem/Office365-REST-Python-Client.git
"""
import argparse
import pandas as pd
from tabulate import tabulate

#Global Args
'''
PATHS = [
'/network-instances/network-instance/protocols/protocol/bgp/global/afi-safis/afi-safi/add-PATHS/config/receive',
'/network-instances/network-instance/protocols/protocol/bgp/global/afi-safis/afi-safi/add-PATHS/config/send',
'/network-instances/network-instance/protocols/protocol/bgp/global/afi-safis/afi-safi/add-PATHS/config/send-max',
'/network-instances/network-instance/protocols/protocol/bgp/global/afi-safis/afi-safi/add-PATHS/config/eligible-prefix-policy',
'/network-instances/network-instance/protocols/protocol/bgp/global/afi-safis/afi-safi/add-PATHS/state/receive',
'/network-instances/network-instance/protocols/protocol/bgp/global/afi-safis/afi-safi/add-PATHS/state/send',
'/network-instances/network-instance/protocols/protocol/bgp/global/afi-safis/afi-safi/add-PATHS/state/send-max',
'/network-instances/network-instance/protocols/protocol/bgp/global/afi-safis/afi-safi/add-PATHS/state/eligible-prefix-policy',
'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/afi-safis/afi-safi/add-PATHS/config/receive',
'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/afi-safis/afi-safi/add-PATHS/config/send',
'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/afi-safis/afi-safi/add-PATHS/config/send-max',
'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/afi-safis/afi-safi/add-PATHS/config/eligible-prefix-policy',
'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/afi-safis/afi-safi/add-PATHS/state/receive',
'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/afi-safis/afi-safi/add-PATHS/state/send',
'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/afi-safis/afi-safi/add-PATHS/state/send-max',
'/network-instances/network-instance/protocols/protocol/bgp/neighbors/neighbor/afi-safis/afi-safi/add-PATHS/state/eligible-prefix-policy',
'/network-instances/network-instance/protocols/protocol/bgp/peer-groups/peer-group/afi-safis/afi-safi/add-PATHS/config/receive',
'/network-instances/network-instance/protocols/protocol/bgp/peer-groups/peer-group/afi-safis/afi-safi/add-PATHS/config/send',
'/network-instances/network-instance/protocols/protocol/bgp/peer-groups/peer-group/afi-safis/afi-safi/add-PATHS/config/send-max',
'/network-instances/network-instance/protocols/protocol/bgp/peer-groups/peer-group/afi-safis/afi-safi/add-PATHS/config/eligible-prefix-policy',
'/network-instances/network-instance/protocols/protocol/bgp/peer-groups/peer-group/afi-safis/afi-safi/add-PATHS/state/receive',
'/network-instances/network-instance/protocols/protocol/bgp/peer-groups/peer-group/afi-safis/afi-safi/add-PATHS/state/send',
'/network-instances/network-instance/protocols/protocol/bgp/peer-groups/peer-group/afi-safis/afi-safi/add-PATHS/state/send-max',
'/network-instances/network-instance/protocols/protocol/bgp/peer-groups/peer-group/afi-safis/afi-safi/add-PATHS/state/eligible-prefix-policy'
]
'''
INTERNAL = '/Users/pranavs/Documents/google-docs/xpaths-trackers/internal.xlsx'
SE_TRACKER = '/Users/pranavs/Documents/google-docs/xpaths-trackers/se_tracker.xlsx'
ONDATRA = '/Users/pranavs/Documents/google-docs/xpaths-trackers/ondatra.xlsx'
INT_PD = pd.read_excel(INTERNAL, "Overall Check")
SE_PD_BUGS = pd.read_excel(SE_TRACKER, "Buganizer_RunningList")
SE_PD_RFP = pd.read_excel(SE_TRACKER, "FeatureProfiles-TextProtoMappin")
ONDATRA_PD = pd.read_excel(ONDATRA)
RESULT = {}
BUGS = {}
ONDATRA_TCS = {}
#out_pd=pd.DataFrame(columns=['Xpath','Eng Support','Test Support','Test Notes'])

#Function Definitions

def parse_them_args():
    parser=argparse.ArgumentParser(description='List XPATHS and their supportability for a specific bug or all bugs')
    parser.add_argument('-b', '--bug', type=str, required=False, help='Enter Bug title string, "example: wbb://software/routing/bgp/addpath"')
    #parser.add_argument('-t', '--tracker', type=str, required=True, help='/Users/pranavs/Documents/google-docs/xpaths-trackers/internal-tracker.xlsx')
    args=parser.parse_args()
    bug=args.bug
    '''
    if (args.tracker):
        INTERNAL=args.tracker
    else:
        INTERNAL='/Users/pranavs/Documents/google-docs/xPATHS-trackers/INTERNAL-tracker.xlsx'
    '''

def get_feature_proto():
    for ref in SE_PD_RFP['HLD Document Reference']]:
        if ()


def get_paths():
    get_feature_proto()

    return path_list

def scrub_paths(paths):
    for path in paths:    
        if(INT_PD.loc[INT_PD['xpath'] == path].empty):
            print(f'Path - {path} IS NOT PRESENT IN INTERNAL TRACKER')
            RESULT[path]={  'Eng Support':'Not Tracked', 
                            'Test Support' : 'N/A',
                            'Test Notes' : 'N/A'
            }
        else:
            RESULT[path]={  'Eng Support': INT_PD.loc[INT_PD['xpath']== path, 'Support Status'].values[0], 
                            'Test Support' : INT_PD.loc[INT_PD['xpath']== path, 'Tested? Yes-No'].values[0],
                            'Test Notes' : INT_PD.loc[INT_PD['xpath']== path, 'Test Notes'].values[0]
            }                

def publish():
    out_pd = pd.DataFrame.from_dict(RESULT, orient='index')
    print(tabulate(out_pd, headers='keys', tablefmt='psql'))
    with pd.ExcelWriter(out_pd) as writer:
        out_pd.to_excel(writer, sheet_name='INTERNAL')

def main():
    #parse_them_args()    
    scrub_paths(get_paths())
    get_bugs()
    get_ondatra()
    publish()

if __name__ == "__main__": 

        main() 