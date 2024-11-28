import requests
import matplotlib.pyplot as ts
import streamlit as st

# URL con filtros para reducir el tamaño de la respuesta
url = 'https://restcountries.com/v3.1/all?fields=name,population,area,flag,currencies,languages,capital'

countries_data = []

# Configurar una sesión con reintentos robustos
session = requests.Session()
retries = requests.adapters.Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[500, 502, 503, 504]
)
adapter = requests.adapters.HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

def obtener_datos_pais(pais):
    """Buscar un país y devolver sus datos relevantes."""
    for country in countries_data:
        name = country.get('name', {}).get('common', '')
        if name.lower() == pais.lower():
            population = country.get('population', 0)
            area = country.get('area', 0)
            capital = country.get('capital', ['Desconocida'])[0]
            flag = country.get('flags', {}).get('png', '')
            currencies = country.get('currencies', {})
            languages = country.get('languages', {})
            return {
                "name": name,
                "population": population,
                "area": area,
                "capital": capital,
                "flag": flag,
                "currencies": list(currencies.keys()),
                "languages": list(languages.values())
            }
    return None

# Realiza la solicitud a la API y procesa los datos
try:
    response = session.get(url, timeout=30)
    response.raise_for_status()  # Lanza excepción para errores HTTP
    countries_data = response.json()

    if not countries_data:
        st.write("No hay datos disponibles. Verifica la API.")
        exit()

except requests.exceptions.RequestException as e:
    st.write(f"Error durante la solicitud: {e}")
    countries_data = []

# Función para permitir la selección de país y obtener datos
def seleccionar_pais():
    countries_names = [country.get('name', {}).get('common', 'Desconocido') for country in countries_data]
    pais_elegido = st.selectbox("Seleccione un país para obtener información", countries_names)
    return pais_elegido

# Función para graficar los datos del país
def graficar_datos(pais_datos):
    # Obtener la información del país seleccionado
    nombre_pais = pais_datos['name']
    poblacion = pais_datos['population']
    area = pais_datos['area']
    idiomas = len(pais_datos['languages'])
    monedas = len(pais_datos['currencies'])

    # Crear las categorías y valores
    categorias = ['Población', 'Área (km²)', 'Idiomas', 'Monedas']
    valores = [poblacion, area, idiomas, monedas]

    # Preguntar al usuario qué tipo de gráfico quiere ver
    grafico = st.selectbox("Seleccione el tipo de gráfico", ["Gráfico de Barras", "Gráfico de Pastel", "Gráfico de Líneas"])

    # Crear los gráficos basados en la opción seleccionada
    if grafico == "Gráfico de Barras":
        # Gráfico de Barras
        fig, ax = plt.subplots(figsize=(8, 6))
        barras = ax.bar(categorias, valores, color=['skyblue', 'lightgreen', 'lightcoral', 'gold'])
        for barra in barras:
            yval = barra.get_height()
            ax.text(barra.get_x() + barra.get_width() / 2, yval + 0.02 * yval, int(yval), ha='center', va='bottom')
        ax.set_title(f"Datos de {nombre_pais}")
        ax.set_xlabel("Categorías")
        ax.set_ylabel("Valores")
        st.pyplot(fig)

    elif grafico == "Gráfico de Pastel":
        # Gráfico de Pastel
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(valores, labels=categorias, autopct='%1.1f%%', colors=['skyblue', 'lightgreen', 'lightcoral', 'gold'])
        ax.set_title(f"Distribución de datos de {nombre_pais}")
        st.pyplot(fig)

    elif grafico == "Gráfico de Líneas":
        # Gráfico de Líneas
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(categorias, valores, marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
        ax.set_title(f"Datos de {nombre_pais} en gráfico de líneas")
        ax.set_xlabel("Categorías")
        ax.set_ylabel("Valores")
        ax.grid(True)
        st.pyplot(fig)

# Página principal
def pagina_principal():
    st.title("Descripción del Proyecto")
    st.write("Este proyecto tiene como objetivo recopilar y analizar información relevante sobre diversos países del mundo, "
        "incluyendo datos sobre su población, idiomas, densidad, área, territorio, etc. A través de una plataforma digital interactiva.")

# Página para visualización de datos
def visualizacion_datos():
    st.title("Visualización de Datos")
    st.write("Aquí se mostrarán datos relevantes sobre diferentes países.")
    pais = seleccionar_pais()

    if pais:
        datos_pais = obtener_datos_pais(pais)
        if datos_pais:
            st.write(f"Datos de {datos_pais['name']}:")
            st.write(f"Capital: {datos_pais['capital']}")
            st.write(f"Población: {datos_pais['population']}")
            st.write(f"Área: {datos_pais['area']} km²")
            st.write(f"Monedas: {', '.join(datos_pais['currencies'])}")
            st.write(f"Idiomas: {', '.join(datos_pais['languages'])}")
        else:
            st.write("No se encontraron datos para este país.")

# Página de gráficos interactivos
def graficos_interactivos():
    st.title("Gráficos Interactivos")
    st.write("Esta sección permite interactuar con gráficos sobre diversos parámetros de los países.")
    pais = seleccionar_pais()

    if pais:
        datos_pais = obtener_datos_pais(pais)
        if datos_pais:
            graficar_datos(datos_pais)

# Función principal que gestiona la navegación
def main():
    # Título de la aplicación
    st.title("Aplicación de Análisis de Países del Mundo")

    # Barra lateral para navegación
    st.sidebar.title("Navegación")
    pagina = st.sidebar.selectbox("Selecciona una página", ["Página principal", "Visualización de datos", "Gráficos interactivos"])

    # Redirigir al contenido correspondiente según la página seleccionada
    if pagina == "Página principal":
        pagina_principal()
    elif pagina == "Visualización de datos":
        visualizacion_datos()
    elif pagina == "Gráficos interactivos":
        graficos_interactivos()

if __name__ == "__main__":
    main()
