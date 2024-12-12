import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


spacex_df = pd.read_csv('spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
sites = spacex_df['Launch Site'].unique()
sites_labels= [{'label':site, 'value':site} for site in sites]
sites_labels.append({'label':'All sites', 'value':"ALL"})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id='site-dropdown',options=sites_labels, value='ALL', placeholder='Select a Launch Site here', searchable=True),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000, marks={str(i):i for i in range(0,10001,int(10000/4))}, value=[min_payload, max_payload]),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def update_pie_chart(site):
    filtered_df = spacex_df
    if site != 'ALL':
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]
        count = filtered_df['class'].value_counts().to_frame().reset_index()
        fig = px.pie(count, values="count", names="class", title=f"Success rate for site {site}")
    else:
        fig = px.pie(filtered_df, values="class", names="Launch Site", title="Success rate for all sites")
    return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),Input(component_id='payload-slider', component_property='value')])
def update_scatter_chart(site, payload):
    filtered_df = spacex_df
    if site != 'ALL':
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload[0]) & (filtered_df['Payload Mass (kg)'] <= payload[1])]
    fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category", title=f"Payload vs Success for site {site}")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
