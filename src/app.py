import pandas as pd

import plotly.express as px

import json as json

import numpy as np

import zipfile
import json

from dash import Dash, html, dcc, callback, Output, Input

import plotly.graph_objs as go

datos = pd.read_csv('../mapa.csv')



#conteo
counts_hist1 = {
    'Edad de 6 a 9': {'Muletas': 33427, 'Aparato auditivo': 37990, 'Lengua de señas': 27677, 'Silla de rueda': 19310, 'Lentes': 190760, 'Otro': 62816, 'Ninguno': 1175772},
    'Edad de 10 a 13': {'Muletas': 7130, 'Aparato auditivo': 18541, 'Lengua de señas': 7333, 'Silla de rueda': 3939, 'Lentes': 307592, 'Otro': 37596, 'Ninguno': 1691828},
    'Edad de 14 a 17': {'Muletas': 3543, 'Aparato auditivo': 11347, 'Lengua de señas': 4122, 'Silla de rueda': 2842, 'Lentes': 333126, 'Otro': 20177, 'Ninguno': 1362447}
}

df_hist1 = pd.DataFrame(counts_hist1)


fig_Z1 = go.Figure()


colors = ['#89458D', '#48CFAE', '#227C9D', '#FF5733', '#FFC300', '#8A2BE2', '#FF4500']

# Agregar barras para cada edad
for i, (column, color) in enumerate(zip(df_hist1.columns, colors)):
    fig_Z1.add_trace(go.Bar(
        x=df_hist1.index,
        y=df_hist1[column],
        name=column,
        marker_color=color,
        textposition='auto' 
    ))


fig_Z1.update_layout(
    title="Discapacidad",
    xaxis_title="Tipo de Discapacidad",
    yaxis_title="Número de Niñas",
    barmode='group'
)


#Definir los conteos para el primer histograma
counts_hist1 = {
    'Edad de 6 a 9': {'Niñas': 134207, 'Niños': 35582, 'Niñas y Niños por igual': 481374, 'Ninguno': 13938},
    'Edad de 10 a 13': {'Niñas': 97789, 'Niños': 15425, 'Niñas y Niños por igual': 838938, 'Ninguno': 12839},
    'Edad de 14 a 17': {'Niñas': 233445, 'Niños': 33783, 'Niñas y Niños por igual': 549594, 'Ninguno': 39636}
}

# Definir los conteos para el segundo histograma
counts_hist2 = {
    'Edad de 6 a 9': {'Niñas': 166880, 'Niños': 31784, 'Niñas y Niños por igual': 362066, 'Ninguno': 114866},
    'Edad de 10 a 13': {'Niñas': 163037, 'Niños': 11640, 'Niñas y Niños por igual': 760876, 'Ninguno': 48377},
    'Edad de 14 a 17': {'Niñas': 56763, 'Niños': 7089, 'Niñas y Niños por igual': 798883, 'Ninguno': 3472}
}

# Crear los DataFrames
df_hist1 = pd.DataFrame(counts_hist1)
df_hist2 = pd.DataFrame(counts_hist2)

# Concatenar los DataFrames
result_df = pd.concat([df_hist1, df_hist2], keys=['En mi casa dicen que son más inteligentes…', ' Para ti, ¿quiénes pueden realizar tareas de la casa (lavar, planchar, limpiar, cocinar, entre otras)?'])

# Colores para las barras
colors = ['#89458D', '#48CFAE', '#227C9D']

# pregunta 1
fig1 = go.Figure()
for i, column in enumerate(df_hist1.columns):
    fig1.add_trace(go.Bar(
        x=df_hist1.index,
        y=df_hist1[column],
        name=column,
        marker_color=colors[i]
    ))

fig1.update_layout(
    title="En mi casa dicen que son más inteligentes…",
    xaxis_title="Respuesta",
    yaxis_title="Número de Niñas",
    barmode='group'
)

# pregunta 2
fig2 = go.Figure()
for i, column in enumerate(df_hist2.columns):
    fig2.add_trace(go.Bar(
        x=df_hist2.index,
        y=df_hist2[column],
        name=column,
        marker_color=colors[i]
    ))

fig2.update_layout(
    title="Para ti, ¿quiénes pueden realizar tareas de la casa (lavar, planchar, limpiar, cocinar, entre otras)?",
    xaxis_title="Respuesta",
    yaxis_title="Número de  Niñas",
    barmode='group'
)

# Mostrar los histogramas
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



app = Dash(__name__,external_scripts=["https://public.tableau.com/javascripts/api/tableau.embedding.3.latest.min.js"])
server = app.server

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
            html.H1('¿Cómo viven niñas, niños y adolescentes en México?'),
            html.Div(style={'height': '30px'}),
            html.Div(children=[' La infancia es algo que todos tenemos en común, sin embargo no todos la vivimos de la misma manera. Cuando nos preguntan sobre la situación de los niños en el país es inevitable recurrir a nuestra experiencia como punto de partida y formar una gran parte de nuestra opinión basada en ella, sin embargo esta forma de pensar puede llevarnos a conclusiones erradas. Por ejemplo, en esta era tecnológica resulta sensato creer que la gran mayoría de personas tienen acceso a internet, pues hoy en día más que un lujo, el internet representa una vía de acceso al conocimiento y la información. Actualmente vivir sin internet puede sonar tan arcaico como vivir sin electricidad, sin embargo más de 16 millones de hogares en México no cuentan con acceso a internet. Aunque parezca sorprendente millones de niñas, niños y jóvenes en México no cuentan con servicios básicos como electricidad o agua corriente. A continuación mostramos algunos datos y gráficos que nos pueden ayudar a comprender cómo vive la niñez en México con base en los datos proporcionados por el REDIM en la base Infancia Cuenta en México (2020) y algunas de sus respuestas sobre experiencias de violencia o agresión y discriminación obtenidas de la Consulta Infantil y Juvenil del INE (2018).']),
            html.Div(style={'height': '30px'}),
            html.Div(className='data-text', 
                     children='En México hay 38.2 millones de niñas, niños y adolescentes de 0 a 17 años de edad; esto representa el 30% de la población total del país.')
        ], style={'width': '90%', 'margin': '0 auto'})
    ),
    html.Div(style={'height': '20px'}),
    # First row
    html.Div([
    html.Iframe(src='https://public.tableau.com/views/Carenciadeserviciosenviviendasmexicanas/Dashboard1?:embed=yes&:showVizHome=no&:host_url=https%3A%2F%2Fpublic.tableau.com%2F&:embed_code_version=3&:tabs=no&:toolbar=yes&:animate_transition=yes&:display_static_image=yes&:display_spinner=yes&:display_overlay=yes&:display_count=yes&language=es-ES',
                style={'width': '100%', 'height': '1000px', 'border': 'none'})], style={'width': '90%', 'margin': '0 auto'}),
        
    html.Div(style={'height': '50px'}),
    
    # Third row
    html.Div([html.H2("Cantidad de Viviendas en esta situación y su relación con la diversidad de NNA en México")], style={'width': '90%', 'margin': '0 auto'}),
    html.Div([
        # Imagen
        html.Div([
            html.Img(src="../assets/Cuadricula.jpeg", style={'width': '100%', 'height': 'auto'})
        ], style={'width': '100%', 'display': 'inline-block'})
    ], style={'width': '80%', 'margin': '0 auto'}),
    
    html.Div(style={'height': '30px'}),
    
    html.Div(style={'height': '30px'}),
    html.Div([
        # Image 1
        html.Img(src="../assets/Indigenas.jpeg", style={'width': '100%', 'height': 'auto','display':'inline-block'}),
        # Image 2
        html.Img(src="../assets/afrodescendientes.jpeg", style={'width': '100%', 'height': 'auto','display':'inline-block'})
    ], style={'width': '80%', 'margin': '0 auto', 'display': 'inline-flex','text-align': 'center'}),
    html.Div(style={'height': '30px'}),

    html.Div(className="part1-text2", children=[
        html.H1('Consulta Infantil y Juvenil 2018 '),
        html.H2("¿Cuál es tu percepción de la violencia en ti?"),
        html.Br(),
        html.Br(),
        # Add the Plotly Express figure here
    ]),

    html.Div([
        dcc.Graph(figure=fig1, style={'width': '50%'}),
        html.Div(className="card", children=[
            html.Div(className="card-body", children=[
                html.P("'El castigo corporal y humillante contra niñas, niños y adolescentes, es una manera de crianza arraigada en nuestro país, aunque no hay cifras exactas sobre el castigo corporal y humillante contra niñas, niños y adolescentes en México, se puede comenzar a visibilizar la problemática. El siguiente gráfico muestra cuántos niños, niñas y jóvenes dijeron haber experimentado alguna clase de agresión en la CDMX.", className="text item")
            ], style={'width': '100%'})],style={'width': '50%'})
    ], style={'display':'flex','width': '100%', 'margin': '0 auto'}),
    html.Div([html.H2("Discapacidad en Niñas, Niños y Adolescentes en México")]),
    html.Div(className='data-text',children=[' La discapacidad más común entre los niños y adolescentes en México es la necesidad de "Lentes", lo que sugiere un impacto significativo en su acceso a la educación y su participación en actividades diarias.']),
    html.Div(dcc.Graph(figure=fig_Z1)),
    html.Div(className='space'),
    html.Div(className="footer-cont", children=[
        html.Div(className="part2-footer", children=[
            html.Table(className="footer-menu", children=[
                html.Tr(children=[
                    html.Th("Acerca de", className="footer-title"),
                    html.Th("Zai", className="footer-title"),
                    html.Th("Semir-amis", className="footer-title"),
                    html.Th("GSV", className="footer-title"),
                    html.Th("Chay", className="footer-title"),
                    html.Th("CIMAT", className="footer-title"),
                    html.Th("REDiM", className="footer-title")
                ]),
                html.Tr(children=[
                    html.Td(html.A("Data-neitors", href="#"), className="footer-item"),
                    html.Td(html.A("Zaira", href="https://www.linkedin.com/in/zaira-l%C3%B3pez-ju%C3%A1rez-29b0b026a/",target="_blank"), className="footer-item"),
                    html.Td(html.A("Semiramis", href="https://www.linkedin.com/in/semiramis-g-de-la-cruz-56b3181b4/",target="_blank"), className="footer-item"),
                    html.Td(html.A("Guillermo", href="https://www.linkedin.com/in/guillermo-sierra-vargas-05061720a/",target="_blank"), className="footer-item"),
                    html.Td(html.A("Isaias", href="https://www.linkedin.com/in/isaiassiliceo-096810268/",target="_blank"), className="footer-item"),
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

def create_histogram(datos,country_name,column):
    
    fig = px.line(datos, x='Población', y='Cantidad', markers=True,title=country_name)
    #px.histogram(datos[['Edad',column]],x='Edad',y=column,
                       #title=country_name)
    #fig.update_layout(height=225, margin={'l': 30, 'b': 30, 'r': 30, 't': 30})

    return fig
    

if __name__ == '__main__':
    app.run(debug=True)
