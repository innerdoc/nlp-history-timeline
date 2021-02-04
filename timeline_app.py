# Javascript Timeline in Streamlit App

# github TimelineJS3 repo   : https://github.com/NUKnightLab/TimelineJS3
# html for timeline         : https://timeline.knightlab.com/docs/instantiate-a-timeline.html
# local js and css          : https://cdn.knightlab.com/libs/timeline3/latest/timeline3.zip
# timeline json format      : https://timeline.knightlab.com/docs/json-format.html
# streamlit render html     : https://docs.streamlit.io/en/stable/develop_streamlit_components.html#render-an-html-string

import json
import streamlit as st
import streamlit.components.v1 as components


# must be called as first command
try:
    st.set_page_config(layout="wide")
except:
    st.beta_set_page_config(layout="wide")


# parameters
CDN_LOCAL = False
CDN_PATH = 'https://cdn.knightlab.com/libs/timeline3/latest'
CSS_PATH = 'timeline3/css/timeline.css'
JS_PATH = 'timeline3/js/timeline.js'

SOURCE_TYPE = 'json' # json or gdocs
GDOCS_PATH = 'https://docs.google.com/spreadsheets/u/1/d/1xuY4upIooEeszZ_lCmeNx24eSFWe0rHe9ZdqH2xqVNk/pubhtml' # example url
JSON_PATH = 'timeline_nlp.json' # example json

TL_HEIGHT = 800 # px


# load data
json_text = ''
if SOURCE_TYPE == 'json':
    with open(JSON_PATH, "r") as f:
        json_text = f.read()
        source_param = 'timeline_json'
        source_block = f'var {source_param} = {json_text};'
elif SOURCE_TYPE == 'gdocs':
    source_param = f'"{GDOCS_PATH}"'
    source_block = ''


# load css + js
if CDN_LOCAL:
    with open(CSS_PATH, "r") as f:
        css_text = f.read()
        css_block = f'<head><style>{css_text}</style></head>'

    with open(JS_PATH, "r") as f:
        js_text = f.read()
        js_block  = f'<script type="text/javascript">{js_text}</script>'
else:
    css_block = f'<link title="timeline-styles" rel="stylesheet" href="{CDN_PATH}/css/timeline.css">'
    js_block  = f'<script src="{CDN_PATH}/js/timeline.js"></script>'


# write html block
htmlcode = css_block + ''' 
''' + js_block + '''

    <div id='timeline-embed' style="width: 95%; height: '''+str(TL_HEIGHT)+'''px; margin: 1px;"></div>

    <script type="text/javascript">
        var additionalOptions = {
            start_at_end: false, is_embed:true,
        }
        '''+source_block+'''
        timeline = new TL.Timeline('timeline-embed', '''+source_param+''', additionalOptions);
    </script>'''


# UI sections
data = 'Data'
code = 'HTML Code'
line = 'Visualization'
about = 'About'
view = st.sidebar.radio("View", (line, data, about), index=0) # code

if view == line:
    # render html
    components.html(htmlcode, height=TL_HEIGHT,)

elif view == data:
    st.subheader(data)
    json_parsed = json.loads(json_text)
    st.write(f"{len(json_parsed['events'])} events")

    # show json
    st.json(json_text)

elif view == code:
    st.subheader(code)
    st.markdown(htmlcode, unsafe_allow_html=False)

elif view == about:
    st.subheader(about)
    st.markdown('This Streamlit + TimelineJS demo is created by [Rob van Zoest](https://www.linkedin.com/in/robvanzoest/) from [innerdoc.com](https://www.innerdoc.com/).')
    st.markdown('The code is available on [github.com/innerdoc](https://github.com/innerdoc/nlp-history-timeline).')
    st.markdown('With the help of [Streamlit](https://streamlit.io) and [TimelineJS](http://timeline.knightlab.com/) it became a demo timeline about the history of Natural Language Processing!')