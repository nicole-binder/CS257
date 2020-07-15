import psycopg2
import getpass

class DataSource:

    '''
	DataSource executes all of the queries on the database.
	It also formats the data to send back to the frontend, typically in a list
	or some other collection or object.
	'''

    def __init__(self, user, password):
        try:
            self.connection = psycopg2.connect(database=user, user=user, password=password)
        except Exception as e:
            print("Connection error: ", e)
            exit()

    def getActivityMinsByState(self, state, activity):
            '''
            Returns a list of average minutes spent on the specified activity per day in the specified State.

            PARAMETERS:
                state - one of fifty United States' States or another region with a stateFIP code
                activity - one of the activities in the database

            RETURN:
                a list of all of average minutes spent on the specified activity per day by specified State
            '''
            listAverageActivityMins = []
            for year in range(2014, 2019):
                listAverageActivityMins.append(self.getActivityAverageMinsByYearAndState(year, state, activity))
            return listAverageActivityMins


    def getActivityAverageMinsByYearAndState(self, year, state, activity):
        '''
        Returns the average number minutes spent on the specified activity in the specified year.

        PARAMETERS:
                year - a year from 2014 to 2018
                state - one of the fifty United States' states, or another region with a stateFIP code
                activity - one of the activities in the database
        RETURN:
            the average number of minutes spent on that activity in that year
        '''
        try:
            cursor = self.connection.cursor()
            stateFIP = self.convertStateToStateFIP(state)
            activityCode = self.convertActivityToActivityCode(activity)
            query = "SELECT AVG(" + activityCode + ") FROM atus WHERE statefip = " + str(stateFIP) + " AND Year = " + str(year)
            cursor.execute(query)
            averageTuple = cursor.fetchone()
	    average = self.stripTupleWithOneElement(averageTuple)
	    return average

        except Exception as e:
            print("Something went wrong when executing getActivityAverageMinsByYearAndState: ", e)
            return None

    def getNumberOfPeopleSurveyedByStateAndYear(self, state, year):
    	'''
            Returns a count of people surveyed on the specified year in the specified State.

            PARAMETERS:
                state - one of fifty United States' States or another region with a stateFIP code
                year - a year from 2014 to 2018

            RETURN:
                a count of people surveyed on the specified year in the specified State.
            '''
    	try:
            cursor = self.connection.cursor()
            stateFIP = self.convertStateToStateFIP(state)
            query = "SELECT COUNT(*) FROM atus WHERE statefip = " + str(stateFIP) + " AND Year = " + str(year)
            cursor.execute(query)
            numberTuple = cursor.fetchone()
	    number = self.stripTupleWithOneElement(numberTuple)
	    return number

        except Exception as e:
            print("Something went wrong when executing getNumberOfPeopleSurveyedByStateAndYear: ", e)
            return None


    def stripTupleWithOneElement(self, tupleWithOneElement):
        '''
        Returns the value stored in the tuple input.

        PARAMETERS:
                tupleWithOneElement - a tuple with exactly one element
        RETURN:
            the content of the tuple passed to the function
        '''
        return tupleWithOneElement[0]


    def convertStateToStateFIP(self, state):
        '''
        Returns the StateFIP (numeric idenitification code) corresponding to the specified state.

        PARAMETERS:
                state - one of the fifty United States' states

        RETURN:
            the stateFIP number for database usage
        '''
        stateDict = {
                "Alabama" : 1,
                "Alaska" : 2,
                "Arizona" : 4,
                "Arkansas" : 5,
                "California" : 6,
                "Colorado" : 8,
                "Connecticut" : 9,
                "Delaware" : 10,
                "Florida" : 12,
                "Georgia"  : 13,
                "Hawaii" : 15,
                "Idaho" : 16,
                "Illinois" : 17,
                "Indiana": 18,
                "Iowa" : 19,
                "Kansas" : 20,
                "Kentucky" : 21,
                "Louisiana" : 22,
                "Maine" : 23,
                "Maryland" : 24,
                "Massachusetts" : 25,
                "Michigan" : 26,
                "Minnesota" : 27,
                "Mississippi" : 28,
                "Missouri": 29,
                "Montana": 30,
                "Nebraska": 31,
                "Nevada": 32,
                "New Hampshire": 33,
                "New Jersey": 34,
                "New Mexico": 35,
                "New York": 36,
                "North Carolina": 37,
                "North Dakota": 38,
                "Ohio":39,
                "Oklahoma":40,
                "Oregon":41,
                "Pennsylvania":42,
                "Rhode Island":44,
                "South Carolina":45,
                "South Dakota":46,
                "Tennessee":47,
                "Texas":48,
                "Utah":49,
                "Vermont":50,
                "Virginia":51,
                "Washington":53,
                "West Virginia":54,
                "Wisconsin":55,
                "Wyoming":56,
                "American Samoa":60,
                "Guam":66,
                "Northern Mariana Islands":69,
                "Puerto Rico":72,
                "Virgin Islands":78
                }
        assert state in stateDict, "Invalid state"
        return stateDict[state]



    def convertActivityToActivityCode(self, activity):
        '''
        Returns the activity code corresponding to the specified activity.

        PARAMETERS:
                activity - one of the activities in the database

        RETURN:
            the database column corresponding to the specified activity
        '''
        activityDict = {
                "Sleeping" : "Sleeping",
                "Eating and drinking" : "EatDrink",
                "Working" : "Working"

                }
        assert activity in activityDict, "Invalid activity"
        return activityDict[activity]


def main():
    user = "diiannic"
    password = "corn972corn"
    dataSource = DataSource(user, password)
    testAverage = dataSource.getActivityAverageMinsByYearAndState(2014, "California", "Eating and drinking")
    testAverageList = dataSource.getActivityMinsByState("New York", "Sleeping")
    print(str(testAverage) + " is the average minutes spent by Californians in 2014 eating and drinking.")
    print(testAverageList)
    print("^ is a list of average mins spent by New Yorkers sleeping, in the years 2014-2018.")
    shouldNotWork = dataSource.getActivityMinsByState("Not a state", "Sleeping")
    shouldNotWork = dataSource.getActivityMinsByState("Minnesota", "Not an Activity")
main()
