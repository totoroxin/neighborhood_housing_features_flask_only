from threading import Thread

from bokeh.embed import components, server_document
from bokeh.server.server import Server
from flask import Flask, render_template
from tornado.ioloop import IOLoop

app = Flask(__name__)

BOKEH_URL = 'https://valueupneighborhood-bokeh.herokuapp.com'

@app.route('/', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def index():
    script_rent_cat_ny = server_document(f'{BOKEH_URL}/bokeh_category_rent_ny')
    script_rent_cat_nj = server_document(f'{BOKEH_URL}/bokeh_category_rent_nj')    
    script_med_rent = server_document(f'{BOKEH_URL}/bokeh_med_rent')
    script_pred_rent = server_document(f'{BOKEH_URL}/bokeh_pred_rent')

    return render_template(
        'index.html',
        script_rent_cat_ny=script_rent_cat_ny,
        script_rent_cat_nj=script_rent_cat_nj,       
        script_med_rent=script_med_rent,
        script_pred_rent=script_pred_rent,
    )

if __name__ == '__main__':
    app.run(port=8080)
