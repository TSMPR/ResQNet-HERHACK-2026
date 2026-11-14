import streamlit as st, requests, pandas as pd, os
st.set_page_config(page_title='ResQNet',page_icon='🚨',layout='wide')
API = st.sidebar.text_input('API base URL', os.environ.get('RESQNET_API_URL','http://127.0.0.1:8000')).rstrip('/')
st.title('🚨 ResQNet')
st.caption('Multilingual disaster-intelligence research prototype · Synthetic/demo mode')
st.warning('Not an emergency service. Predictions, duplicate matches and demo resources are unverified. Do not use for dispatch or real-world safety decisions. In India, call 112 for immediate emergencies.')
def get(path):
    try:
        r=requests.get(API+path,timeout=4); r.raise_for_status(); return r.json()
    except Exception as e: st.error(f'API unavailable: {e}'); return None
page=st.sidebar.radio('Workspace',['Submit report','Incident monitor','Resource inventory','About & limitations'])
if page == 'Submit report':
    st.subheader('Submit a report')
    with st.form('report'):
        txt=st.text_area('Incident description',height=130,placeholder='Describe what was reported. Do not include personal identifiers.')
        lang=st.selectbox('Language',['auto','en','te','hi'])
        c1,c2=st.columns(2); lat=c1.number_input('Latitude (optional)',value=0.0,format='%.6f'); lon=c2.number_input('Longitude (optional)',value=0.0,format='%.6f')
        submit=st.form_submit_button('Analyse report',type='primary')
    if submit:
        if len(txt.strip()) < 3: st.warning('Enter at least three characters.')
        else:
            try:
                r=requests.post(API+'/api/v1/reports',json={'text':txt,'language':lang,'latitude':lat or None,'longitude':lon or None},timeout=60); r.raise_for_status(); data=r.json(); pred=data['prediction']
                st.success('Report stored; human review required.')
                a,b=st.columns(2); a.metric('Top category',pred['category']); b.metric('Model score',f"{pred['score']:.3f}")
                st.caption('Uncalibrated model score, not the probability that an incident is real.')
                st.write(pred['explanation']); st.write('Evidence terms:',', '.join(pred['evidence_terms']) or 'None extracted')
                st.write('Alternative categories:',pred['alternatives']); st.write('Candidate duplicates:',data['candidate_duplicates']); st.code(data['report_id'])
            except Exception as e: st.error(str(e))
elif page == 'Incident monitor':
    st.subheader('Incident monitor'); m=get('/api/v1/metrics'); rows=get('/api/v1/reports')
    if m:
        a,b=st.columns(2); a.metric('Reports submitted',m['total_reports']); b.metric('Categories represented',len(m['by_category']))
        st.write('Category counts'); st.dataframe(pd.DataFrame(m['by_category']),use_container_width=True)
    if rows: st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
    if st.button('Refresh'): st.rerun()
elif page == 'Resource inventory':
    st.subheader('Demo resource inventory'); st.info('All bundled resources are fictional placeholders. No dispatch or availability verification is performed.')
    rows=get('/api/v1/resources')
    if rows: st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
else:
    st.markdown('''### Included in this MVP\n- Multilingual text classification baseline (word + character TF-IDF and Logistic Regression).\n- FastAPI report API and SQLite persistence.\n- Candidate duplicate matching using character n-gram similarity.\n- Human review endpoint and audit log.\n- Voice and image upload endpoints (storage only).\n- Synthetic demo dataset and Google Colab XLM-R training notebook.\n\n### Not yet implemented\n- Production live data feeds or official alert verification.\n- Actual speech transcription and image classification.\n- Calibrated model confidence, robust location extraction or live GIS clustering.\n- Real resource directories, dispatch or responder integration.\n\nAll sample records are synthetic. A model prediction is not a verified incident.''')
