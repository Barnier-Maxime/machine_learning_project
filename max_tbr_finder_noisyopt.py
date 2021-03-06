from geometry_breeder_material import *
from noisyopt import minimizeCompass, minimizeSPSA
import numpy as np 
import json 
import pandas as pd
import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter, Layout

def simulate(material,first_wall):
    results=[]
    bounds=()
    x0=[]

    with open('results/result_noisyopt_'+str(material)+'_'+str(first_wall)+'.json','w') as file_object:
        json.dump([],file_object,indent=2)    

    for number_of_layers in [1,2,3,4]:

        with open('results/result_noisyopt_'+str(material)+'_'+str(first_wall)+'.json') as file_object:
            results = json.load(file_object)

        bounds=bounds+((0,1),)
        print(bounds)
        x0.append(0.5)
        print(x0)
        result = minimizeCompass(find_tbr, bounds=bounds, x0=x0, deltatol=0.01, paired=True, disp=False)
        args=[{'material':material,'first_wall':first_wall}]
        print(result)
        print(1/result.fun)
        json_output = {
                    "max_tbr":1/result.fun,
                    "best_enrichment":list(result.x),
                    "number_of_layers":len(result.x),
                    "breeder_material_name":args[0]['material'],
                    "include_first_wall":args[0]['first_wall']
                    }
        print('json_output',json_output)
        results.append(json_output)

        with open('results/result_noisyopt_'+str(material)+'_'+str(first_wall)+'.json','w') as file_object:
            json.dump(results,file_object,indent=2)

def make_plot(material, first_wall):
    number_of_layers_plot=[]
    max_tbr_plot=[]
    trace =[]
    df = pd.read_json('results/result_noisyopt_'+str(material)+'_'+str(first_wall)+'.json')
    for number_of_layers in [1,2,3,4]:
        
        row_with_number_of_layers = df.loc[df['number_of_layers']==number_of_layers]
        #row_with_max_tbr_number_of_layers = df.loc[row_with_number_of_layers['max_tbr'].idxmax()]

        max_tbr = float(row_with_number_of_layers['max_tbr'])


        # PLOTS RESULTS #
        number_of_layers_plot.append(number_of_layers)
        max_tbr_plot.append(max_tbr)

    trace = Scatter(x=number_of_layers_plot, 
                    y=max_tbr_plot,
                    name='Optimized tbr',
                    mode = 'markers+lines',
                    )
    

    layout = {'title':'Optimized max TBR with non uniform enrichment fraction as a function of the number of layer',
            'xaxis':{'title':'Number of layer'},
            'yaxis':{'title':'Max TBR'},
            }
    print(trace)
    plot({'data':[trace],
        'layout':layout},
        filename='plots/max_tbr_study_opti_'+str(material)+'_'+str(first_wall)+'.html')


if __name__ == "__main__":
    simulate('Li', False)
    make_plot('Li', False)
