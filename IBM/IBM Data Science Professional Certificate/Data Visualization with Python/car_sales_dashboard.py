import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
df = pd.read_csv(URL)

app = dash.Dash(__name__)
app.layout = html.Div(children=[html.H1('Automobile Sales Statistics Dashboard', style={'textAlign':'center','color':'#503d36','font-size':24}),
                                html.Div([
                                    html.Div([
                                         html.H2('Report'),
                                         dcc.Dropdown(
                                            id='dropdown-satistics',
                                            options=[
                                                {'label':'Yearly Statistics','value':'Yearly Statistics'},
                                                {'label':'Recession Period Statistics','value':'Recession Period Statistics'}
                                            ],
                                            placeholder='Select a report type',
                                            style={
                                                'width':'80%',
                                                'padding':'3px',
                                                'font-size':'20px',
                                                'text-align-last':'center'},
                                            value='Select Statistics'
                                         )
                                    ]),
                                    html.Div([
                                        html.H2('Year'),
                                        dcc.Dropdown(
                                            id='select-year',
                                            value='Select-year',
                                            placeholder='Select-year',
                                            options=[{'label':i, 'value':i} for i in df['Year'].unique()],
                                            style={
                                                'width':'80%',
                                                'padding':'3px',
                                                'font-size':'20px',
                                                'text-align-last':'center'}	
                                        )
                                    ])
                                ]),
                                html.Div([
                                    html.Div([], id='output-container', className='chart-grid', style={'display': 'flex'}),
                                ],)
])

@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-satistics', component_property='value'))
def update_input_container(dropdown_value):
    return dropdown_value == 'Recession Period Statistics'

@app.callback(
    Output(component_id='output-container', component_property='children'),
    Input(component_id='dropdown-satistics', component_property='value'),
    Input(component_id='select-year', component_property='value'))
def update_output(statistics_value, year_value):
    if statistics_value == 'Recession Period Statistics':
        recession_data = df[df['Recession'] == 1]

        #Line chart: sales fluctuation during recession
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].sum().reset_index()
        R_chart1 = dcc.Graph(
            figure = px.line(yearly_rec, x='Year', y='Automobile_Sales', title='Automobile Sales During Recession')
        )
        #Bar chart: average number of vehicles sold by type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure = px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title='Average Number of Vehicles Sold by Type')
        )
        #Pie chart: total expenditure share by vehicle type
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure = px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type', title='Total Expenditure Share by Vehicle Type')
        )
        #Bar chart: effct of uneployment rate
        unemp_data = recession_data.groupby(['Year','unemployment_rate'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure = px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'}, title='Effect of Unemployment Rate on Automobile Sales')
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)],style={'display': 'flex'})
        ]
    
    elif(year_value and statistics_value=='Yearly Statistics'):
        yearly_data = df[df['Year'] == year_value]
    
        #Line chart: yearly automobile sales
        yas = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure = px.line(yas, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales')
        )

        #Line chart: monthly automobile sales
        mas = df.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure = px.line(mas, x='Month', y='Automobile_Sales', title='Monthly Automobile Sales')
        )

        #Bar chart: average number of vehicles sold during givn year
        avr_vdata = yearly_data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure = px.bar(avr_vdata, x='Month', y='Automobile_Sales', title='Average Number of Vehicles Sold')
        )

        #Pie: Advertisement spent per vehicle type
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure = px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', title='Advertisement Spent per Vehicle Type')
        )
    
        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)],style={'display': 'flex'})
        ]


if __name__ == '__main__':
    app.run_server()