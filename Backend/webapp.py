import flask
from flask import render_template, request
import json
import sys
import datasource

app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/sample_results.html/<state>/<activity>')
def renderResults():
    result = DataSource()
    stateMinList = result.getActivityMinsByState(state, activity)
    return render_template('sample_results.html',
                            stateMinList = stateMinList)

'''
#Add a method that will render the "home page" you wrote for Part 1 of the project.
@app.route('/home')
def renderHome():
    return render_template('/homepage.html')
'''

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
