import flask
from flask import render_template, request, redirect
import json
import sys
import datasource
import matplotlib.pyplot as plt
import numpy as np

app = flask.Flask(__name__, static_folder='static', template_folder='template')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def createPlot(start, end, stateMins):
    # set up initial numbers
    years = np.arange(start, end + 1)
    x = np.arange(len(years))
    width = 0.5

    #create subplots, rectangles
    fig, ax = plt.subplots()
    if (start == end and start != "---"):
        plt.ylim(0, stateMins + 50)
    else:
        plt.ylim(0, max(stateMins) + 50)
    rects = ax.bar(x, stateMins, width)

    #create labels
    ax.set_ylabel('Average minutes spent')
    ax.set_xticks(x)
    ax.set_xticklabels(years)

    #create labels above showing exact numbers
    for rect in rects:
    	height = rect.get_height()
    	ax.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    fig.tight_layout()

    plt.savefig("static/Images/results_plot.png")

@app.route('/results', methods = ["GET"])
def renderResultTimeUsageRange():
    result = datasource.DataSource("diiannic", "corn972corn")
    state = request.args.get("state")
    activity = request.args.get("activity")
    start = request.args.get("start")
    end = request.args.get("end")
    if ((start == "---") and (end == "---")):
        stateMins = result.getActivityMinsByState(state, activity)
        start = 2014
        end = 2018
        year_message = "from " + str(start) + " to " + str(end)
        peopleSurveyed = result.getNumberOfPeopleSurveyedByStateAverage(state, start, end)
    elif (end == "---"):
        start = int(start)
        end = start
        year_message = "in " + str(start)
        stateMins = result.getActivityAverageMinsByYearAndState(start, state, activity)
        peopleSurveyed = result.getNumberOfPeopleSurveyedByStateAndYear(state, start)
    elif (start == "---"):
        end = int(end)
        start = end
        year_message = "in " + str(end)
        stateMins = result.getActivityAverageMinsByYearAndState(end, state, activity)
        peopleSurveyed = result.getNumberOfPeopleSurveyedByStateAndYear(state, end)
    else:
        start = int(start)
        end = int(end)
        if (start > end):
            temp = start
            start = end
            end = temp
        if start == end:
            year_message = "in " + str(start)
        else:
            year_message = "from " + str(start) + " to " + str(end)
        stateMins = result.getActivityMinsByStateRange(state, activity, start, end)
        peopleSurveyed = result.getNumberOfPeopleSurveyedByStateAverage(state, start, end)

    plt.clf()
    createPlot(start, end, stateMins)

    return render_template('sample_results.html', peopleSurveyed=peopleSurveyed, type=activity + " Time Usage", state=state, year=year_message)

@app.route('/')
def renderHome():
    return render_template('homepage.html')

@app.route('/aboutdata')
def renderAboutData():
    return render_template('aboutdata.html')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port, debug = True)
