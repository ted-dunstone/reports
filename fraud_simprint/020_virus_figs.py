# Load the support variables
from px_build_doc.util import TrendsManager, FigureManager
import statistics
import pandas as pd
import seaborn as sns
import yaml
from px_build_doc.util import FigureManager, TableManager, fetch_var, display
import jinja2
import re


def raise_error(error_str):
  raise ValueError("\n\n"+error_str)

class ReportProcess():

  global_data_dict = {} # the data dictionary - holds all ddefined data variables


  def __init__(self,filename):
    
    with open(filename) as f:
      sns.set(style="ticks", palette="pastel")

      self.bp=self.load_yaml(f.read())

      self.tables = TableManager(format=self.meta.output_type) 
      self.figs = FigureManager(format=self.meta.output_type)

      try:
        self.load_data(self.bp)
        self.build_report(self.bp['report'])
#        self.run_analysis(bp)
      except Exception: #or AssertionError
        import traceback
        traceback.print_exc(limit=10)


  def load_yaml(self,yaml_str):
    """ Load the blue print, if variables are defined substitute them
    Note that the variables must be defined as an array """
    variables_str=""
    for line in yaml_str.splitlines():
      if line.startswith('variables'):
          variables_str+=line+"\n"
      elif len(variables_str)>0:
          variables_str+=line+"\n"
          if len(line.strip())==0:
            break
    blueprint = yaml.load(variables_str,Loader=yaml.Loader)
    # allow varibale definitiions
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
        
        template = jinja2.Template(yaml_str)
        yaml_str = template.render(**var_dict)

        blueprint = yaml.load(yaml_str,Loader=yaml.Loader)

    self.meta = self.to_obj(blueprint,key='meta',defaults={'output_type':'md'})
    return blueprint

  # turn dict into object
  def to_obj(self,indict,key=False,defaults={}):
    #print(indict)
    if key:
      indict = indict[key] if key is indict else {}
    defaults.update(indict)
    #print(defaults)
    return type('from_dict', (object,), defaults)

  def load_data(self,bp):
    """ Load all the data from various sources """

    import sqlite3
    
    conn = sqlite3.connect("pxdata")

    # build query dicitionary
    for result in bp['data']:
      for key,val in result.items():
          data_query = self.to_obj(val,defaults={'enabled':True,"query":False,'fields':False,'table':False})
          if data_query.enabled:
            if data_query.fields:
              data_query.table = " from "+data_query.table if data_query.table else ''
              data_query.query = "select "+data_query.fields + data_query.table +" "+ data_query.query
            df = pd.read_sql_query(data_query.query, conn) if data_query.query else None
            self.global_data_dict[key]=df

  def run_analysis(self,bp):
    """ Run analysis on the loaded data """
    tables = self.tables
    figs = self.figs
    
    for result in bp['analysis']:
      for key,val in result.items():
          #pylint: disable=no-member
          analysis = self.to_obj(val,defaults={'enabled':False,"use_data":False,'table':False,"before":'',"after":''})
          if analysis.enabled:
            if analysis.use_data:
                df=self.global_data_dict[analysis.use_data]

          display("\n"+analysis.before+"\n")
          if analysis.plot: 
            ccmpiled = compile(analysis.plot,'py_vars', 'exec')
            exec(ccmpiled,globals(),locals())
          if analysis.table:
            tables.read_df(globals()[analysis.table['variable']]).display(analysis.table['caption']) #pylint: disable=unsubscriptable-object
          
          display("\n"+analysis.after+"\n")

  def format_caption(self,obj):

    #if self.local_caption: 
    #  return self.local_caption
    #else:
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
    #raise_error(str(analysis.plot))
    if analysis.plot:
      plot_obj=self.to_obj(analysis.plot,defaults={"labels":False,"caption":False,"height":8})

      if plot_obj.labels:
          labs=[l.strip() for l in plot_obj.labels.split(',')] #pylint: disable=no-member
          if len(labs)>0:
            plt.xlabel(labs[0])
          if len(labs)>1:
            plt.ylabel(labs[1])
      if plot_obj.caption:
        figs.save_plot(self.format_caption(plot_obj),height=plot_obj.height).display()
  
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
      table_obj=self.to_obj(analysis.table,defaults={"variable":False,"caption":"","height":8})
      if table_obj.variable:
        tables.read_df(globals()[table_obj.variable]).display(self.format_caption(table_obj))

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
      uml_obj=self.to_obj(analysis.plot,defaults={"variable":False,"caption":"","height":8})
      if analysis.plot:
        figs.set_uml("wbs",self.format_caption(uml_obj),height=uml_obj.height,uml=analysis.uml).display()

  def analysis_func(self,analysis_name,func_params=None):
    """ Process the analysis function name """

    tables = self.tables # define vars avaliable to any anlysis function
    figs = self.figs
    self.local_caption = None

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

    def str_to_dict(instr):
      """ take a string with named parameters and convert it to a python dictionary """
      if len(instr.strip())==0:
        return {}
      param_split = lambda instr,fld_no: [s.split('=')[fld_no].strip() for s in instr.split(',')]
      dict_str='{%s}'%','.join([f"'{key.replace('.','_')}':{val}" for key,val in zip(param_split(instr,0),param_split(instr,1))])
      return eval(dict_str)
    
    def set_func_params(func_name,func_params_str):
      """ build a dict for the analysis variablies handel both one line str and dict form"""
      param_split = lambda instr: [s.strip() for s in instr.split(',')]

      func_params_def_vars = param_split(func_params_str)
         
      func_var_dict = str_to_dict(func_params_str)
      if analysis.params:
        required_params = param_split(analysis.params)
        params_in=[a for a in func_params_def_vars if not a.startswith('_')]
        #if len(required_params)!=len(params_in):
        #  raise_error("Number of parameters (%s,%s) wrong for function [%s]"%(str(required_params),str(params_in),func_name))

      options={}
      for key,val in func_var_dict.items():
        if key.startswith('_'):
          var_names = key.split('_')
          if len(var_names)==3:
            if var_names[1] not in options:
                options[var_names[1]]={}
            options[var_names[1]].update({var_names[2]:val})
      #if len(options)>0:
      #  self.rasie_error(str(options))

      if '_plot_caption' in func_var_dict:
            self.local_caption=func_var_dict['_plot_caption']

      return func_var_dict

    def run_function(var_params_dict,analysis,analysis_name,df):
      """ run the analysis function in the current context"""

      # note df provdied as local to analysis function

      _local = locals().copy()
      _local.update(var_params_dict)
      ccmpiled = compile(analysis.py,'py_vars', 'exec')
      try:
        exec(ccmpiled,globals(),_local)
      except:
        raise_error("Syntax error excuting function [%s]"%analysis_name)


    analysis_name,func_params_str,use_data = split_params(analysis_name)
    defaults={'enabled':False,"use_data":False,'table':False,"before":'',"after":'',"uml":False,"py":False,"params":False}
    
    analysis_dict = self.bp['analysis'][analysis_name]
    if func_params is not None:
      analysis_dict.update(func_params)
    else:
      func_params={}
   
    analysis = self.to_obj(analysis_dict,defaults = defaults)

    if use_data is not None and 'use_data' not in func_params: # data is specified excplicitly in the function call
        analysis.use_data = use_data

    if analysis.use_data:
        if analysis.use_data in self.global_data_dict:
          df=self.global_data_dict[analysis.use_data]
        else:
          raise_error("Error data source %s is not definied.")

    #func_var_dict = set_func_params(analysis_name,func_params_str)
    #func_var_dict.update(func_params)

    display("\n"+analysis.before+"\n")
    
    if analysis.py:
      run_function(func_params,analysis,analysis_name,df)
      #raise_error(analysis_name+':'+str(func_params)+str(analysis.plot))
      self.handle_plot(figs,analysis)
      self.handle_table(tables,analysis)
  
    self.handle_uml(figs,analysis)    
    
    display("\n"+analysis.after+"\n")
    

  def build_report(self, item_list, level=1):
    for result in item_list:
      for key,val in result.items():
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
                # recursive call
                #display('#'*(level+1)+f" {key1}")
                self.build_report([cmds],level+1)


ReportProcess('analysis.yaml')