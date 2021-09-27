
#Importar librerias 
import pandas as pd 
import pickle 
import streamlit as st 
import joblib
import sklearn 


#cargar modelos 
lightgbm_par_d1=joblib.load("modelo_lgbm_4.pkl")
lightgbm_par_d2=joblib.load("modelo_lgbm_d2.pkl")

#Titulo del sitio
st.title('Predictor de Rate of penetration (ROP)')

#descripcion del aplicativo
st.write("""
    
     **¡Bienvenido a pypredictorop!** 

     Podrás realizar predicciones acerca de cuál será la próxima ROP para una corrida teniendo en cuenta los siguientes 
     parámetros: **Profundidad, Carga en el gancho, WOB, torque, Revoluciones por minuto de la broca, Presión de la bomba, 
     flujo de salida, flujo de entrada, Overbalance, diferencia de temperatura, tiempo de rotación y desgaste de la broca.** 
     Además, podrás introducir los datos de forma manual, cargándolos mediante un archivo Excel [xlsx], donde podrás predecir 
     más de una corrida de manera simultánea. 

     """)

st.sidebar.title("Datos de entrada")

#escoger el modelo preferido
option = ['Desgaste lineal', 'Desgaste Radical']
model = st.sidebar.selectbox('Escoja un modelo de desgaste:', option)
    
st.subheader('Modelo de desgaste aplicado:',model)
st.write(model)

if model == 'Desgaste lineal':   
#main para desgaste lineal 
 def main(): 
  
    #subir un archivo con los parametros definidos
    st.sidebar.markdown("""
    [Descargar Archivo Excel guia](https://drive.google.com/uc?export=download&id=1NZGrbPItrW7ioNZ7jZ4rx7brh5CY64IT)
    """)
    # Collects user input features into dataframe
    uploaded_file = st.sidebar.file_uploader("Carga tu archivo .xlsx", type=["xlsx"])

    if uploaded_file is not None:
     df1 = pd.read_excel(uploaded_file)
     df1 = pd.DataFrame(df1)

     st.subheader('Datos que se usarán para el cálculo:')

     df1=df1[['BIT_DEPTH', 'HKLD', 'WOB', 'TORQUE',
       'BIT_RPM', 'PUMP', 'FLOW_OUT_PC', 'FLOW_IN', 'OVERBALANCE', 'dT',
       'ROT_TIME', 'DESGASTE']]
     st.write(df1)

     if st.button('Launch '):

        #Prediccion 
            pxx= lightgbm_par_d1.predict(df1)
            px2=pd.DataFrame(pxx)
            px2.columns = ['Prediction']

            st.subheader('La ROP esperada podría variar en ±0.9 [Ft/hr]:')
            st.write(px2)

            # grafico de matplot

            import plotly.express as px

            dfgraf=pd.DataFrame(dict(
            Predicción=px2["Prediction"],
            Profundidad=df1['BIT_DEPTH']
            ))

            fig = px.scatter(dfgraf,x="Predicción",y='Profundidad' 
            ,title='Gráfica Profundidad Vs ROP Predicha')
            
            st.plotly_chart(fig, use_container_width=True)

    else: 
     #funcion para poner los parametros en el sidebar
     def user_input_parameters():

        
 
        #ROP= st.sidebar.slider('ROP', 0.0, 110.3, 3.5)
        BIT_DEPTH = st.sidebar.slider('profundidad (ft)', 16193, 18487, 16562)
        HKLD = st.sidebar.slider('Hook Load (klbf)',380.0, 488.0, 452.6)
        WOB = st.sidebar.slider('WOB (klbf)', 0.0, 45.0, 18.6)
        TORQUE = st.sidebar.slider('Torque (kft.lb)', 0.0, 27.0, 14.5)
        BIT_RPM = st.sidebar.slider('RPM', 0, 290, 124)
        PUMP = st.sidebar.slider('Pump (psi)', 1330, 3650, 2871)
        FLOW_OUT_PC = st.sidebar.slider('Flow out (%)', 0.0, 55.0, 34.4)
        FLOW_IN = st.sidebar.slider('Flow in (USgal/min)', 0, 700, 551)
        OVERBALANCE = st.sidebar.slider('Overbalance (psi)', 2.6, 5.6, 3.9)
        dT = st.sidebar.slider('Temperture Diference (F°)', -10, 92, 28)
        ROT_TIME = st.sidebar.slider('Rotary Time (hr)', 0.0, 147.0, 112.1)
        DESGASTE = st.sidebar.slider('Desgaste', 0.0, 8.0, 1.6)
        
        data = {#'ROP': ROP,
                'BIT_DEPTH': BIT_DEPTH,
                'HKLD': HKLD,
                'WOB': WOB,
                'TORQUE': TORQUE,
                'BIT_RPM': BIT_RPM,
                'PUMP': PUMP,
                'FLOW_OUT_PC': FLOW_OUT_PC,
                'FLOW_IN': FLOW_IN,
                'OVERBALANCE': OVERBALANCE,
                'dT': dT,
                'ROT_TIME': ROT_TIME,
                'DESGASTE': DESGASTE,
                }
        features = pd.DataFrame(data, index=[0])
        return features
     df = user_input_parameters()

     #escritura de parametros seleccionados en la pagina
     st.subheader('Datos que se usarán para el cálculo:')
     st.write(df)
     if st.button('Launch'):

        #Prediccion 
            px= lightgbm_par_d1.predict(df)
            px1=pd.DataFrame(px)
            pxf= px1.iat[0,0]
            pxf= round(pxf, 3)
            st.write('La ROP esperada es de :', pxf, "± 0.9 [ft/hr] ")

           
    #Final 
 if __name__ == '__main__':
    main()

#desgaste radical lineas de codigo
elif model == 'Desgaste Radical':
#main para desgaste lineal 
 def main(): 
 
    #subir un archivo con los parametros definidos
    st.sidebar.markdown("""
    [Descargar Archivo Excel guia](https://drive.google.com/uc?export=download&id=1NZGrbPItrW7ioNZ7jZ4rx7brh5CY64IT)
    """)
    # Collects user input features into dataframe
    uploaded_file = st.sidebar.file_uploader("Carga tu archivo .xlsx", type=["xlsx"])

    if uploaded_file is not None:
     dfr1 = pd.read_excel(uploaded_file)
     dfr1 = pd.DataFrame(dfr1)

     st.subheader('Datos que se usarán para el cálculo:')

     dfr1=dfr1[['BIT_DEPTH', 'HKLD', 'WOB', 'TORQUE',
       'BIT_RPM', 'PUMP', 'FLOW_OUT_PC', 'FLOW_IN', 'OVERBALANCE', 'dT',
       'ROT_TIME', 'DESGASTE']]
     st.write(dfr1)

     if st.button('Launch '):

        #Prediccion 
            pxxr= lightgbm_par_d2.predict(dfr1)
            pxr2=pd.DataFrame(pxxr)
            pxr2.columns = ['Prediction']

            st.subheader('La ROP esperada podría variar en ± 0.9 [Ft/hr]:')
            st.write(pxr2)

            # grafico de plotly
            
            import plotly.express as px

            dfgraf=pd.DataFrame(dict(
            Predicción=pxr2["Prediction"],
            Profundidad=dfr1['BIT_DEPTH']
            ))

            fig = px.scatter(dfgraf,x="Predicción",y='Profundidad' 
            ,title='Gráfica Profundidad Vs ROP Predicha')
            
            st.plotly_chart(fig, use_container_width=True)
            
              

    else: 
     #funcion para poner los parametros en el sidebar
     def user_input_parameters_dr():

        #ROP= st.sidebar.slider('ROP', 0.0, 110.3, 3.5)
        BIT_DEPTH = st.sidebar.slider('profundidad (ft)', 16193, 18487, 16562)
        HKLD = st.sidebar.slider('Hook Load (klbf)',380.0, 488.0, 452.6)
        WOB = st.sidebar.slider('WOB (klbf)', 0.0, 45.0, 18.6)
        TORQUE = st.sidebar.slider('Torque (kft.lb)', 0.0, 27.0, 14.5)
        BIT_RPM = st.sidebar.slider('RPM', 0, 290, 124)
        PUMP = st.sidebar.slider('Pump (psi)', 1330, 3650, 2871)
        FLOW_OUT_PC = st.sidebar.slider('Flow out (%)', 0.0, 55.0, 34.4)
        FLOW_IN = st.sidebar.slider('Flow in (USgal/min)', 0, 700, 551)
        OVERBALANCE = st.sidebar.slider('Overbalance (psi)', 2.6, 5.6, 3.9)
        dT = st.sidebar.slider('Temperture Diference (F°)', -10, 92, 28)
        ROT_TIME = st.sidebar.slider('Rotary Time (hr)', 0.0, 147.0, 112.1)
        DESGASTE = st.sidebar.slider('Desgaste', 0.0, 8.0, 1.6)
        
        data = {#'ROP': ROP,
                'BIT_DEPTH': BIT_DEPTH,
                'HKLD': HKLD,
                'WOB': WOB,
                'TORQUE': TORQUE,
                'BIT_RPM': BIT_RPM,
                'PUMP': PUMP,
                'FLOW_OUT_PC': FLOW_OUT_PC,
                'FLOW_IN': FLOW_IN,
                'OVERBALANCE': OVERBALANCE,
                'dT': dT,
                'ROT_TIME': ROT_TIME,
                'DESGASTE': DESGASTE,
                }
        features = pd.DataFrame(data, index=[0])
        return features
     dfr = user_input_parameters_dr()

     #escritura de parametros seleccionados en la pagina
     st.subheader('Datos que se usarán para el cálculo:')
     st.write(dfr)
     if st.button('Launch'):

        #Prediccion 
            pxr= lightgbm_par_d2.predict(dfr)
            pxr1=pd.DataFrame(pxr)
            pxrf= pxr1.iat[0,0]
            pxrf= round(pxrf, 3)
            st.write('La ROP esperada es de :', pxrf, "± 0.9 [ft/hr] ")

           
    #Final 
 if __name__ == '__main__':
    main()
             
