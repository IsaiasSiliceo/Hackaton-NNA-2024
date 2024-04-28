import pandas as pd

import plotly.express as px

import json as json

import numpy as np

import zipfile
import json

from dash import Dash, html, dcc, callback, Output, Input

datos = pd.read_csv('../mapa.csv')

with zipfile.ZipFile('../geo.zip', 'r') as zip_ref:
    # Extract the JSON file from the ZIP archive
    zip_ref.extractall()

with open('geo.json', 'r') as f:
    counties = json.load(f)


# Histograma 1
counts_df = pd.read_csv('../Zai6a9.csv')
discapacidad_columns = [
    'Muletas', 'Aparato  auditivo', 'Lengua de señas', 'Silla de rueda',
    'Lentes', 'Otro', 'Ninguno'
]

fig_6a9 = px.bar(counts_df, x='Tipo de Discapacidad', y='Número de Niños', title='Discapacidad en niños de 6 a 9',
             labels={'Número de Niños':'Número de Niños', 'Tipo de Discapacidad': 'Tipo de Discapacidad'})

fig_6a9.update_layout(xaxis_title='Tipo de Discapacidad', yaxis_title='Número de Niños',
                  title={'text': 'Discapacidad en niños de 6 a 9 años', 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                  xaxis_tickangle=-45)

# Histograma 2
discapacidad_columns = [
    'Muletas', 'Aparato  auditivo', 'Lengua de señas', 'Silla de rueda',
    'Lentes', 'Otro', 'Ninguno'
]

counts_df3 = pd.read_csv('../Zai.csv')
fig3 = px.bar(counts_df3, x='Tipo de Discapacidad', y='Número de Niños', title='Discapacidad en niños de 10 a 13 años',
             labels={'Número de Niños':'Número de Niños', 'Tipo de Discapacidad': 'Tipo de Discapacidad'})

fig3.update_layout(xaxis_title='Tipo de Discapacidad', yaxis_title='Número de Niños',
                  title={'text': 'Discapacidad en niños de 10 a 13 años', 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                  xaxis_tickangle=-45)


# Violencia


# Datos
grupos = ['6 a 9 años', '10 a 13 años', '14 a 17 años']
valores1 = [11105, 7862, 6729]
valores2 = [9577, 7125, 5749]

# Crear el DataFrame
data = {
    'Grupo de edad': grupos * 2,
    'Valor': valores1 + valores2,
    'Género': ['Niñas'] * 3 + ['Niños'] * 3
}

# Crear la gráfica con Plotly Express
fig1 = px.bar(data, x='Grupo de edad', y='Valor', color='Género',
             color_discrete_map={'Niñas': 'pink', 'Niños': 'blue'},
             barmode='stack')

# Agregar título
fig1.update_layout(title='Casos de violencia en niñas, niños y jóvenes en CDMX')


discapacidad_columns = [
    'Muletas', 'Aparato  auditivo', 'Lengua de señas', 'Silla de rueda',
    'Lentes', 'Otro', 'Ninguno'
]

counts_df2 = pd.read_csv('../Zai14a17.csv')
fig2 = px.bar(counts_df2, x='Tipo de Discapacidad', y='Número de Niños', title='Discapacidad en niños de 14 a 17 años',
             labels={'Número de Niños':'Número de Niños', 'Tipo de Discapacidad': 'Tipo de Discapacidad'})

fig2.update_layout(xaxis_title='Tipo de Discapacidad', yaxis_title='Número de Niños',
                  title={'text': 'Discapacidad en niños de 14 a 17 años', 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
                  xaxis_tickangle=-45)



app = Dash(__name__)
# Define the meta tags and link tags
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- Letra de Google Fonts -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=League+Spartan&family=Nunito+Sans:wght@900&display=swap" rel="stylesheet">
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
app.layout = html.Div([
    # Espacio para un nuevo título
    html.Div(style={'height': '50px'}),
    html.Div(
        children=html.Div([
            html.H1('Cómo viven las Niñas, Niños y Adolescentes en México'),
            html.Div(style={'height': '10px'}),
            html.Div('Visualización de la distribución de NNA de acuerdo a la accesibilidad de servicios por cantidad de viviendas.')
        ], style={'width': '90%', 'margin': '0 auto'})
    ),
    html.Div(style={'height': '20px'}),
    # First row
    html.Div([
        # Barra para buscar un filtro entre grupos
        # Formato: Unicos | Grupo | id para la función
        # ['Población afrodescendiente',
       #'Población con condición mental', 'Población con discapacidad',
       #'Población hablante de lengua indígena', 'Población total']
        dcc.Dropdown(id='Filtro-grupo',options=[{'label': grupo, 'value': grupo} for grupo in datos['Población'].unique()],value='No disponen de energía eléctrica',
                     style={'width': '100%', 'margin': '0 auto'})
    ], style={'width': '40%', 'margin': '0 auto'}),
    # Gráfico
    html.Div([
        # Mapa de calor
        dcc.Graph(id = 'Mapa',hoverData={'points': [{'location': 'Aguascalientes'}],},style={'width': '100%','height':'500px'})     
    ], style={'width': '80%', 'margin': '0 auto'}),
    # Slider de los años
    html.Div([dcc.Slider(datos['Año'].min(),datos['Año'].max(),step=None,id='Slider',value=datos['Año'].max(),
                        marks={str(year): str(year) for year in datos['Año'].unique()}
    )], style={'width': '40%','margin':'0 auto'}),
    #dcc.Graph(id = 'mapa',figure=fig),
    html.Div(style={'height': '50px'}),
    
    # Third row
    html.Div([html.H2("Cantidad de Viviendas en esta situación y su relación con la diversidad de NNA en México")], style={'width': '90%', 'margin': '0 auto'}),
    html.Div([
        # Histograma
        html.Div([
            dcc.Graph(id='Histograma',style={'width': '100%', 'height': '500px'})
        ], style={'width': '50%', 'display': 'inline-block'}),
        # Imagen
        html.Div([
            html.Img(src="../assets/Cuadricula.jpeg", style={'width': '100%', 'height': 'auto'})
        ], style={'width': '50%', 'display': 'inline-block'})
    ], style={'width': '80%', 'margin': '0 auto'}),
    
    html.Div(style={'height': '30px'}),
    html.Div([
        # Image 1
        html.Img(src="../assets/Indigenas.jpeg", style={'width': '100%', 'height': 'auto','display':'inline-block'}),
        # Image 2
        html.Img(src="../assets/Discapacidad.jpeg", style={'width': '100%', 'height': 'auto','display':'inline-block'})
    ], style={'width': '80%', 'margin': '0 auto', 'display': 'inline-flex','text-align': 'center'}),
    html.Div(style={'height': '30px'}),

    html.Div(className="part1-text2", children=[
        html.H1('Consulta Infantil y Juvenil 2018 '),
        html.H2("¿Cuál es tu percepción de la violencia en ti?"),
        html.Br(),
        html.Br(),
        html.P("En desarrollo...", className="text"),
        # Add the Plotly Express figure here
        dcc.Graph(figure=fig1),
        html.H2("Discapacidad en Niñas, Niños y Adolescentes en México")
    ],style={'width': '70%', 'margin': '0 auto'}),
    html.Div([
        dcc.Graph(figure=fig_6a9, style={'display': 'inline-block', 'width': '30%'}),
        dcc.Graph(figure=fig3, style={'display': 'inline-block', 'width': '30%'}),
        dcc.Graph(figure=fig2, style={'display': 'inline-block', 'width': '30%'})
    ], style={'width': '100%', 'margin': '0 auto'}),
    html.Div(className='space'),
    html.Div(className="footer-cont", children=[
        html.Div(className="part2-footer", children=[
            html.Table(className="footer-menu", children=[
                html.Tr(children=[
                    html.Th("Acerca de", className="footer-title"),
                    html.Th("Redes", className="footer-title"),
                    html.Th("CIMAT", className="footer-title"),
                    html.Th("REDiM", className="footer-title")
                ]),
                html.Tr(children=[
                    html.Td(html.A("Data-neitors", href="#"), className="footer-item"),
                    html.Td(html.A("LinkedIn", href="https://www.linkedin.com/in/isaiassiliceo-096810268/",target="_blank"), className="footer-item"),
                    html.Td(html.A("CIMAT-MTY", href="https://www.cimat.mx/nuestras-sedes/sede-monterrey/"), className="footer-item"),
                    html.Td(html.A("REDiM", href="https://derechosinfancia.org.mx/v1/"), className="footer-item")
                ])
            ])
        ])
    ]),
    html.Div(className="footer-botton", children=[
        html.Img(src="/assets/conahcyt.svg",style={'width': '18%', 'height': 'auto'}),
        html.Img(src="/assets/cimat.png",style={'width': '14%', 'height': 'auto'}),
        html.Img(src="/assets/mtylogo(1).png",style={'width': '10%', 'height': 'auto'}),
        html.Div(className="links", children=[
            html.A("3er Hackatón por los Derechos de los Niños, Niñas y Adolescentes", href="https://retos.codeandomexico.org/challenges/3-3er-hackaton-por-los-derechos-de-la-ninez-y-la-adolescencia-en-mexico-2024"),
            html.P("@2024 La diversidad de las Niñas, Niños y Adolescentes. Data-neitors")
        ])
    ])
    
])

@callback(
    Output('Mapa', 'figure'),
    Input('Slider', 'value'),
    Input('Filtro-grupo','value'))
def update_graph(year_value,group):
    dff = datos[datos['Año'] == year_value]
    #dff = dff[dff['Pblación']==group]
    
    fig = px.choropleth_mapbox(dff, geojson=counties, 
                           featureidkey='properties.cve_agee',
                           locations='cve_agee', color='Cantidad',color_continuous_scale='Oryel',
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 19.42847, "lon": -99.12766},
                           range_color=(150000,200000),
                           opacity=0.5,
                           labels={'Metrica':'Metrica'}
                          )
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )
    return fig

@app.callback(
    Output('Histograma', 'figure'),
    [Input('Mapa', 'hoverData'),
     Input('Slider', 'value'),
     Input('Filtro-grupo','value')]
)
def update_histogram(hoverData, year,column):
    if hoverData is None:
        # If hoverData is None, set default value
        country_name = 'Aguascalientes'
    else:
        # Extract 'Estados' value from hoverData
        country_location = hoverData['points'][0]['location']
        filtered_data = datos[datos['cve_agee'] == country_location]
        if not filtered_data.empty:
            country_name = filtered_data['Entidad'].iloc[0]
        else:
            country_name = 'Unknown'
    
    # Filter DataFrame based on 'Estados' and 'Año'
    dff = datos[(datos['Entidad'] == country_name) & (datos['Año'] == year)]

    return create_histogram(dff,country_name,column)

def create_histogram(datos,country_name,column):
    
    fig = px.line(datos, x='Población', y='Cantidad', markers=True,title=country_name)
    #px.histogram(datos[['Edad',column]],x='Edad',y=column,
                       #title=country_name)
    #fig.update_layout(height=225, margin={'l': 30, 'b': 30, 'r': 30, 't': 30})

    return fig
if __name__ == '__main__':
    app.run(debug=True)
