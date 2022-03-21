import collections
import json
from django.http import JsonResponse
import mysql.connector as mysql
from django.http import HttpResponse
import sys
# sys.path is a list of absolute path strings
sys.path.insert(0, '/home/anish_mohanan/Rest_api/restproject/restapp/models')
from user import User


def user_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dump = json.dumps(data)

        """ convert to str dict """
        data_dict = json.loads(dump)

        """ task is insert_data(data_dict) """
        return HttpResponse(insert_data(data_dict))


def insert_data(insert_data):
    userDB = User()

    try:
        userData = [insert_data["First_Name"], insert_data["Last_Name"], insert_data["Email"], insert_data["Password"],
                     insert_data["Date_Of_Birth"], insert_data["Gender"],
                     insert_data["mobile"]]
        user_id = userDB.insert_user_data(userData)

        hq = insert_data["Highest_Qualification"][0]

        qualification_details = [user_id, hq["hq"], hq["Branch"], hq["Passout_month"],
                   hq["Passout_year"], hq["Marks_type"], hq["Marks"], hq["State"],
                   hq["Institute"], hq["University"]]
        userDB.insert_user_qualification(qualification_details)

        roles_details = [user_id, insert_data["Roles"][0], user_id, insert_data["Roles"][1], user_id, insert_data["Roles"][2]]
        userDB.inert_user_roles(roles_details)

        address_details = [user_id, insert_data["Address_for_communication"], insert_data["Pin_code"],
                   insert_data["Current_Residing_city"], insert_data["Sub_Location"]]
        userDB.insert_user_address(address_details)
        userDB.execute_and_close()
    except mysql.Error as err:
        nl = '\n'
        msg = f"Error is {err}. {nl}  Error Code: {err.errno} {nl} SQLSTATE: {err.sqlstate} {nl} Message: {err.msg} {nl}"
        return HttpResponse(msg)
    else:
        return HttpResponse("Data inserted successfully")


def get_details(request, user_id):
    """
    Function to get user details
    @params:request,user_id
    """
    db = mysql.connect(
        host="localhost",
        user="root",
        password="",
        database="rest_api"
    )
    cursor = db.cursor()
    try:
        user_id = user_id
        userDb = User()
        user_result = userDb.get_user(user_id)

        if not user_result:
            return HttpResponse("User ID Not Found. Please enter a valid ID")
        education_result = userDb.get_user_education(user_id)
        roles_result = userDb.get_user_roles(user_id)
        userDb.execute_and_close();

        # Convert query to objects of key-value pairs
        # objects_list = []
        d = collections.OrderedDict()
        for row in user_result:
            d["id"] = row[0]
            d["First_Name"] = row[1]
            d["Last_Name"] = row[2]
            d["Email"] = row[3]
            d["Date_Of_Birth"] = row[4]
            d["Gender"] = row[5]
            d["Address_for_communication"] = row[6]
            d["Pincode"] = row[7]
            d["Current_Residing_city"] = row[8]
            d["Sub_location"] = row[9]
            d["mobile"] = row[10]

            d["Highest_Qualification"] = []
            d["Roles"] = []

        for row in education_result:
            e = collections.OrderedDict()
            e["Course_Name"] = row[1]
            e["Course_type"] = row[2]
            e["Branch"] = row[3]
            e["Passout-month"] = row[4]
            e["Passout_year"] = row[5]
            e["marks_type"] = row[6]
            e["Marks"] = row[7]
            e["State"] = row[8]
            e["Institute"] = row[9]
            e["University"] = row[10]

            d["Highest_Qualification"].append(e)

        for row in roles_result:
            d["Roles"].append(row[2])

        return JsonResponse(d)

    except mysql.Error as err:
        nl = '\n'
        msg = f"Error is {err}. {nl}  Error Code: {err.errno} {nl} SQLSTATE: {err.sqlstate} {nl} Message: {err.msg} {nl}"
        return HttpResponse(msg)
