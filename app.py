import dash
from dash import dcc, html, Output, Input, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Load the dataset from the csv file
csv_file_path = './ProcessedTweets.csv'
tweets_df = pd.read_csv(csv_file_path)

months= tweets_df['Month'].unique()

dropdown1 = html.Div(
    className="child1_1_1",
    children=[
        html.Label('Month', style={'font-weight': 'bold', 'margin-bottom':'14px', 'margin-right':'10px'}),
        html.Div(  # Wrapper div for the slider
            dcc.Dropdown(id='month', options=months, value=months[0]),
            style={'flex': '1'}  # This allows the slider to grow and take available space
        )
    ],
    style=dict(display='flex', alignItems='center', width="200px")
)
slider1 = html.Div(
    className="child1_1_1",
    children=[
        html.Label('Sentiment Score', style={'font-weight': 'bold', 'margin-bottom':'14px', 'margin-left':"15px"}),
        html.Div(  # Wrapper div for the slider
            dcc.RangeSlider(id='sentiment', min=-1, max=1, value=[-1, 1], marks={-1: '-1', 1: '1'}),
            style={'flex': '1'}  # This allows the slider to grow and take available space
        )
    ],
    style=dict(display='flex', alignItems='center', width="250px")
)
slider2 = html.Div(
    className="child1_1_3",
    children=[
        html.Label('Subjectivity Score', style={'font-weight': 'bold', 'margin-bottom':'14px'}),
        html.Div(  # Wrapper div for the slider
            dcc.RangeSlider(id='subjectivity', min=0, max=1, value=[0, 1], marks={0: '0', 1: '1'}),
            style={'flex': '1'}  # This allows the slider to grow and take available space
        )
    ],
    style=dict(display='flex', alignItems='center', width="250px")
)

column_name = 'RawTweet'

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(className="parent", children=[
    html.Div(className="child1",children=[html.Div([dropdown1,slider1,slider2], className="child1_1"),html.Div(dcc.Graph(id='graph1'), className="child1_2")]),
    dash_table.DataTable(
        id='selected-data-table',
        columns=[{"name": column_name, "id": column_name}],
        data=tweets_df[[column_name]].to_dict('records'),
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_header={
            'textAlign': 'center',
            'fontWeight': 'bold'
        },
        style_cell={
            'textAlign': 'center',  # Adjust the text alignment as needed
            'whiteSpace': 'normal',
              # Adjust fontSize as needed for readability
        },
        # Additional styling can be added here
    )
])

# graph1                                                             value = value we select
@app.callback(Output('graph1','figure'), [Input('month', "value"), Input('sentiment', "value"),  Input('subjectivity',"value")])
def myfunc(month, sentiment, subjectivity): 
    filtered_df = tweets_df[tweets_df['Month'] == month]
    filtered_df = filtered_df[(tweets_df['Sentiment'] >= sentiment[0]) & (tweets_df['Sentiment'] <= sentiment[1])]
    filtered_df = filtered_df[(tweets_df['Subjectivity'] >= subjectivity[0]) & (tweets_df['Subjectivity'] <= subjectivity[1])]
   
    # define scatterplot
    fig = px.scatter(filtered_df, x="Dimension 1", y="Dimension 2")
    fig.update_layout(dragmode='lasso',xaxis_title="",yaxis_title="")
    # Remove axis labels and tick marks
    fig.update_xaxes(tickvals=[], showticklabels=False, ticks="")
    fig.update_yaxes(tickvals=[], showticklabels=False, ticks="")
    return fig

# raw tweets table
@app.callback(Output('selected-data-table', 'data'),[Input('graph1', 'selectedData')])
def update_table(selectedData):
    if selectedData is not None:
        indices = [point['pointIndex'] for point in selectedData['points']]
        selected_df = tweets_df.iloc[indices]
        return selected_df.to_dict('records')
    return []

if __name__ == '__main__':
    app.run_server(debug=True)
