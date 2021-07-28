#Importar librerias 

import pandas as pd 
import pickle 
import streamlit as st 
import joblib
import sklearn 

#cargar modelos 
lightgbm_4=joblib.load("modelo_lgbm_4.pkl")
lightgbm_1=joblib.load("modelo_lgbm_1.pkl")

#main 
def main(): 
    #Titulo del sitio
    st.title('ROP predictor_ test1')

    #Sidebar 
    st.sidebar.header('Choose parameters')

     #funcion para poner los parametros en el sidebar
    def user_input_parameters():

        
        #ROP= st.sidebar.slider('ROP', 0.0, 110.3, 3.5)
        BIT_DEPTH = st.sidebar.slider('depth', 16193, 18487, 16562)
        HKLD = st.sidebar.slider('Hook Load',295.1, 488.0, 452.6)
        WOB = st.sidebar.slider('WOB', 0.0, 414.0, 18.6)
        TORQUE = st.sidebar.slider('Torque', 0.0, 27.0, 14.5)
        BIT_RPM = st.sidebar.slider('Bit RPM', 0, 1822, 124)
        PUMP = st.sidebar.slider('Pump', 1010, 4561, 2871)
        FLOW_OUT_PC = st.sidebar.slider('Flow out', 0.0, 73.0, 34.4)
        FLOW_IN = st.sidebar.slider('Flow in', 0, 15371, 551)
        OVERBALANCE = st.sidebar.slider('Overbalance', 2.6, 5.6, 3.9)
        dT = st.sidebar.slider('Temperture Diference', -70, 92, -28)
        ROT_TIME = st.sidebar.slider('Rotary Time', 0.0, 147.0, 112.1)
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
    st.subheader('User Input Parameters')
    st.write(df)

    #escoger el modelo preferido
    option = ['Lgbm_4', 'Lgbm_1']
    model = st.sidebar.selectbox('Which model you like to use?', option)
    
    st.subheader('Model applied')
    st.write(model)
    
    if st.button('RUN'):
        if model == 'Lgbm_4':
            
            #Prediccion 
            px= lightgbm_4.predict(df)
            px1=pd.DataFrame(px)
            st.write(px1)

        elif model == 'Lgbm_1':
             
            #Prediccion 
            pc= lightgbm_1.predict(df)
            pc1=pd.DataFrame(pc)
            st.write(pc1)

        

    #Final 
if __name__ == '__main__':
    main()
