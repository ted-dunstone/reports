# Load the support variables
import re
import contextlib
import statistics
import collections.abc
import pickle
import os.path

from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

import yaml
import jinja2

import pandas as pd
import seaborn as sns

from px_build_doc.util import TrendsManager, FigureManager
from px_build_doc.util import FigureManager, TableManager, fetch_var, display

## Util Functions
def raise_error(error_str):
  raise ValueError("\n\n"+str(error_str))

def deep_update(d,u):
    """
    Update a nested dictionary or similar mapping.
    """
    for k, v in u.items():
        if isinstance(d, collections.abc.Mapping):
            if isinstance(v, collections.abc.Mapping):
                r = deep_update(d.get(k, {}), v)
                d[k] = r
            else:
                d[k] = u[k]
        else:
            d = {k: u[k]}
    return d

## Report Functions

class ReportProcess():

  global_data_dict = {} # the data dictionary - holds all ddefined data variables
  observation = {}
  
  def __init__(self,filename):
    sns.set()
    with open(filename) as f:
      sns.set(style="ticks", palette="pastel")

      self.bps=self.load_yaml(f.read())
      self.tables = TableManager(format=self.doc_format) 
      self.figs = FigureManager(format=self.doc_format)

      try:
        # build the reports
        self.bp = self.bps[0]
        self.load_data(self.bp)
        if len(self.bps)>0:
          for bp in self.bps[1:]:
            self.create_md_doc(bp)
 
      except Exception: #or AssertionError
        import traceback
        traceback.print_exc(limit=10)


  def load_yaml(self,yaml_str):
    """ Load the blue print, if variables are defined substitute them
    Note that the variables must be defined as an array """

    def get_variables_dict(yaml_str):
      """ get the defined variables """

      # Can't read enitre yaml as jinja2 may cause invalid yaml
      variables_str=""
      for line in yaml_str.splitlines():
        if line.startswith('variables'):
            variables_str+=line+"\n"
        elif len(variables_str)>0:
            variables_str+=line+"\n"
            if len(line.strip())==0:
              break
      if len(variables_str)==0:
        # no variables defined
        return {}

      blueprint = yaml.load(variables_str,Loader=yaml.Loader)

      if 'variables' in blueprint:
        # resubstitute vairables 
        var_dict={}
        for var_list in blueprint['variables']:
          for key,val in var_list.items():
            if type(val)==type(""):
              val=val.format(**var_dict)
            #if type(val)==type({}):
            #  if len(val)==1:
            #    val=var_dict[list(val)[0]]
                
            var_dict[key]=val
      return var_dict



    def update_yaml(yaml_str,var_dict={}):      
      template = jinja2.Template(yaml_str)
      yaml_str = template.render(**var_dict)
      #open('temp.yaml','w').write(yaml_str)
      blueprints = yaml.load_all(yaml_str,Loader=yaml.Loader)
      return list(blueprints)

    var_dict = get_variables_dict(yaml_str)
    
    blueprints = update_yaml(yaml_str,var_dict)

    #  call import yamls
    imported = {}
    setup_bp = blueprints[0]
    if 'import' in setup_bp:
      for filename in setup_bp['import']:
          with open(filename+'.yaml') as f:
            imported = list(yaml.load_all(f.read(),Loader=yaml.Loader))[0]
            setup_bp = deep_update(imported,setup_bp)

    #raise_error(list(setup_bp['analysis']))
    
    self.doc_meta = self.get_doc_meta(setup_bp,defaults={'output_type':'md','test':'test'})
    self.doc_format = self.doc_meta['output_type']
    
    blueprints[0] = setup_bp
    
    return blueprints

  def get_doc_meta(self,blueprint,defaults):
    """ Get the document meta data where available"""

    newdict=defaults.copy()
    if 'doc_meta' in blueprint:
      newdict = deep_update(newdict,blueprint['doc_meta'])
    return newdict


  # turn dict into object
  def to_obj(self,indict,key=False,defaults={}):
    if key:
      indict = indict[key] if key is indict else {}
    return type('from_dict', (object,), deep_update(defaults,indict))

  def do_query(self,query_str):
    return pd.read_sql_query(query_str, self.conn)

  def load_data(self,bp):
    """ 
    Load all the data from various sources 
    cache results in "global_data.sav" """

    import sqlite3
    
    self.conn = sqlite3.connect("pxdata")

    cache_data_file = 'global_data.sav'
    if os.path.exists(cache_data_file):
      with open(cache_data_file,'rb') as f:
        self.global_data_dict=pickle.load(f)

    # build query dicitionary
    #raise_error(list(bp['data'].keys()))
    for key,val in bp['data'].items():
        data_query = self.to_obj(val,defaults={'enabled':True,"query":"",'fields':False,'table':False})
        if data_query.enabled:
          if data_query.fields:
            data_query.table = " from "+data_query.table if data_query.table else ''
            data_query.query = "select "+data_query.fields + data_query.table +" "+ data_query.query
          # if cached and the query is the same then just use cache
          if key in self.global_data_dict and self.global_data_dict['_q_'+key]==data_query.query:
            continue

          df = self.do_query(data_query.query) if data_query.query else None

          self.global_data_dict[key]=df
          self.global_data_dict['_q_'+key]=data_query.query

    with open(cache_data_file,'wb') as f:
      pickle.dump(self.global_data_dict,f)


  def format_caption(self,obj):
    return obj.caption


  def handle_plot(self,figs,analysis):
    """ Create a plot figure diagram using pyplot, pandas or seaborn syntax
    
    usage
    ```yaml
    py: |
      [python code]
    plot:
    - caption: the caption for the table
    - height: the height of the figure
    ```
    """
    import matplotlib.pyplot as plt
    if analysis.plot:
      plot_obj=self.to_obj(analysis.plot,defaults={}) #defaults={"labels":False,"caption":False,"height":5,"format":self.doc_format})
      #raise_error(str(analysis.plot)+str(plot_obj.height))

      if plot_obj.labels:
          labs=[l.strip() for l in plot_obj.labels.split(',')] #pylint: disable=no-member
          if len(labs)>0:
            plt.xlabel(labs[0])
          if len(labs)>1:
            plt.ylabel(labs[1])
      if plot_obj.caption:
        figs.save_plot(self.format_caption(plot_obj),height=plot_obj.height,format=plot_obj.format).display()
  
  def handle_table(self,tables,analysis):
    """ Create a table when specified in the analysis
    
    usage
    ```yaml
    py: |
      [python code]
    table:
    - variable (the dataframe to use)
    - caption: the caption for the table
    - height: the height of the figure
   ```
    """
    
    if analysis.table:
      table_obj=self.to_obj(analysis.table,defaults={})
      if table_obj.variable:
        tables.read_df(globals()[table_obj.variable]).display(self.format_caption(table_obj),floatfmt=table_obj.floatfmt)

  def handle_uml(self,figs,analysis):
    """ Create a uml diagram using plantuml
    
    usage
    ```yaml
    uml: |
      @startuml ....
    plot:
    - caption: the caption for the table
    - height: the height of the figure
    ```
    """
    if analysis.plot and analysis.uml:
      uml_obj=self.to_obj(analysis.plot,defaults={}) #"variable":False,"caption":"","height":8})
      if analysis.plot:
        figs.set_uml("uml",self.format_caption(uml_obj),height=uml_obj.height,uml=analysis.uml).display()
  

  def analysis_func(self,analysis_name,func_params=None):
    """ Process the analysis function name """

    tables = self.tables # define vars avaliable to any analysis function
    figs = self.figs

    def get_data(source_name):
      """ return the data from a query"""

      if not source_name in self.global_data_dict:
        raise_error("Error data source %s is not definied."%analysis.use_data)
      return self.global_data_dict[source_name]

    def split_params(name):
      """ split function and parameters
      match func(a,b,c..):use_data 
      
      a function can be called as so:
      ```yaml
      - an: pie_test(24):stats_fingers
      ```
      """

      regex = r"(.*)\((.*)\)(:.*)*"
      matches = re.search(regex, name)
      func_params = ""
      use_data = None
      if matches:
        name = matches.group(1)
        func_params = matches.group(2)
        use_data = matches.group(3)
        if use_data is not None:
          use_data=use_data[1:] # strip first char as its a :
      return name,func_params, use_data

    
    def run_function(var_params_dict,analysis_code,analysis_name,df):
      """ run the analysis function in the current context"""

      # note df provdied as local to analysis function
      tables = self.tables
      figs = self.figs
      get_df = get_data
      def set_observation(key,info):
        if not key in self.observation:
          self.observation[key]=[]
        self.observation[key].append(info)

      observations = self.observation


      _local = locals().copy()
      _local = deep_update(_local,var_params_dict)
    
      if type(analysis.params)==type([]):
        for param in analysis.params:
          if param not in _local:
            p_var=param.split('=')
            if len(p_var)==1:
              _local[param] = None
            else:
              _local[p_var[0]] = p_var[1]
      
      #_local.update(var_params_dict)
      ccmpiled = compile(analysis_code,'py_vars', 'exec')
      try:
        exec(ccmpiled,globals(),_local)
      except:
        raise_error("Syntax error excuting function [%s]"%analysis_name)


    analysis_name,func_params_str,use_data = split_params(analysis_name)
    defaults={'enabled':False,"use_data":False,'table':False,"before":'',"after":'',
                "uml":False,"py":False,"after_py":False,"params":False,
                "plot":{"labels":False,"caption":False,"height":7,"format":self.doc_format},
                "table":{"variable":False,"caption":"","height":8,"floatfmt":()}}
    
    analysis_dict = self.bp['analysis'][analysis_name]
    if func_params is not None:
      #analysis_dict.update(func_params)
      analysis_dict = deep_update(analysis_dict,func_params)
    else:
      func_params={}
   
    analysis = self.to_obj(analysis_dict,defaults = defaults)

    if use_data is not None and 'use_data' not in func_params: # data is specified excplicitly in the function call
        analysis.use_data = use_data

    if analysis.use_data:
        df=get_data(analysis.use_data)
    else:
        df=None
    
    display("\n"+analysis.before+"\n")
    
    if analysis.py:
      run_function(func_params,analysis.py,analysis_name,df)
      #raise_error(str(analysis.plot))
      self.handle_plot(figs,analysis)
      self.handle_table(tables,analysis)

    if analysis.after_py:
      run_function(func_params,analysis.after_py,analysis_name,df)
      #raise_error(str(analysis.plot))
       
  
    self.handle_uml(figs,analysis)    
    
    display("\n"+analysis.after+"\n")
    
  def create_md_doc(self, blueprint):
    """ Build the doc from a blueprint dict """

    # allow definition of local doc params
    doc_meta = self.get_doc_meta(blueprint,defaults=self.doc_meta)
    for doc_name,doc_def in blueprint.items():
      if not doc_name == 'doc_meta': 
        with open(doc_name+'.md','w') as f:
         #with contextlib.redirect_stdout(f):
            print("---")
            print(yaml.dump(doc_meta))
            print("---")
            self.build_md_doc(doc_def)

    # save config yaml
    #with open(doc_name+'.yaml', 'w') as file:
    #    yaml.dump(doc_meta, file)


  def build_md_doc(self, item_list, level=1):
    """ Recursively builds a markdown document from a dict
    
    Rules are:
    * If value is a string treat as markdown
    * If a key:
     * contains a () then it is an analysis, params are in the dict
     * **file**: load markdown file
    """
    #raise_error(str(item_list))
    for item_num, result in enumerate(item_list):
      for key,val in result.items():
        
      #  if key =='doc_meta': # allow definition of local doc params
      #      self.doc_meta.update(val)
      #      continue

        display('#'*level+f" {key}")
        for cmds in val:
          if type(cmds)==type(""):
            cmds={'md':cmds}
          if type(cmds)==type({}):  
            for key1,val1 in cmds.items():
              if key1.find('()')!=-1:
                  self.analysis_func(key1,val1)
              if key1=='md':
                  display("\n"+val1+'\n')
              elif key1=='py':
                  ccmpiled = compile(val1,'py_vars', 'exec')
                  exec(ccmpiled,globals(),locals())   
              elif key1=='an':
                  self.analysis_func(val1)
              elif key1=='file':
                  with open(val1) as f:
                    display("\n"+f.read()+'\n')
              
              if type(val1) == type([]):
                # recursive call for lower heading levels
                self.build_md_doc([cmds],level+1)


ReportProcess('analysis.yaml')