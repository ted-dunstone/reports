from PxS_util import get_df
import PxS_calc as pxc
import numpy as np
import json
import yaml
import os
import pickle
import pandas as pd
from datetime import datetime, timedelta
from px_build_doc.util import update_vars, fetch_vars, fetch_var

def read_variables_yaml(fn):
    if os.path.isfile(fn):
        stream = open(fn, 'r')
        return yaml.load(stream,Loader=yaml.Loader)
    else:
        return {}

def read_json_file(fn):
    if os.path.isfile(fn):
        json_file = open(fn)
        return json.load(json_file)
    else:
        return {}

class Params():
    """ Define the parameters for the script """
    def __init__(self, ps_dict=None, fn=None):
        # Set default values
        self.threshold = None #Used as threshold for analysis.
        self.fpr_arry = [0.1, 0.05, 0.01, 0.001] #False Positive Rate/Ratio.
        self.data_type = 'data type'
        self.test_type = 'test type' #Used in Introduction.
        self.label = 'Fingerprint'
        self.results_probe_col = '' #Used in reading data.
        self.results_gallery_col = '' #Used in reading data.
        self.results_scores_col = '' #Used in reading data.
        self.results_filter_col = '' #Used in reading data.
        self.results_rank_col = '' #Used in reading data.
        self.truth_probe_col = '' #Used in reading data.
        self.truth_gallery_col = '' #Used in reading data.
        self.truth_match_col = 'truth' #Used in reading data.
        self.show_types = '*' #indicate what finger positions to show.
        self.gallery_size = None
        self.null_string = 'NULL'
        if fn is not None:
            self.read_json(fn)
        if ps_dict is not None:
            self.read_dictionary(ps_dict)

    def read_json(self, fn):
        ps = read_json_file(fn)
        self.read_dictionary(ps)

    #ps is a dictionary
    def read_dictionary(self, ps):
        self.__dict__.update(ps) #TODO update only existing keys.
        self.lower_col_names()
        self.show_types.strip()
    
    def lower_col_names(self):
        lowercase_attributes = ['results_filter_col',
                                'results_gallery_col',
                                'results_probe_col',
                                'results_rank_col',
                                'results_scores_col',
                                'truth_gallery_col',
                                'truth_match_col',
                                'truth_probe_col']
        for atr in lowercase_attributes:
            self.__dict__[atr] = self.__dict__[atr].replace('_','').lower()

def find_column_name(search_arr, columns):
    use_col = None
    for name in search_arr:
        if name in columns:
            use_col = name
            break
    return use_col

#Read in the data TODO wrap in try except block
# truth_data_path : str
# truth_col : dict
# score_col : dict TODO add filter column
# null_string : str
def read_data_simple(score_data_path,
        null_string="null"):
    valid_df = True
    is_identification = True
    errors = []
    col = {
        'pid':"pid",
        'gid':"gid",
        'rank':'rank',
        'score':"score",
        'truth':"truth",
        'ppos':None,
        'gpos':None,
        'fltr':'filter'
    }

    score_data  = get_df(score_data_path)
    score_data['filter'] = 'ALL' #['Default' for s in score_data] 
    score_data['pid'] = [os.path.basename(s['probe']).split('_')[0] for i,s in score_data.iterrows()]
    score_data['gid'] = [os.path.basename(s['candidate']).split('_')[0] for i,s in score_data.iterrows()]
    score_data["score"] = 1.0-pd.to_numeric(score_data["score"], errors='coerce')
    score_data["rank"] = pd.to_numeric(score_data["rank"], errors='coerce')
    score_data['truth'] = score_data['match'].replace({"True": True, "False": False})
    

    # important: rank is not on person_id but on probe_id
    ## score_data.sort_values('score',inplace=True,ascending=False)
    ## tmp = score_data.groupby('probe').size()
    ## rank=tmp.map(range)
    ## rank = [item+1 for sublist in rank for item in sublist]
    ## score_data['rank'] = rank

    score_data.to_csv('output.csv')

    # build rank
    #  raise ValueError(str(score_data[['score',"match"]]))
    #print(score_data)
    #score_data['rank'] = score_data.groupby('probe')['score'].rank(ascending=False)

    if valid_df and len(errors) == 0:
        return score_data, col, is_identification, []
    else:
        return None , None , None, errors

#Read in the data TODO wrap in try except block
# truth_data_path : str
# truth_col : dict
# score_col : dict TODO add filter column
# null_string : str
def read_data(truth_data_path, job_data_path, 
        truth_col = {'pid':'probeid','gid':'galleryid','truth':'truth'},
        results_col = {'pid':'probeid','gid':'galleryid','score':'score','rank':'rank'},
        null_string="null"):
    valid_df = True
    is_identification = False
    errors = []
    # Extract and clean up source data to not have leading or trailing spaces, and also standardise names
    truth_table = get_df(truth_data_path)
    truth_table.columns = [x.replace('_','').lower() for x in truth_table.columns]
    
    #required columns, find the required column in the df columns.
    #These are global variables.
    c_tpid = find_column_name([truth_col['pid'], 'probeepi', 'probeid'], truth_table.columns)
    c_tgid = find_column_name([truth_col['gid'], 'galleryepi', 'galleryid'], truth_table.columns)
    c_truth = find_column_name([truth_col['truth'], 'truth', 'match'], truth_table.columns)
    truth_required_headers = [c_tpid, c_tgid, c_truth]
    
    if None in truth_required_headers:
        raise Exception("""A required header for the truth table is not provided. 
                        Check that the data has a probeid, galleryid, and match column. 
                        These column names can be set in the parameter file.""")
    
    truth_table[c_truth] = truth_table[c_truth].apply(lambda x : x.lower())
    truth_table[c_truth] = truth_table[c_truth] == 'true' #Needs check
    
    # Replace a string (default 'NULL') with null value
    truth_table = truth_table.replace(null_string, np.nan)
    
    # Extract and clean up job data to not have leading or trailing spaces
    score_data  = get_df(job_data_path)
    score_data.columns = [x.replace('_','').lower() for x in score_data.columns]
    
    # Replace a string (default 'NULL') with null value
    score_data = score_data.replace(null_string, np.nan)
    
    score_data_dirty = score_data
    
    #required columns, find the required column in the df columns.
    #These are global variables. TODO ensure all functions that use these names have the variable passed as a parameter.
    c_rpid = find_column_name([results_col['pid'],'probeepi','probeid'], score_data.columns)
    c_rgid = find_column_name([results_col['gid'],'galleryepi','galleryid'], score_data.columns)
    c_score = find_column_name([results_col['score'],'score','scores'], score_data.columns)
    
    #columns specific for fingerprints
    c_ppos = 'ppos'
    c_gpos = 'gpos'
    #code sets filter for fingerprints to either ppos or gpos.
    
    #convert null values to unknown position information.
    score_data[c_ppos] = score_data.apply(lambda x : x[c_ppos] if pd.notnull(x[c_ppos]) else 'Unknown', axis=1)
    score_data[c_gpos] = score_data.apply(lambda x : x[c_gpos] if pd.notnull(x[c_gpos]) else 'Unknown', axis=1)
    c_fltr = c_ppos
    if 'Unknown' in list(score_data[c_fltr].unique()): #test if incomplete probe finger position
        if 'Unknown' not in list(score_data[c_gpos].unique()): #test if complete gallery finger position
            c_fltr = c_gpos #use gallery finger position instead
        else:
            pass
    
    score_required_headers = [c_rpid, c_rgid, c_score, c_ppos, c_gpos]
    
    if not set(score_required_headers).issubset(set(score_data.columns)):
        raise Exception("""A required header for the score data file is not provided. 
                        Check that the data has probeid, galleryid, score, ppos, gpos. 
                        These column names can be set in the parameter file.""")
    
    
    #check if id columns have data in them
    if score_data[c_rpid].isnull().all(): #Check if all values are null
        raise Exception(f"probeid column in job data is all null. User specified column was {c_rpid}.")
    if score_data[c_rgid].isnull().all(): 
        raise Exception(f"galleryid column in job data is all null. User specified column was {c_rgid}.")
    
    #Filter out records that do not have a score value.
    missing_score_df = pxc.missing_score(score_data, c_score)
    score_data.drop(missing_score_df.index, axis=0, inplace=True)
    
    #Filter out records that have a null value in either the probe or gallery id.
    score_data.dropna(subset=[c_rpid, c_rgid], axis='index', inplace=True)
    
    # Format position data to remove impresion information.
    score_data[c_ppos] = score_data[c_ppos].apply(lambda x: x.split('_')[0] if isinstance(x, str) else x)
    score_data[c_gpos] = score_data[c_gpos].apply(lambda x: x.split('_')[0] if isinstance(x, str) else x)
    
    #check for identification
    c_rank = find_column_name([results_col['rank'], 'rank'], score_data.columns)
    if c_rank is None:
        is_identification = False
    else:
        is_identification = len(score_data[c_rank].unique()) > 1
    is_verification = not is_identification

    # ensure columns can be joined on when they contain strings
    score_data = score_data.astype({c_rpid: 'str',c_rgid: 'str'})
    truth_table = truth_table.astype({c_tpid: 'str',c_tgid: 'str'})
    
    # Merges truth data and job data
    merged_df = pd.merge(score_data, truth_table[[c_tpid,c_tgid,c_truth]],how='left', left_on=[c_rpid,c_rgid],
                        right_on=[c_tpid,c_tgid])
    #id columns for merged df
    c_pid = c_rpid
    c_gid = c_rgid

    # Replace matches not in truth table with False for truth column
    merged_df[c_truth].fillna(False, inplace=True)
    
    try:
        merged_df[c_score] = merged_df[c_score].astype('float64')
        if is_identification:
            merged_df[c_rank] = merged_df[c_rank].astype('int64')
    except Esception as ex:
        errors.append(f"Unable to convert scores or rank data type due to the following exception: {ex}")
    
    # Checking of data
    if merged_df.shape[0] == 0:
        valid_df = False
        msg = """No probe or candidate ids found in job data were located within the source table containing match and non-match pairs. 
        This indicates that the source table needs to be updated or that the probe and gallery ids provided in the job data are not accurate."""
    elif merged_df[c_truth].unique().shape[0] != 2:
        valid_df = False
        msg = """The submitted dataset does not contain both mated and non-mated match pairs. 
                The measurement of matching performance cannot be completed without a valid data 
                set. This data set is not valid. Please submit a data set with genuine matches 
                and non-matches."""
    if not valid_df:
        errors.append(msg)

    col = {
        'pid':c_pid,
        'gid':c_gid,
        'rank':c_rank,
        'score':c_score,
        'truth':c_truth,
        'ppos':c_ppos,
        'gpos':c_gpos,
        'fltr':c_fltr
    }
    if valid_df and len(errors) == 0:
        return merged_df, col, is_identification, []
    else:
        return None , None , None, errors


def get_finger_types(data_df, col, show_types):
    #Filter data on types TODO genralise (not just fingers)
    finger_types = list(data_df[col['fltr']].unique())
    if show_types == '*':
        #this *sorting* assumes that position is just a single number string.
        finger_types_template = ['ALL','Unknown','1','2','3','4','5','6','7','8','9','10']
    else:
        finger_types_template = [x.strip() for x in show_types.split(',')]
    finger_types = [x for x in finger_types_template if x in finger_types]
    return finger_types

def calc_results_main(data_df, col, threshold=2000, gallery_size=10000, fpr_arry=[0.1, 0.05, 0.01, 0.001], is_identification=True, finger_types=[]):
    #Main Analysis
    results = {}
    for ft in finger_types:
        analysis = pxc.Analysis(ft, "Finger")
        tmp_df = data_df[data_df[col['fltr']] == ft]
        analysis.analyse(tmp_df, id_col=col['pid'], rank_col=col['rank'], score_col=col['score'], truth_col=col['truth'], threshold=threshold, gallery_size=gallery_size, fpr_arry=fpr_arry, is_identification=is_identification)
        results[ft] = analysis
    
    return results

def calc_outliers(data_df, col, finger_types):
    #Outliers Analysis
    outliers = {}
    for ft in finger_types:
        tmp_df = data_df[data_df[col['fltr']] == ft]
        outlier_tables = pxc.calc_outliers(tmp_df, col['score'], col['truth'], col['rank'], ft, [])
        outliers[ft] = outlier_tables
    return outliers

def calc_summary(data_df, col, is_identification):
    #Summary Data Analysis
    #candidate length max/min analysis
    can_mets = pxc.candidate_length(data_df, col['pid'], col['rank'], is_identification)
    #calc total matches and non-matches
    count_mets = pxc.counts(data_df, col['pid'], col['truth'])
    # Initial score analysis.
    score_mets = pxc.scores_summary(data_df, col['score'], col['truth'])
    return {**can_mets, **count_mets, **score_mets}


def get_data(truth_data_path, job_data_path, params):
    # params = Params(analysis_path)

    if truth_data_path is not None or truth_data_path=='None':
        data_df, col, is_identification, errors = read_data(truth_data_path, job_data_path, {
                'pid':params.truth_probe_col,
                'gid':params.truth_gallery_col,
                'truth':params.truth_match_col
            }, {
                'pid':params.results_probe_col,
                'gid':params.results_gallery_col,
                'score':params.results_scores_col,
                'rank':params.results_rank_col
            }, params.null_string)
    else:    
        data_df, col, is_identification, errors = read_data_simple(job_data_path, params.null_string)

    if len(errors) > 0:
        print('Could not read and process data')
        return

    finger_types = get_finger_types(data_df, col, params.show_types)

    
    results = calc_results_main(data_df, col, params.threshold, params.gallery_size, params.fpr_arry,is_identification,finger_types)

    

    outliers = calc_outliers(data_df, col, finger_types)

    metrics = calc_summary(data_df, col, is_identification)

    return data_df, col, results, outliers, metrics

def get(reload_data=False):
    doc_params = fetch_vars()
    base_path = os.path.splitext(doc_params['results_file'])[0]
    data_pkl = base_path+'_data_df.pkl'
    results_pkl = base_path+'_results.pkl'
    outliers_pkl = base_path+'_outliers.pkl'
    
    try:
        data_loaded = fetch_var("data_loaded")
    except:
        data_loaded = False

    if not data_loaded or reload_data:
        pfn = doc_params['analysis_file'] if 'analysis_file' in doc_params.keys() else None
        params = Params(fn=pfn, ps_dict=doc_params)
        if not 'truth_file' in doc_params:
            doc_params['truth_file']=None
        data_df, col, results, outliers, metrics = get_data(doc_params['truth_file'], doc_params['results_file'], params)
        data_df.to_pickle(data_pkl)
        pickle.dump(results, open(results_pkl, "wb"))
        pickle.dump(outliers, open(outliers_pkl, "wb"))

        date = datetime.today().strftime('%d %B %Y')
        finger_types = get_finger_types(data_df, col, params.show_types)
        pvars= {"data_type":params.data_type, 
                "test_type":params.test_type, 
                "label":params.label,
                "date":date, 
                "column_names":col,
                "finger_types":finger_types
                }

        for m in ["unique_probes","max_length","min_length","total_matches","total_non_matches","total_nr","min_pos_score","max_neg_score","pos_score_05","pos_score_95","neg_score_05","neg_score_95","nr_pos_eo","nr_neg_eo"]:
            if isinstance(metrics[m], np.float64):
                pvars[m]="%.2f"%metrics[m]
            else:
                pvars[m]=str(metrics[m])

        pvars["data_loaded"] = True
        update_vars(pvars)

        return data_df, results, outliers
    else:
        data_df = pd.read_pickle(data_pkl)
        results = pickle.load(open(results_pkl, "rb"))
        outliers = pickle.load(open(outliers_pkl, "rb"))
        return data_df, results, outliers

