import mysql.connector as mysql


class User:
    cursor = "pass"
    db = "pass"

    def __init__(self):
        self.db = mysql.connect(
            host="localhost",
            user="root",
            password="",
            database="rest_api"
        )
        self.cursor = self.db.cursor()

    def insert_user_data(self, data):
        insert_user_details = "INSERT INTO User_Details" \
                              "(First_Name, Last_Name, Email, Password, Date_Of_Birth, Gender, mobile) " \
                              "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(insert_user_details, data)
        return self.cursor.lastrowid

    def insert_user_qualification(self, data):
        insert_user_highest_qualification_details = "INSERT INTO User_Highest_Qualification_Details (user_id, " \
                                                    "Highest_Qualification, Branch, Passout_month, Passout_year, " \
                                                    "Marks_type, Marks, State ,Institute, University) VALUES (%s, %s, " \
                                                    "%s, %s, %s, %s, %s, %s, %s, %s) "
        self.cursor.execute(insert_user_highest_qualification_details,data)
        return True

    def inert_user_roles(self, data):
        insert_user_roles = "INSERT INTO User_Roles" \
                            "(user_id,Roles) VALUES (%s, %s),(%s,%s),(%s,%s)"
        self.cursor.execute(insert_user_roles,data)
        return True

    def insert_user_address(self, data):
        insert_user_address_details = "INSERT INTO User_Address_Details" \
                                      "(user_id, Address_for_communication, Pin_code, Current_Residing_city, " \
                                      "Sub_Location)" \
                                      " VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(insert_user_address_details,data)
        return True

    def get_user(self, user_id):
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
        self.cursor.execute(user_query, [user_id])
        return self.cursor.fetchall()

    def get_user_education(self, user_id):
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
        self.cursor.execute(education_query, [user_id])
        return self.cursor.fetchall()

    def get_user_roles(self, user_id):
        roles_query = """   SELECT 
                            User_Roles.user_id, 
                            User_Roles.Roles,
                            Roles.Roles_Name
                            FROM User_Roles
                            LEFT JOIN Roles
                            ON User_Roles.Roles=Roles.id
                            WHERE User_Roles.user_id= %s    """
        self.cursor.execute(roles_query, [user_id])
        return self.cursor.fetchall()

    def execute_and_close(self):
        self.db.commit()
        self.cursor.close()
        self.db.close()
        return True
