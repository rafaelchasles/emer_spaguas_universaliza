import streamlit as st
from streamlit_folium import folium_static
import folium
import geopandas as gpd
from folium.plugins import Fullscreen 


st.set_page_config(layout="wide")
# Caminho para o arquivo GeoJSON
mun_path = "data/mun_emergencia_spaguas_universalizasp.geojson"

# Função para carregar o GeoJSON com cache
@st.cache_data
def load_geojson(path):
    """
    Carrega um GeoJSON e retorna um GeoDataFrame.
    Os dados são armazenados em cache para melhorar o desempenho.
    """
    gdf = gpd.read_file(path)
    
    # Garantir que o GeoDataFrame tenha uma coluna de geometria válida
    if 'geometry' not in gdf.columns:
        raise ValueError("O GeoJSON não possui uma coluna 'geometry'.")
    
    return gdf


# Aplicação principal
try:
    # Carregar os dados do GeoJSON
    gdf = load_geojson(mun_path)


    # Criar o mapa com folium
    m = folium.Map(location=[-22.245, -48.669], zoom_start=6.5, tiles='CartoDB positron')


    Fullscreen(position='topright').add_to(m)

    # Criar camadas para cada GeoJSON
    mun_layer = folium.FeatureGroup(name="Municípios Emergência Estiagem", show=True)



    # Adicionar os dados GeoJSON ao mapa com hover e popup
    folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': 'green',  
            'color': 'green',      
            'weight': 2,     
            'fillOpacity': 0.5    
        },
            highlight_function=lambda feature: {
            'fillColor': 'red',             
            'color': 'red',                
            'weight': 3,                     
            'fillOpacity': 0.7           
            },

        tooltip=folium.GeoJsonTooltip(
            fields=['NOME'],  
            aliases=['Nome:'],  
            localize=True
        ),
        popup=folium.GeoJsonPopup(
            fields=['Municipios Estado Emergência - ESTIAGEM (Defesa Civil, 2024)', 'Relacionamento SP Águas', 'Adesão Universaliza SP', 'UGRHI', 'Área (km²)', 'População', 'SPI-06', 'Classificação SPI-06', 'Magnitude de Seca (meses)','Classificação de Falkenmark', 'Vazão Média Anual per capita (m³/dia.hab.)', 'Média Retirada Superficial (m³/s)', 'Média Retirada Subterrânea (m³/s)', 'Média Lançamento (m³/s)', 'Vazão Total Estoque', 'Balanço: Estoque - Cap. Total (m³/s)', 'Comprometimento Balanço Hídrico (5)', 'Classificação Comprometimento Balanço Hídrico', 'Classificação Manancial', 'Classificação Sistema Produtor', 'Eficiência Produção Água', 'Perdas', 'Cobertura (%)', 'Eficiência Distribuição Água', 'ISH-U', 'Demanda Urbana 2020 (litros/s)', 'Demanda Urbana 2035 (litros/s)', 'Operador Oficial', 'Tipo de Operador', 'Sistema Produtor', 'Tipo de Sistema', 'Manancial Abastecimento', 'Tipo de Manancial'],  # Campos no popup
            aliases=['Municipios Estado Emergência - ESTIAGEM (Defesa Civil, 2024)', 'Relacionamento SP Águas', 'Adesão Universaliza SP', 'UGRHI', 'Área (km²)', 'População', 'SPI-06', 'Classificação SPI-06', 'Magnitude de Seca (meses)','Classificação de Falkenmark', 'Vazão Média Anual per capita (m³/dia.hab.)', 'Média Retirada Superficial (m³/s)', 'Média Retirada Subterrânea (m³/s)', 'Média Lançamento (m³/s)', 'Vazão Total Estoque', 'Balanço: Estoque - Cap. Total (m³/s)', 'Comprometimento Balanço Hídrico (5)', 'Classificação Comprometimento Balanço Hídrico', 'Classificação Manancial', 'Classificação Sistema Produtor', 'Eficiência Produção Água', 'Perdas', 'Cobertura (%)', 'Eficiência Distribuição Água', 'ISH-U', 'Demanda Urbana 2020 (litros/s)', 'Demanda Urbana 2035 (litros/s)', 'Operador Oficial', 'Tipo de Operador', 'Sistema Produtor', 'Tipo de Sistema', 'Manancial Abastecimento', 'Tipo de Manancial'],  # Campos no popup
            localize=True
        )
    ).add_to(mun_layer)

    mun_layer.add_to(m)


    folium.LayerControl().add_to(m)
    


    # Exibir o mapa como estático
    folium_static(m, width=1200, height=600)

except FileNotFoundError:
    st.error(f"Arquivo GeoJSON não encontrado no caminho: {mun_path}")
except ValueError as ve:
    st.error(f"Erro nos dados GeoJSON: {ve}")
except Exception as e:
    st.error(f"Erro ao carregar o GeoJSON: {e}")
