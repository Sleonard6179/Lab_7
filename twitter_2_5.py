_author__ = 'sleonard'
from TwitterSearch import *
import arcpy
from arcpy import env

tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
tso.set_keywords(['Tacoma'])  # let's define all words we would like to have a look for
tso.set_include_entities(False)  # and don't give us all those entity information
tso.set_geocode(47.2414, -122.4594, 100, False) # This bit sets a search distance
                                                # Lat, Long, distance, True for meters, False for miles.
# Object creation with secret token
ts = TwitterSearch(
    consumer_key='ejOxTol16LSoRywZCscNN3TzI',
    consumer_secret='c2TBpLDoxANVb3Jg9TbxYvd76s9TnQwXISNR6EMkntvAO4CKMz',
    access_token='2864979423-QszBWpBwWHaPPAyzRzHA0KGznGsQcJOGyVLAPjd',
    access_token_secret='eRO9TR82RlHoEsSJh2iHQCg8O4Ue0kROFWTfCjvcPVC0S'
)
 # This is where the fun actually starts :)
env.workspace = "F:/GIS/A_Masters_Program/501/Lab_7"
workspace = "F:/GIS/A_Masters_Program/501/Lab_7/final/"
fc = "twitter_final.shp"
ft = "twitter_table.dbf"
fx = "twitter_excel.xls"
var1 = 3857 # WKID numeric code for spatial referenceing.
spat = arcpy.SpatialReference(var1) # Setting spatial ref.

# Create new Feature class and sets it as a point feature with a spatial ref.
arcpy.CreateFeatureclass_management(workspace, fc, "POINT", "", "", "", spat)
arcpy.CreateTable_management(workspace,ft)
# The next few lines create new fields in the feature class.
# Feature class name, Field name, field type, blah, blah, length, blah, allows nulls.
arcpy.AddField_management(workspace+fc, "TWEETER", "TEXT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(workspace+fc, "TWEETED", "TEXT", "", "", 100, "", "NULLABLE")
arcpy.AddField_management(workspace+fc, "SCRN_NAM", "TEXT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(workspace+fc, "LAT", "FLOAT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(workspace+fc, "LONG", "FLOAT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(workspace+fc, "DATE", "TEXT", "", "", 30, "", "NULLABLE")

arcpy.AddField_management(workspace+ft, "TWEETER", "TEXT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(workspace+ft, "TWEETED", "TEXT", "", "", 100, "", "NULLABLE")
arcpy.AddField_management(workspace+ft, "SCRN_NAM", "TEXT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(workspace+ft, "LAT", "FLOAT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(workspace+ft, "LONG", "FLOAT", "", "", 20, "", "NULLABLE")
arcpy.AddField_management(workspace+ft, "DATE", "TEXT", "", "", 30, "", "NULLABLE")

fields = ["TWEETER", "TWEETED", "SCRN_NAM", "LAT", "LONG", "DATE","SHAPE@XY"]
fields2  = ["TWEETER", "TWEETED", "SCRN_NAM", "LAT", "LONG", "DATE"]
# Create insert cursor to create rows from points obtained from twitter info.
curs1 = arcpy.da.InsertCursor(workspace+ft, fields2)
curs2 = arcpy.da.InsertCursor(workspace+fc, fields)
# For every tweet indexed using "search_tweets_iterable(tso) do some stuff.
for tweet in ts.search_tweets_iterable(tso):
    try:
        # But only do some stuff if the tweet has "place" info aka geo-tagged (sort of).
        if tweet['place'] is not None:


            # This begins an ugly bit of variable creation
            # G grabs coordinate info from tweets and put them in a Dictionary,
            G = (tweet['coordinates'])

            # So this bit turns the dict. G into a list of items. {Key:Value , Key:Value} becomes [key,value,key,value]
            H = list(reduce(lambda x, y: x + y, G.items()))
            # L,V,U, break down the list objects and eventually pulls the lat, long in a way so that it's usable to me.
            L = H[3]
            # L becomes just [long,lat]

            # V creates a list to put some stuff.
            V = []

            # U grabs the second value from L which is Lat, and the first value long.
            U = L[1], L[0]
            # U [lat,long]

            # But I couldn't get U to work the way it was so I appended it to V.
            # now that lat, long are in the right order lets append that to V to be used by the insert cursor.
            V.append(U)
            # More ugly variables.
            # B is the Tweeters user name. Tweet is a function of twitter_search_order
            # 'user' is a class of tweet, and 'name' is class of 'user'
            B = (tweet['user']['name'])

            # A returns the text of the tweet. I'd like to clean this up
            # and parse through for specific text, but yeah someother time.
            A = (tweet['text'])

            # D returns screen name much the same way that B returned user name.
            D = (tweet['user']['screen_name'])

            # Sets X as lat value, just like above, but this time for using it as a field value.
            X = L[1]

            # Same thing for Y.
            Y = L[0]

            # F returns a time date stamp.
            F = str((tweet['created_at']))

            curs1.insertRow([B,A,D,X,Y,F,])
            curs2.insertRow([B,A,D,X,Y,F,(X,Y)])
    except SystemError:
        print "error"

arcpy.TableToExcel_conversion(workspace+ft,workspace+fx)