import streamlit as st
import pandas as pd
from streamlit_card import card
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_option_menu import option_menu
import gspread_dataframe as gd
scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]
df= pd.read_csv('voices_unavailable.csv')
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css('style.css')
st.image(image='HeaderBanner.jpg')
def append_variations(var):
    print('not overloaded')
    df2= pd.read_csv('voices_unavailable.csv')
    word=var[0]
    df2=df2.drop(df2.loc[df2['word']==word].index.values)
    variations=var[1]
    final=pd.read_csv('final.csv')
    final=final.append({
            'final words':word
        },ignore_index=True)
    for i in variations:
        final=final.append({
            'final words':i
        },ignore_index=True)
    final.to_csv('final.csv',index=False)
    df2.to_csv('voices_unavailable.csv',index=False)
    st.write('variations Added')
def append_variations_with_original_word(var,original):
    print('overloaded method')
    df2= pd.read_csv('voices_unavailable.csv')
    word=var[0]
    df2=df2.drop(df2.loc[df2['word']==original].index.values)
    variations=var[1]
    final=pd.read_csv('final.csv')
    final=final.append({
            'final words':word
        },ignore_index=True)
    for i in variations:
        final=final.append({
            'final words':i
        },ignore_index=True)
    final.to_csv('final.csv',index=False)
    df2.to_csv('voices_unavailable.csv',index=False)
    st.write('variations Added')
def append_correctness(corr):
    
    df2= pd.read_csv('voices_unavailable.csv')
    df2=df2.drop(df2.loc[df2['word']==corr[0]].index.values)
    final=pd.read_csv('final.csv')
    final=final.append({
        'final words':corr[1]
    },ignore_index=True)
    
    final.to_csv('final.csv',index=False)
    df2.to_csv('voices_unavailable.csv',index=False)
    st.write(corr[0] + ' id corrected to '+ corr[1])
def functionality():
    card(title=df[st.session_state["counter"]], text=' ', image="https://images.pexels.com/photos/2341290/pexels-photo-2341290.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1")
    st.markdown('<p class="urdu-font"; style=text-align:right; >درست لفظ اعراب کے ساتھ یہاں درج کریں۔</p>', unsafe_allow_html=True)
    incorr=st.text_input('')
    st.markdown('<p class="urdu-font"; style=text-align:right; >مزید املا شامل کیجیے۔</p>', unsafe_allow_html=True)
    st.markdown('<p class="urdu-font"; style=text-align:right; > ہر لفظ لکھنے کے بعد نیا لفظ انٹر دبا کر تحریر کریں </p>', unsafe_allow_html=True)
    var=st.text_area('')
    corr=st.checkbox('لفظ درست ہے۔')
    return {
        'correct form':incorr,
        'variations':var,
        'iscorrect':corr
    }
with st.sidebar:
    choose = option_menu("Modules", ["Correct Words","Data corrected Today","See Uploaded Data"],
                         icons=['check','search' ,'search'],
                          default_index=0)

if choose=='Correct Words':

    df=df['word']
    st.markdown('<p class="urdu-font"; style=text-align:right; >الفاظ کی درستگی کیجیے۔</p>', unsafe_allow_html=True)
    if "counter" not in st.session_state:
        st.session_state["counter"] = 0
    with st.form("My form",clear_on_submit=True):
        checked_data=functionality()
        
        submitted = st.form_submit_button("اندراج کیجیے۔")
        if submitted:
            if checked_data['correct form']!='' and checked_data['variations'].split('\n')[0]=='':
                print('1st one')
                append_correctness([df[st.session_state["counter"]],checked_data['correct form']])
            if checked_data['variations'].split('\n')[0]!='':
                st.write(len(checked_data['variations'].split('\n')))
                if checked_data['correct form']!='':
                    print('2nd one')
                    append_variations_with_original_word([checked_data['correct form'],checked_data['variations'].split('\n')],df[st.session_state["counter"]])
                else:
                    print('3rd one')
                    append_variations([df[st.session_state["counter"]],checked_data['variations'].split('\n')])
            if checked_data['iscorrect']==True:
                append_correctness([df[st.session_state["counter"]],df[st.session_state["counter"]]])
            st.write(checked_data['variations'].split('\n'))
            #st.session_state["counter"]=st.session_state["counter"]+1
            st.experimental_rerun()

if choose=='See Uploaded Data':
    credentials = ServiceAccountCredentials.from_json_keyfile_name("words-correction-a710f731b5e8.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open("Corrected words").sheet1
    a=sheet.get()
    x=pd.DataFrame(a)
    x.style.set_properties(**{'text-align': 'right'})
    st.write(x)
  
if choose=='Data corrected Today':
    credentials = ServiceAccountCredentials.from_json_keyfile_name("words-correction-a710f731b5e8.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open("Corrected words").sheet1
    #sheet=pd.read_csv('final.csv')
    final= pd.read_csv('final.csv')
    st.write(final)
    upload= st.button('Upload File')
    if upload:
        # final= pd.concat([final,pd.DataFrame(sheet.get())],axis=0)
        # #final= pd.concat([final,sheet],axis=0)
        # st.write(final)
        # sheet.clear()
        existing=gd.get_as_dataframe(sheet)
        updated= existing.append(final)
        gd.set_with_dataframe(sheet,updated)
        #set_withdataframe(worksheet=sheet,row=1, col=1, dataframe=final, include_index=False,include_column_header=True, resize=True)
        #sheet=sheet.update(final)
        final.drop(final.index, inplace=True)
        final.to_csv('final.csv',index=False)
        st.write('Data Uploaded Successfully')