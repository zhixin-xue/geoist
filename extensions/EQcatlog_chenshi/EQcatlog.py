﻿# -*- coding: utf-8 -*-
# pass in Python3.6
def run_EQCatlog():
    # part 1 ----------import and set loginfo---------- #  
    import pandas as pd
    import matplotlib.pyplot as plt
    import pathlib
    # output logging 
    import geoist as gi      
    gi.log.setname('Datist_EQCatlog')
    gi.log.info('EQCatlog START')    
    ####--------------End PART ONE--------------####    
    #import shutil  
    #shutil.copy(argfile,  'debug.JSON') #仅在调试时候用    
    # part 2 ----------读取前节点界面参数---------- #
#    CatalogName = data['pars']['CatalogName'] 
#    print('debug: CatalogName//'+str(CatalogName))
    #####--------------End PART TWO--------------####
    ## part 3 ----------设置程序运行参数---------- #
    #Res_flag = data['GetResult'] #Print,JSON
#    Mod_flag = data['DataMode']  #FileList,Url,DataTable
    # parameters for saving data
    tmppath = pathlib.Path(__file__).parent
    path = pathlib.Path(tmppath,'tmpData')
    if not path.exists():
        path.mkdir()    
    file1 = pathlib.Path(tmppath,'tmpData','catalog.csv')
    fileinfo1 = pathlib.Path(tmppath,'tmpData','catsample.csv')
    filedesc1 = pathlib.Path(tmppath,'tmpData','catdesc.csv')
    downfile = pathlib.Path(tmppath,'tmpData','Hash.txt')
    png_file = pathlib.Path(tmppath,'tmpData','eqM-T.png') 
    png_file1 = pathlib.Path(tmppath,'tmpData','eqLocations.png')
    html_file = pathlib.Path(tmppath,'tmpData','tsdata.html')
    #####--------------End PART THREE--------------####
    #
    ## part 4 ----------专业逻辑实现部分---------- #
    # data processing
    from geoist.others import fetch_data
    import requests, os
    #先获得HASH信息从Github到本地
    url = "https://raw.githubusercontent.com/gravity-igpcea/dataset/master/"
    filename = url + 'regHash.txt'
    f = open(downfile,'wb+')    
    with f:
        r = requests.get(filename, stream=True)
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    
    fetch_data.Drepo1.load_registry(downfile)
    cncat = fetch_data.fetch_catalogCN()  #dataframe
    #gemcat = fetch_data.fetch_catalogGME()  #dataframe
    #xccat = fetch_data.fetch_catalog('catalog_xc.TXT')  #dataframe
    #allcat = fetch_data.fetch_catalogGEM()

#    year = cncat["year"].values
#    mon = cncat["month"].values
    cncat.to_csv(file1,sep=';',index=False,encoding="utf-8")
    catinfo = pd.concat([cncat.head(),cncat.tail()])    
    catinfo.to_csv(fileinfo1,sep=';',index=True,encoding="utf-8")
    catdesc = cncat.describe()
    catdesc.to_csv(filedesc1,sep=';',index=True,encoding="utf-8")
#    print(cncat.dtypes)
#    print(cncat.head())
#    print(cncat.tail())
#    print(cncat.info())
#    print(cncat.describe())
    
#    data=pd.read_csv(pathlib.Path(orig_file),parse_dates=True,delimiter=";",index_col=[0],na_values=na_values)
#    data['origin_data'] = data[data.columns[0]].interpolate()  
#    res = tsa.adfuller(data['origin_data'].values)
#    res1 = tsa.acorr_ljungbox(data['origin_data'] ,lags = 1)
#    with open(pathlib.Path(res_file),'w') as f:
#        print('ADF and White noise tests for time series signal: {}'.format('original data'),file=f)
#        tsa.print_adf(res,'original data',file=f)
#        print(' ',file=f)
#        print('White noise test for {}:'.format('original data'),file=f)
#        print(' ' * 2 + 'test statistic: {}'.format(res1[0]),file=f)
#        print(' ' * 2 + 'p-value: {}'.format(res1[1]),file=f)    
#    
#    tsa.plot_acf(data['origin_data']).savefig(str(png_file1),format='png') 
#    data['mean_data'] = data['origin_data'].rolling(window=window_size).mean()
#    data['std_data'] = data['origin_data'].rolling(window=window_size).std()
#    data.plot(figsize=(15,12),y=['origin_data','mean_data','std_data'])
#
#    gi.log.info('windowsize = ' + str(window_size))
#    gi.log.info('data length = ' + str(len(data['origin_data'])))
#    # output html
#    if Mod_flag == 'Url':
#        import bokeh.plotting as bp
#        from bokeh.palettes import Spectral4
#        from bokeh.models import ColumnDataSource    
#        p = bp.figure(title="The preliminary result by windowsize = "+str(window_size)
#                     , plot_width=535, plot_height=350, x_axis_type="datetime")
#        bp.output_file(html_file, mode = 'inline')
#        source = ColumnDataSource(data)
#        
#        for data, name, color in zip([source.column_names[1], source.column_names[2], source.column_names[3]], ["ORI", "mean", "std"], Spectral4):
#           p.line(source.column_names[0], data, source=source,color=color, alpha=0.8, legend=name)
#        p.xaxis.axis_label = 'Date'
#        p.yaxis.axis_label = 'Value'
#        p.legend.location = "top_left"
#        p.legend.click_policy="hide"	
#        bp.save(p)
#        print(str(html_file)) #输出网络地址
#        gi.log.info('output html finished')
#     #output static pic
#    if Mod_flag == 'FileList':
#        SMALL_SIZE = 12
#        MEDIUM_SIZE = 15
#        BIGGER_SIZE = 18
#        plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
#        plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
#        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
#        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
#        plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
#        plt.rc('legend', fontsize=MEDIUM_SIZE,loc='upper left')    # legend fontsize
#        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title        
#        ax = data.plot(figsize=(15,12),y=[data.columns[0],'mean_data','std_data'])
#        ax.set_xlabel('Date')
#        ax.set_ylabel('Value')
#        plt.grid()
#        plt.legend()
#        plt.title("The preliminary result by windowsize={}".format(window_size),loc='left')
#        plt.savefig(str(png_file),format='png') 
#        gi.log.info('output png file finished')
#        print(png_file) #输出一个图片
#    #####--------------End PART FOUR--------------####
#    #
#    ## part 5 ------------输出数据------------------ #
#    print(res_file) #输出数据表格文件zai 
#    #####--------------End PART FIVE--------------####

if __name__ == '__main__':
    print('debug: starting//EQCatlog.py by chenshi')    
#    import sys, json
#    argfile=sys.argv[1] #json参数  
#    print('debug: open//'+argfile) 
#    with open(argfile,'rb') as f:
#        data = json.load(f)    
    run_EQCatlog()  #业务实现
    print('debug: EQCatlog is finished.')


