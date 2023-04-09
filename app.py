import pandas as pd
from dash import Dash, Input, Output, State, dcc, html, dash_table, ALL, MATCH
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import base64
import operator
from io import BytesIO
from datetime import date
from datetime import datetime
from nltk.corpus import stopwords
import reddit_etl

print('Getting data...')
data = reddit_etl.grab_subreddit_sentiment()
print('Done grabbing and transforming reddit df')

# CSS
external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Reddit Sentiment Analysis Project"


sidebar = html.Div(
    [
        html.H1(
            children='Reddit Sentiment Analysis', className='header-title'
        ),
        html.Hr(className='my-line'),
        html.P(
            children=(
                'Top "hot" post titles in /r/Futurology'
            ),
            className='header-description',
        ),
        html.P(''),
        html.A('Link to subreddit', href='https://www.reddit.com/r/Futurology/', target='_blank', className='link-subreddit'),
        html.P(''),
        html.P(
            children=(
                    'Last updated: ' + str(datetime.now().strftime('%B %-d %Y, %-I:%M %p'))
            ),
            className='header-description-date',
        ),
    ],
    style={
        'position': 'fixed',
        'top': -10,
        'left': 0,
        'bottom': 0,
        'width': '14rem',
        'padding': '2rem 1rem',
        'background-color': '#dedede',
    }
)

# Layout
maindiv = html.Div(
    children=[
        html.Div(
            children=[
                    html.P('Wordcloud of the hottest posts', className='wordcloud_title', style={'margin-left': '280px',
                                                                                                 'margin-top': '30px'}),
                    html.Img(src='data:image/png;base64,' + reddit_etl.create_wordcloud(data), id='wordcloud_img',
                             style={'margin-left': '280px', 'margin-top': '10px'}),
            ],
            id='wordcloud'
        ),

        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Label(['Choose visualization:'],
                                   style={'font-weight': 'normal', 'color': 'black'}),
                        dcc.Dropdown(options=['Sentiment Score',
                                              'Frequency Table',
                                              'Frequency Chart',
                                              'Posts by Sentiment',
                                              'Polarity/Subjectivity'],
                                     value=[], id='dropdown',
                                     style={'width': '230px', 'height': '30px'}),
                        html.Div(id='dropdown_viz')
                    ],
                    style={'margin-left': '770px', 'margin-top': '-330px', 'margin-bottom': '30px', 'margin-right': '30px'}
                ),

                html.Div(
                    children=[
                        html.Div(id='dropdown_viz_detail')
                    ],
                    style={'margin-left': '833px', 'margin-top': '-66px', 'margin-bottom': '30px', 'margin-right': '30px'},
                    id='dropdown_detail_html'
                ),
            ],
        ),
    ],
)

def serve_layout():
    print('Getting data...')
    data = reddit_etl.grab_subreddit_sentiment()
    print('Done grabbing and transforming reddit df')

    # CSS
    external_stylesheets = [
        {
            "href": (
                "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap"
            ),
            "rel": "stylesheet",
        },
    ]
    app = Dash(__name__, external_stylesheets=external_stylesheets)
    app.title = "Reddit Sentiment Analysis Project"

    sidebar = html.Div(
        [
            html.H1(
                children='Reddit Sentiment Analysis', className='header-title'
            ),
            html.Hr(className='my-line'),
            html.P(
                children=(
                    'Top "hot" post titles in /r/Futurology'
                ),
                className='header-description',
            ),
            html.P(''),
            html.A('Link to subreddit', href='https://www.reddit.com/r/Futurology/', target='_blank',
                   className='link-subreddit'),
            html.P(''),
            html.P(
                children=(
                        'Last updated: ' + str(datetime.now().strftime('%B %-d %Y, %-I:%M %p'))
                ),
                className='header-description-date',
            ),
            html.Button('Update', id='update-button', n_clicks=0)
        ],
        style={
            'position': 'fixed',
            'top': -10,
            'left': 0,
            'bottom': 0,
            'width': '14rem',
            'padding': '2rem 1rem',
            'background-color': '#dedede',
        }
    )

    # Layout
    maindiv = html.Div(
        children=[
            html.Div(
                children=[
                    html.P('Wordcloud of the hottest posts', className='wordcloud_title', style={'margin-left': '280px',
                                                                                                 'margin-top': '30px'}),
                    html.Img(src='data:image/png;base64,' + reddit_etl.create_wordcloud(data), id='wordcloud_img',
                             style={'margin-left': '280px', 'margin-top': '10px'}),
                ],
                id='wordcloud'
            ),

            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Label(['Choose visualization:'],
                                       style={'font-weight': 'normal', 'color': 'black'}),
                            dcc.Dropdown(options=['Sentiment Score',
                                                  'Frequency Table',
                                                  'Frequency Chart',
                                                  'Posts by Sentiment',
                                                  'Polarity/Subjectivity'],
                                         value=[], id='dropdown',
                                         style={'width': '230px', 'height': '30px'}),
                            html.Div(id='dropdown_viz')
                        ],
                        style={'margin-left': '770px', 'margin-top': '-330px', 'margin-bottom': '30px',
                               'margin-right': '30px'}
                    ),

                    html.Div(
                        children=[
                            html.Div(id='dropdown_viz_detail')
                        ],
                        style={'margin-left': '833px', 'margin-top': '-66px', 'margin-bottom': '30px',
                               'margin-right': '30px'},
                        id='dropdown_detail_html'
                    ),
                ],
            ),
        ],
    )

    return html.Div([
    dbc.Row(
        [
            dbc.Col(sidebar, width=2),
            dbc.Col(maindiv, width=6)
        ]
    )
])

# Create the Dash app layout
# app.layout = html.Div([
#     dbc.Row(
#         [
#             dbc.Col(sidebar, width=2),
#             dbc.Col(maindiv, width=6)
#         ]
#     )
# ])

app.layout = serve_layout

@app.callback(
    Output('dropdown_viz', 'children'),
    [Input('dropdown', 'value')]
)
def select_viz(value):
    sorted_freq_df = reddit_etl.create_freq_df(data)

    if value == 'Frequency Table':
        dash_tbl = dash_table.DataTable(
            data=sorted_freq_df.head(30).to_dict('records'),
            columns=[{"name": i, "id": i} for i in sorted_freq_df.columns],
            style_cell={'textAlign': 'left', 'padding': '1px', 'border': '1px solid grey', 'fontSize': 14, 'font-family': 'Lato'},
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'border': '1px solid black',
                'color': 'black',
                'fontWeight': 'bold',
            },
            style_data={
                'backgroundColor': 'white',
                'color': 'black'
            },
            fill_width=False
        )

        return html.Div(children=[dash_tbl],
                 style={'margin-left': '0px', 'margin-top': '20px', 'margin-bottom': '30px', 'margin-right': '30px'}
                 )

    elif value == 'Frequency Chart':
        bar_chart_goFig = go.Figure(go.Bar(
            x=sorted_freq_df.head(40).Word,
            y=sorted_freq_df.head(40).Frequency,
            orientation='v'),
        )

        bar_chart_goFig.update_layout(
                        autosize=False,
                        width=600,
                        height=450,
                        margin=dict(
                            l=30,
                            r=30,
                            b=30,
                            t=50,
                            pad=4
                        ),
                        title='Commonly Used Words by Count',
                        xaxis=dict(tickmode='linear')
        )

        bar_chart_figure = dcc.Graph(figure=bar_chart_goFig)

        return html.Div(children=[bar_chart_figure],
                 style={'margin-left': '0px', 'margin-top': '20px', 'margin-bottom': '30px', 'margin-right': '30px'}
                 )

    elif value == 'Sentiment Score':

        pie_chart_goFig = go.Figure(data=[go.Pie(labels=['Neutral', 'Positive', 'Negative'],
                                     values=[data['Sentiment'].value_counts()['Neutral'],
                                             data['Sentiment'].value_counts()['Positive'],
                                            data['Sentiment'].value_counts()['Negative']])])
        pie_chart_goFig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=15)
                          # marker=dict(colors=colors, line=dict(color='#000000', width=2)))

        pie_chart_goFig.update_layout(
                        autosize=False,
                        width=400,
                        height=400,
                        margin=dict(
                            l=30,
                            r=30,
                            b=30,
                            t=50,
                            pad=4
                        ),
                        title='Overall Sentiment Breakdown - Count',
        )

        pie_chart_figure = dcc.Graph(figure=pie_chart_goFig)

        return html.Div(children=[pie_chart_figure],
                 style={'margin-left': '0px', 'margin-top': '20px', 'margin-bottom': '30px', 'margin-right': '30px'}
                 )

    elif value == 'Polarity/Subjectivity':
        scatter_plot_goFig = go.Figure()
        scatter_plot_goFig.add_trace(go.Scatter(
            x=data.query("Polarity == 0")['Polarity'],
            y=data.query("Polarity == 0")['Subjectivity'],
            marker=dict(color='lightgrey', size=9),
            mode='markers',
            marker_line=dict(width=1, color='black'),
            name='Neutral',
            text=data.query("Polarity == 0")['Title'].str.wrap(40).apply(lambda x: x.replace('\n', '<br>')),
            hovertemplate=
            "<b>%{text}</b><br><br>" +
            "Polarity: %{x:,.2f}<br>" +
            "Subjectivity: %{y:,.2f}<br>"
        ))

        scatter_plot_goFig.add_trace(go.Scatter(
            x=data.query("Polarity > 0")['Polarity'],
            y=data.query("Polarity > 0")['Subjectivity'],
            marker=dict(color='#6098d4', size=9),
            mode='markers',
            marker_line=dict(width=1, color='black'),
            name='Positive',
            text=data.query("Polarity > 0")['Title'].str.wrap(40).apply(lambda x: x.replace('\n', '<br>')),
            hovertemplate=
            "<b>%{text}</b><br><br>" +
            "Polarity: %{x:,.2f}<br>" +
            "Subjectivity: %{y:,.2f}<br>"
        ))

        scatter_plot_goFig.add_trace(go.Scatter(
            x=data.query("Polarity < 0")['Polarity'],
            y=data.query("Polarity < 0")['Subjectivity'],
            marker=dict(color='#9b4d4d', size=9),
            mode='markers',
            marker_line=dict(width=1, color='black'),
            name='Negative',
            text=data.query("Polarity < 0")['Title'].str.wrap(40).apply(lambda x: x.replace('\n', '<br>')),
            hovertemplate=
            "<b>%{text}</b><br><br>" +
            "Polarity: %{x:,.2f}<br>" +
            "Subjectivity: %{y:,.2f}<br>"
        ))

        scatter_plot_goFig.update_layout(title='Sentiment Analysis of Subreddit Posts',
                                         xaxis_title='Polarity',
                                         yaxis_title='Subjectivity',
                                         xaxis=dict(range=[-1.05, 1.05], showgrid=False, showline=True, linewidth=1,
                                                    linecolor='black', zeroline=False, ticks='outside', mirror=True,
                                                    dtick=0.25),
                                         yaxis=dict(range=[-0.05, 1.05], showgrid=False, showline=True, linewidth=1,
                                                    linecolor='black', zeroline=False, ticks='outside', mirror=True),
                                         plot_bgcolor='rgba(0,0,0,0)',
                                         width=650,
                                         height=380,
                                         margin=dict(
                                             l=30,
                                             r=30,
                                             b=30,
                                             t=50,
                                             pad=4
                                         ),
                        )

        scatter_plot_figure = dcc.Graph(figure=scatter_plot_goFig)

        return html.Div(children=[scatter_plot_figure],
                        style={'margin-left': '0px', 'margin-top': '20px', 'margin-bottom': '30px',
                               'margin-right': '30px'}
                        )

    elif value == 'Posts by Sentiment':
        return html.Div(children=[
            dcc.Dropdown(
                options=[
                    {'label': 'Positive', 'value': 'pos'},
                    {'label': 'Negative', 'value': 'neg'}
                ],
                multi=False,
                style={'width': '150px', 'height': '30px'},
                id={'type': 'sentiment_dropdown', 'index': 0}
            )
        ],
            style={'margin-left': '232px', 'margin-top': '-30px', 'margin-bottom': '30px', 'margin-right': '30px'}
        )

@app.callback(
    Output('dropdown_viz_detail', 'children'),
    [Input({'type': 'sentiment_dropdown', 'index': ALL}, 'value')]
)
def select_viz_detail(dropdown_detail_value):
    if dropdown_detail_value == ['pos']:
        dash_tbl = dash_table.DataTable(
            data=data.query("Sentiment == 'Positive'").head(30)[['Title', 'Average Score', 'Upvote Ratio']].to_dict('records'),
            columns=[{"name": i, "id": i} for i in ['Title', 'Average Score', 'Upvote Ratio']],
            style_cell={'textAlign': 'left', 'padding': '1px', 'border': '1px solid grey', 'fontSize': 14, 'font-family': 'Lato',
                        'maxWidth': '510px', 'whiteSpace': 'normal'},
            style_as_list_view=False,
            style_header={
                'backgroundColor': 'white',
                'border': '1px solid black',
                'color': 'black',
                'fontWeight': 'bold'
            },
            style_data={
                'backgroundColor': 'white',
                'color': 'black'
            },
            fill_width=False
        )

        return html.Div(children=[dash_tbl],
                 style={'margin-left': '-60px', 'margin-top': '90px', 'margin-bottom': '50px', 'margin-right': '15px'}
                 )

    elif dropdown_detail_value == ['neg']:
        dash_tbl = dash_table.DataTable(
            data=data.query("Sentiment == 'Negative'").head(30)[['Title', 'Average Score', 'Upvote Ratio']].to_dict('records'),
            columns=[{"name": i, "id": i} for i in ['Title', 'Average Score', 'Upvote Ratio']],
            style_cell={'textAlign': 'left', 'padding': '1px', 'border': '1px solid grey', 'fontSize': 14, 'font-family': 'Lato',
                        'maxWidth': '510px', 'whiteSpace': 'normal'},
            style_as_list_view=False,
            style_header={
                'backgroundColor': 'white',
                'border': '1px solid black',
                'color': 'black',
                'fontWeight': 'bold'
            },
            style_data={
                'backgroundColor': 'white',
                'color': 'black'
            },
            fill_width=False
        )

        return html.Div(children=[dash_tbl],
                 style={'margin-left': '-60px', 'margin-top': '90px', 'margin-bottom': '50px', 'margin-right': '15px'}
                 )


if __name__ == "__main__":
    app.run_server(debug=True)