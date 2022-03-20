import collections
import json
from django.http import JsonResponse
import mysql.connector as mysql
from django.http import HttpResponse


# Create your views here.

def user_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dump = json.dumps(data)

        """ convert to str dict """
        data_dict = json.loads(dump)

        """ task is insert_data(data_dict) """
        return HttpResponse(insert_data(data_dict))


def insert_data(insert_data):
    db = mysql.connect(
        host="localhost",
        user="root",
        password="",
        database="rest_api"
    )
    cursor = db.cursor()

    try:
        insert_user_details = "INSERT INTO User_Details" \
                              "(First_Name, Last_Name, Email, Password, Date_Of_Birth, Gender, mobile) " \
                              "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = [insert_data["First_Name"], insert_data["Last_Name"], insert_data["Email"], insert_data["Password"],
                  insert_data["Date_Of_Birth"], insert_data["Gender"],
                  insert_data["mobile"]]
        cursor.execute(insert_user_details, values)

        user_id = cursor.lastrowid

        insert_user_highest_qualification_details = "INSERT INTO User_Highest_Qualification_Details (user_id, " \
                                                    "Highest_Qualification, Branch, Passout_month, Passout_year, " \
                                                    "Marks_type, Marks, State ,Institute, University) VALUES (%s, %s, " \
                                                    "%s, %s, %s, %s, %s, %s, %s, %s) "
        hq = insert_data["Highest_Qualification"][0]

        values2 = [user_id, hq["hq"], hq["Branch"], hq["Passout_month"],
                   hq["Passout_year"], hq["Marks_type"], hq["Marks"], hq["State"],
                   hq["Institute"], hq["University"]]
        cursor.execute(insert_user_highest_qualification_details, values2)

        insert_user_roles = "INSERT INTO User_Roles" \
                            "(user_id,Roles) VALUES (%s, %s),(%s,%s),(%s,%s)"

        values3 = [user_id, insert_data["Roles"][0], user_id, insert_data["Roles"][1], user_id, insert_data["Roles"][2]]
        cursor.execute(insert_user_roles, values3)

        insert_user_address_details = "INSERT INTO User_Address_Details" \
                                      "(user_id, Address_for_communication, Pin_code, Current_Residing_city, " \
                                      "Sub_Location)" \
                                      " VALUES (%s, %s, %s, %s, %s)"
        values4 = [user_id, insert_data["Address_for_communication"], insert_data["Pin_code"],
                   insert_data["Current_Residing_city"], insert_data["Sub_Location"]]
        cursor.execute(insert_user_address_details, values4)

        db.commit()
        cursor.close()
        db.close()
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
        user_query = """    SELECT
                            User_Details.user_id, 
                            User_Details.First_Name, 
                            User_Details.Last_Name, 
                            User_Details.Email, 
                            User_Details.Date_Of_Birth, 
                            User_Details.Gender, 
                            User_Address_Details.Address_for_communication, 
                            User_Address_Details.Pin_code, 
                            City.city_Name,  
                            Sub_Location.Location_Name, 
                            User_Details.mobile 
                            FROM User_Details  
                            LEFT JOIN User_Address_Details
                            ON User_Details.user_id = User_Address_Details.user_id
                            LEFT JOIN City
                            ON User_Address_Details.Current_Residing_city = City.id
                            LEFT JOIN Sub_Location
                            ON User_Address_Details.Sub_Location = Sub_Location.id
                            WHERE User_Details.user_id= %s  """

        education_query = """   SELECT 
                                User_Highest_Qualification_Details.user_id,
                                Course.Course_Name,
                                Course.Course_type,
                                Branch.Branch_Name,
                                User_Highest_Qualification_Details.Passout_month,
                                User_Highest_Qualification_Details.Passout_year,
                                User_Highest_Qualification_Details.Marks_type,
                                User_Highest_Qualification_Details.Marks,
                                State.State_Name,
                                Institute.Institute_Name,
                                University.University_Name
                                FROM User_Highest_Qualification_Details 
                                LEFT JOIN Course ON User_Highest_Qualification_Details.Highest_Qualification = Course.id
                                LEFT JOIN Branch ON User_Highest_Qualification_Details.Branch = Branch.id
                                LEFT JOIN Institute ON User_Highest_Qualification_Details.Institute = Institute.id
                                LEFT JOIN University ON User_Highest_Qualification_Details.University = University.id
                                LEFT JOIN State ON User_Highest_Qualification_Details.State = State.id
                                WHERE User_Highest_Qualification_Details.user_id= %s  """

        roles_query = """   SELECT 
                            User_Roles.user_id, 
                            User_Roles.Roles,
                            Roles.Roles_Name
                            FROM User_Roles
                            LEFT JOIN Roles
                            ON User_Roles.Roles=Roles.id
                            WHERE User_Roles.user_id= %s    """

        cursor.execute(user_query, [user_id])
        user_result = cursor.fetchall()
        if not user_result:
            return HttpResponse("User ID Not Found. Please enter a valid ID")

        cursor.execute(education_query, [user_id])
        education_result = cursor.fetchall()
        cursor.execute(roles_query, [user_id])
        roles_result = cursor.fetchall()

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
