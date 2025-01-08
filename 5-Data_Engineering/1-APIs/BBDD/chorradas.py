from flask import Flask, request   # Importamos Flask

app = Flask(__name__)  # Creamos una instancia de Flask

@app.route('/')  # Definimos la ruta raíz
def home():
    return "Alles gut"  # Respuesta


@app.route('/saludo1/<nombredelavariable>')  # Definimos la ruta raíz
def saludo1(nombredelavariable):
    return f"HOLA {nombredelavariable}"  # Respuesta


@app.route('/saludo2')  # Definimos la ruta raíz
def saludo2():
       
    # if "name" in request.args:
    #     name = request.args["name"]
    #     return f"OTRO HOLA {name}"  # Respuesta
    # return "no seas pelotudo"
    name = request.args.get("name", "desconocido")
    return f"OTRO HOLA {name}"

import requests  # Importamos requests para trabajar con APIs externas

@app.route('/country')
def country_info():

    country_name = request.args.get("country_name", None)

    if country_name:

        from openai import OpenAI
        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Write a haiku about {country_name}. Nothing but the haiku itself. No instructions. No metadata. Just the string with the haiku."
                }
            ]
        )

        haiku = completion.choices[0].message.content

        url = f"https://restcountries.com/v3.1/name/{country_name}"
        response = requests.get(url)  # Hacemos la solicitud a la API
        
        if response.status_code == 200:  # Si la solicitud fue exitosa
            data = response.json()
            return {
                "country_name": data[0]["name"]["common"],
                "region": data[0]["region"],
                "population": data[0]["population"],
                "haiku":haiku
            }
        else:  # Si hubo un error, devolvemos un mensaje
            return "sueño contigo"
    else:
        return "pelotudo"


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Ejecutamos la app