from dash import Dash, dcc, Output, Input, html
import plotly.express as px
import pandas as pd 
import dash_bootstrap_components as dbc    
import numpy as np  
             
df = pd.read_csv('preprocessed_data.csv',index_col=0)
df_geo = pd.read_csv('preprocessed_geo.csv')
top10_kota = pd.read_csv('top10_kota.csv')
top10_provinsi = pd.read_csv('top10_provinsi.csv')


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

mytitle = dcc.Markdown("Indonesia Earthquake Dashboard")
subtitle = "The Indonesia earthquake dashboard is an interactive web application that provides information about earthquakes history that occur in Indonesia. The dashboard uses data to display the location, magnitude, and time it occur. Users can filter the earthquakes by time, and view additional details about each earthquake by hover to the plot. The dashboard also includes a summary of the most recent earthquakes and a graph of earthquake frequency over time. The goal of the dashboard is to help people stay informed about earthquake activity in Indonesia and take necessary precautions to stay safe."
mygraph1 = dcc.Graph(figure={})
mygraph2 = dcc.Graph(figure={})
mygraph3 = dcc.Graph(figure={})
mygraph4 = dcc.Graph(figure={})
mygraph5 = dcc.Graph(figure={})
mygraph6 = dcc.Graph(figure={})
options=[{"label": str(year), "value": year} for year in df["year"].unique()]
options.append({"label": "All", "value": 0})
dropdown = dcc.Dropdown(options=options,
                        value=0,  # initial value displayed when page first loads
                        clearable=False,style= {'color': 'black'})
dropdown1 = dcc.Dropdown(options=[{'label': 'Province', 'value': 1},
                                  {'label': 'City', 'value': 2}],
                        value=1,  # initial value displayed when page first loads
                        clearable=False,style= {'color': 'black'})
dropdown2 = dcc.Dropdown(options=[{'label': 'Year', 'value': 1},
                                  {'label': 'Month', 'value': 2}],
                        value=1,  # initial value displayed when page first loads
                        clearable=False,style= {'color': 'black'})

app.layout = dbc.Container([
       html.H1(mytitle, style={'text-align': 'center', 'color': 'white', 'font-weight': 'bold'}),
        
        dbc.Row(html.H4(subtitle),style={'text-align': 'center','font-weight': 'bold'}) , 
        
        dbc.Row([
            dbc.Col([
                html.Label("Select Year"),
                dbc.Col([dropdown])
            ]),
            dbc.Col([
                html.Label("Select Province / City"),
                dbc.Col([dropdown1])
            ]),
            dbc.Col([
                html.Label("Select Year / Month"),
                dbc.Col([dropdown2])
            ]),
        ]) ,
        html.Br(),
        
        # html.H6(subtitle),

        # html.Label("Select Year"),
        # dbc.Row([
        #         dbc.Col([dropdown], width=2)
        # ], justify="left"),
        
        # html.Label("Select Province / City"),
        # dbc.Row([
        #         dbc.Col([dropdown1], width=2)
        # ], justify="left"),
        
        # html.Label("Select Year / Month"),
        # dbc.Row([
        #         dbc.Col([dropdown2], width=2)
        # ], justify="left"),

        dbc.Row([
                dbc.Col([mygraph5], width=4,  style={"height": "100%"}),
                dbc.Col([mygraph1], width=8,  style={"height": "100%", "display": "flex", "justify-content": "flex-end"})
        ], className="g-0",),

        dbc.Row([
                dbc.Col([mygraph3], width=3,  style={"height": "20%"}),
                dbc.Col([mygraph4], width=6,  style={"height": "20%"}),
                dbc.Col([mygraph2], width=3,  style={"height": "20%"}),         
        ], className="g-0"),
        
        ], fluid=True,
    style={ 'height': '100vh','width': '100%',
    'margin': 0})

# -------- Callback ---------
@app.callback(
        Output(mygraph1, "figure"),
        Output(mygraph2, "figure"),
        Output(mygraph3, "figure"),
        Output(mygraph5, "figure"),
        Output(mygraph4, "figure"),
        Input(dropdown, "value"),
        Input(dropdown1, "value"),
        Input(dropdown2, "value")
)
def update_dashboard(selected_year,region,time):
    dff = df.copy()
    dff_geo = df_geo.copy()
    if(selected_year!=0):
        dff = dff[dff["year"]==selected_year]
        dff_geo = dff_geo[dff_geo["year"]==selected_year]
    

    # map_fig, bar_fig, line_fig, pie_fig = create_figures(dff)

    def earthquake_month(df):
        #order = ['January', 'February', 'March', 'April', 'May', 'June',
        #        'July', 'August', 'September', 'October', 'November', 'December']
        vfunc = np.vectorize(lambda x: pd.to_datetime(str(x), format='%m').strftime('%B'))
        order = vfunc(np.sort(df['month'].unique()))
        group = df.groupby('month_name').agg({'magnitude':['count','mean'],'depth':'mean'})
        group.columns = group.columns.map(lambda x: ' '.join(x))
        sorted_group = group.loc[order]
        sorted_group.reset_index(inplace=True)
        month_fig = px.bar(data_frame=sorted_group.round(2),x='month_name',y='magnitude count',
                    title='Earthquake Frequency by Month',color_discrete_sequence=['rgb(178, 34, 34)'],
                    hover_data={'month_name':False,'magnitude count':True,'magnitude mean':True,'depth mean':True},hover_name='month_name',
                    template='plotly_dark')
        # add a line plot
        month_fig.add_trace(px.line(data_frame=sorted_group.round(2), x='month_name', y='magnitude count',
                            color_discrete_sequence=['#1f77b4']).update_traces(line=dict(width=3)).data[0])
        month_fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
        month_fig.update_xaxes(title_text="Count")
        month_fig.update_yaxes(title_text="Month")
        return month_fig

    def earthquake_year(df):
        group = df.groupby('year').agg({'magnitude':['count','mean'],'depth':'mean'})
        group.columns = group.columns.map(lambda x: ' '.join(x))
        group.reset_index(inplace=True)
        # create the bar chart
        year_fig = px.bar(data_frame=group.round(2), x='year', y='magnitude count',
                    title='Earthquake Frequency by Year',color_discrete_sequence=['rgb(178, 34, 34)'],
                    hover_data={'year':False,'magnitude count':True,'magnitude mean':True,'depth mean':True}, hover_name='year',
                    template='plotly_dark')

        # add a line plot
        year_fig.add_trace(px.line(data_frame=group.round(2), x='year', y='magnitude count',
                            color_discrete_sequence=['#1f77b4']).update_traces(line=dict(width=3)).data[0])

        # update the layout
        year_fig.update_layout(title='Earthquake Frequency by Year',
                        xaxis_title='Year', yaxis_title='Magnitude Count',plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
        year_fig.update_yaxes(title_text="Count")
        return year_fig

    def earthquake_class(df):
        def earthquake_classification(mag):
            if mag == "Micro":
                mag_class = 1
            elif mag == "Minor":
                mag_class = 2
            elif mag <= "Light":
                mag_class = 3
            elif mag <= "Moderate":
                mag_class = 4
            else:
                mag_class = 5
            return mag_class
        def earthquake_classification_reverse(mag):
            if mag == 1:
                mag_class = "Micro"
            elif mag == 2:
                mag_class = "Minor"
            elif mag == 3:
                mag_class = "Light"
            elif mag == 4:
                mag_class = "Moderate"
            else:
                mag_class = "Strong"
            return mag_class
        vfunc = np.vectorize(earthquake_classification)
        vfunc_reverse = np.vectorize(earthquake_classification_reverse)
        order =vfunc_reverse(np.sort(vfunc(df['class'].unique())))
        #order = ['Micro','Minor','Light','Moderate','Strong']
        group = df.groupby('class').agg({'magnitude':['count','mean'],'depth':'mean'})
        group.columns = group.columns.map(lambda x: ' '.join(x))
        #group.reset_index(inplace=True)
        sorted_group = group.loc[order]
        sorted_group.reset_index(inplace=True)
        class_fig = px.bar(data_frame=sorted_group.round(2),x='class',y='magnitude count',
                    title='Earthquake Frequency by Class',color_discrete_sequence=['rgb(178, 34, 34)'],
                    hover_data={'class':False,'magnitude count':True,'magnitude mean':True,'depth mean':True},hover_name='class'
                    ,template='plotly_dark')
        class_fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
        class_fig.update_yaxes(title_text="Count")

        return class_fig

    def create_density_map(dataframe):
        # Define hover data
        hover_data = {
            'date': True, 'magnitude': True, 'provinsi': True,
            'longitude': False, 'latitude': False
        }
        
        # Create density map figure
        map_fig = px.density_mapbox(
            dataframe, lat='latitude', lon='longitude',
            z='magnitude', radius=2, center=dict(lat=-2.5, lon=118),
            zoom=3.8, hover_name='id',
            hover_data=hover_data, color_continuous_scale='Hot',
            mapbox_style='carto-darkmatter', template='plotly_dark'
        )
        
        # Update figure layout
        map_fig.update_layout(
            width=1680, height=575,
            margin=dict(r=1, t=1, l=1, b=1), plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)'
        )
        
        # Update colorbar location and orientation
        map_fig.update_coloraxes(
            showscale=True,
            colorbar=dict(
                len=0.3, yanchor='bottom', y=0,
                xanchor='center',
                thickness=10, title='Earthquake Magnitude',
                orientation='h', title_side="top")
        )
        
        return map_fig
    
    def top10_provinsi_plot(data_plot):
        earthquake_provinsi = data_plot.groupby('provinsi')['id'].count()
        top10_provinsi = earthquake_provinsi.drop('Sea').sort_values(ascending=False).head(10)
        top10_provinsi = pd.DataFrame(top10_provinsi.reset_index())
        top10_provinsi.rename({'id':'count'},axis=1,inplace=True)
        provinsi_fig = px.bar(data_frame=top10_provinsi,y='provinsi',x='count',color_discrete_sequence=['rgb(178, 34, 34)'],
                    title='Earthquake Frequency by Province',hover_data={'provinsi':False},hover_name='provinsi',template='plotly_dark',orientation='h')
        provinsi_fig.update_layout(
            height=575, plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)'
        )
        provinsi_fig.update_yaxes(autorange='reversed')
        return provinsi_fig
    
    def top10_kota_plot(data_plot):
        earthquake_kota = data_plot.groupby('id')['provinsi'].count()
        top10_kota = earthquake_kota.drop('Sea').sort_values(ascending=False).head(10)
        top10_kota = pd.DataFrame(top10_kota.reset_index())
        top10_kota.rename({'id':'kota','provinsi':'count'},axis=1,inplace=True)
        kota_fig = px.bar(data_frame=top10_kota,y='kota',x='count',color_discrete_sequence=['rgb(178, 34, 34)'],
                    title='Earthquake Frequency by City',hover_data={'kota':False},hover_name='kota',template='plotly_dark',orientation='h')
        kota_fig.update_layout(
            height=575, plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)'
        )
        kota_fig.update_yaxes(autorange='reversed')
        return kota_fig
    
    def earthquake_line(df):
        df.index =pd.to_datetime(df.index)
        group = df.groupby(level=0).agg({'magnitude':['count','mean'],'depth':'mean'})
        group.columns = group.columns.map(lambda x: ' '.join(x))
        group.reset_index(inplace=True)

        # Create the basic line chart
        group['date'] = group['date'].dt.date
        date_buttons = [
        {'count': 14, 'label': "All", 'step': "year", 'stepmode': "todate"},
        {'count': 12, 'label': "YTD", 'step': "month", 'stepmode': "todate"},
        {'count': 6, 'label': "6M", 'step': "month", 'stepmode': "todate"}]

        fig = px.line(data_frame=group.round(2),x='date', y='magnitude count', 
                    title="Earthquake Frequency",color_discrete_sequence=['rgb(178, 34, 34)'],
                    hover_data={'date':False,'magnitude count':True,'magnitude mean':True,'depth mean':True},hover_name='date',template='plotly_dark')
        fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
        fig.update_layout(
            {'xaxis':
            {'rangeselector': {'buttons': date_buttons, 'font': {'color': 'black'}}}})
        return fig
    
    def create_figures(dff,dff_geo,region,time):
        map_fig = create_density_map(dff_geo)
        class_fig = earthquake_class(dff)
        if(time==1):
            time_fig = earthquake_year(dff)
        else:
            time_fig = earthquake_month(dff)
        if(region==1):
            region_fig = top10_provinsi_plot(dff_geo)
        else:
            region_fig = top10_kota_plot(dff_geo)
        line_fig = earthquake_line(dff)
        return map_fig, class_fig, time_fig,region_fig,line_fig


    # Create and update the figures based on the selected year
    map_fig, class_fig, time_fig,line_fig,region_fig = create_figures(dff,dff_geo,region,time)

    return  map_fig, class_fig, time_fig,line_fig,region_fig

# -------- Run app ---------
if __name__ == '__main__':
    app.run_server(debug=True, port=8054)
    
    