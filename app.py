#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import json
import random

global inputs
global longueurIntro

longueurIntro = ""

with open('data.json', encoding='utf8') as f:
    inputs = json.load(f)
# print(data['data']['gages'][0]['text'])
# print(data['data']['chansons'][0]['url'])

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    }
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server



app.layout = html.Div(
    children=[

        html.Div(
            children=[
                html.P(id='placeholder', children=""),
                html.P(children="📻", className="header-emoji"),
                html.H1(
                    children="RADIO BATTLE !", className="header-title"
                ),
                html.P(
                    children="Le jeu de compétition entre animateurs de stations de radio rivales ! Quelle station a les meilleurs animateurs ?",
                    className="header-description",
                ),
            ],
            className="header",
        ),

        html.Div(children=[
            html.P("LES REGLES DU JEU", className="rulesTitle"),
            html.P("Deux équipes d'animateurs s'affrontent dans un jeu d'improvisation."),
            html.P("Le but du jeu est de meubler avant le lancement d'une chanson comme le ferais un animateur radio."),
            html.P("Toutefois les animateurs auront des contraintes à respecter afin de marquer des points !"),
            html.P("Pour marquer ces points les animateurs doivent dire toutes leurs contraintes avant que l'intro ne se termine"),
            html.P("Dans le cas ou l'animateur déborde sur la chanson ou finis trop tôt, il perds un point."),
            html.P("Et dans le cas ou ce dernier ne parvient pas à dire toutes ses containtes il ne marque pas les points associés."),
            html.P("L'équipe ayant le plus de points gagne !"),
           ],
            className="rules",
        ),

        html.Div(children=[

            html.Div(children=[
                html.P("Combien y a t-il de joueurs pour ce round ?"),
                dcc.RadioItems(id="nbJoueurs",
                    options=[
                        {'label': '1', 'value': '1'},
                        {'label': '2', 'value': '2'},
                        {'label': '3', 'value': '3'}
                    ],
                    value='2'),
            ], className="nbJoueurs"),

            html.Div(children=[
                html.P("Combien y a t-il de gages supplémentaires par joueur ?"),
                dcc.RadioItems(id="nbGages",
                    options=[
                        {'label': '2', 'value': 2},
                        {'label': '3', 'value': 3},
                        {'label': '4', 'value': 4}
                    ],
                    value='2'),
            ], className="nbGages"),

            html.Div(children=[
                html.Button('Go!', id='submit'),
                html.Button('Reset', id='reset')
            ], className="submitButton")

        ],
            className="form"
        ),

        html.Div(children=[
            html.Div(children=[
                html.Iframe(id="embed", src=f'https://www.youtube.com/embed/eRlipt5VNgc'),
            ], className="embedWrapper"),
            html.Div(children=[
                html.P(id="gagesTitle", children='Gages :', className="rulesTitle"),
                html.P(id="gagesObligatoires1", children="Dire son nom d'animateur"),
                html.P(id="gagesObligatoires2", children="Dire le nom de la radio"),
                html.P(id="gagesObligatoires3", children="Dire le nom de la chanson"),
                html.P(id="gages", className="gagesList", children='Ici doivent figurer les gages'),
                html.P(id="dureeIntro", children="Durée de l'intro en secondes.", className="rulesTitle")
            ])
        ], className="result")
    ]
)


@app.callback([Output('placeholder', 'children')], [Input('reset', 'n_clicks')])
def reset_game(click):
    global inputs
    with open('data.json', encoding='utf8') as f:
        inputs = json.load(f)
    return ""


@app.callback(Output('embed', 'src'), [Input('submit', 'n_clicks')], [State('nbJoueurs', 'value')])
def change_embed_iframe(click, value):
    global longueurIntro
    if click == None:
        return f'https://www.youtube.com/embed/eRlipt5VNgc'

    else:

        songs = inputs["data"]["chansons_difficulte_" + str(value)]  # string concatenation to switch the songs list
        # selects a random song in the chosen list
        aleaSong = random.randint(0, len(songs) - 1)
        print("aleaSong: ", aleaSong)
        songSelected = songs[aleaSong]

        # remove the previous selection in the database
        del songs[aleaSong]

        print("song selected : ", songSelected["url"], " duree: ", songSelected["longueurIntro"])

        longueurIntro = songSelected["longueurIntro"]

        return f'https://www.youtube.com/embed/{songSelected["embed"]}'


@app.callback(Output('gages', 'children'), [Input('submit', 'n_clicks')], [State('nbGages', 'value')])
def change_gages(click, value):
    if click == None:
        return 'Ici doivent figurer les gages'

    else:

        daresSelected = []
        daresList = inputs["data"]["gages"]
        for i in range(0, value):
            # selects a random dare in the database
            a = random.randint(0, len(daresList) - 1)
            daresSelected.append(daresList[a]["text"])

            # removes the previous selection in the database
            del daresList[a]

        return str(daresSelected)


@app.callback(Output('dureeIntro', 'children'), [Input('submit', 'n_clicks')])
def change_duree_intro(click):
    global longueurIntro
    if click == None:
        return "Durée de l'intro en secondes."

    else:
        print("longueurIntro = ", longueurIntro)
        #return "Durée de l'intro: " + longueurIntro + " secondes."
        return "Durée de l'intro: WIP"


@app.callback(Output('embed', 'style'), [Input('submit', 'n_clicks')])
def affichage_embed(click):
    if click == None:
        return {'display': 'none'}

    else:
        return {'display': 'block'}


@app.callback(Output('gages', 'style'), [Input('submit', 'n_clicks')])
def affichage_gages(click):
    if click == None:
        return {'display': 'none'}

    else:
        return {'display': 'block'}


@app.callback(Output('dureeIntro', 'style'), [Input('submit', 'n_clicks')])
def affichage_duree_intro(click):
    if click == None:
        return {'display': 'none'}

    else:
        return {'display': 'block'}

@app.callback(Output('gagesTitle', 'style'), [Input('submit', 'n_clicks')])
def affichage_gagesTitle(click):
    if click == None:
        return {'display': 'none'}

    else:
        return {'display': 'block'}

@app.callback(Output('gagesObligatoires1', 'style'), [Input('submit', 'n_clicks')])
def affichage_gagesObligatoire1(click):
    if click == None:
        return {'display': 'none'}

    else:
        return {'display': 'block'}

@app.callback(Output('gagesObligatoires2', 'style'), [Input('submit', 'n_clicks')])
def affichage_gagesObligatoire2(click):
    if click == None:
        return {'display': 'none'}

    else:
        return {'display': 'block'}

@app.callback(Output('gagesObligatoires3', 'style'), [Input('submit', 'n_clicks')])
def affichage_gagesObligatoire3(click):
    if click == None:
        return {'display': 'none'}

    else:
        return {'display': 'block'}

if __name__ == '__main__':
    app.run_server(debug=True)
