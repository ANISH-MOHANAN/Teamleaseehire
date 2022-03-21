from django.db import models


class Branch(models.Model):
    branch_name = models.CharField(db_column='Branch_Name', max_length=50)  # Field name made lowercase.
    course_id = models.IntegerField(db_column='Course_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Branch'


class City(models.Model):
    city_name = models.CharField(db_column='city_Name', max_length=50)  # Field name made lowercase.
    state_id = models.IntegerField(db_column='State_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'City'


class Course(models.Model):
    course_name = models.CharField(db_column='Course_Name', max_length=50)  # Field name made lowercase.
    course_type = models.CharField(db_column='Course_type', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Course'


class Institute(models.Model):
    institute_name = models.CharField(db_column='Institute_Name', max_length=70)  # Field name made lowercase.
    city_id = models.IntegerField(db_column='City_id')  # Field name made lowercase.
    state_id = models.IntegerField(db_column='State_id')  # Field name made lowercase.
    university_id = models.IntegerField(db_column='University_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Institute'


class Roles(models.Model):
    roles_name = models.CharField(db_column='Roles_Name', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Roles'


class State(models.Model):
    state_name = models.CharField(db_column='State_Name', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'State'


class SubLocation(models.Model):
    location_name = models.CharField(db_column='Location_Name', max_length=50)  # Field name made lowercase.
    city_id = models.IntegerField(db_column='City_id')  # Field name made lowercase.
    state_id = models.IntegerField(db_column='State_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sub_Location'


class University(models.Model):
    university_name = models.CharField(db_column='University_Name', max_length=70)  # Field name made lowercase.
    state_id = models.IntegerField(db_column='State_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'University'


class UserAddressDetails(models.Model):
    user = models.ForeignKey('UserDetails', models.DO_NOTHING)
    address_for_communication = models.CharField(db_column='Address_for_communication', max_length=300)  # Field name made lowercase.
    pin_code = models.IntegerField(db_column='Pin_code')  # Field name made lowercase.
    current_residing_city = models.IntegerField(db_column='Current_Residing_city')  # Field name made lowercase.
    sub_location = models.IntegerField(db_column='Sub_Location')  # Field name made lowercase.
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'User_Address_Details'


class UserDetails(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(db_column='First_Name', max_length=50)  # Field name made lowercase.
    last_name = models.CharField(db_column='Last_Name', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=40)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=40)  # Field name made lowercase.
    date_of_birth = models.DateField(db_column='Date_Of_Birth')  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=6, blank=True, null=True)  # Field name made lowercase.
    mobile = models.BigIntegerField(unique=True)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'User_Details'


class UserHighestQualificationDetails(models.Model):
    user = models.ForeignKey(UserDetails, models.DO_NOTHING)
    highest_qualification = models.IntegerField(db_column='Highest_Qualification')  # Field name made lowercase.
    branch = models.IntegerField(db_column='Branch')  # Field name made lowercase.
    passout_month = models.IntegerField(db_column='Passout_month')  # Field name made lowercase.
    passout_year = models.IntegerField(db_column='Passout_year')  # Field name made lowercase.
    marks_type = models.CharField(db_column='Marks_type', max_length=10, blank=True, null=True)  # Field name made lowercase.
    marks = models.FloatField(db_column='Marks')  # Field name made lowercase.
    state = models.IntegerField(db_column='State')  # Field name made lowercase.
    institute = models.IntegerField(db_column='Institute')  # Field name made lowercase.
    university = models.IntegerField(db_column='University')  # Field name made lowercase.
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'User_Highest_Qualification_Details'


class UserRoles(models.Model):
    user = models.ForeignKey(UserDetails, models.DO_NOTHING)
    roles = models.IntegerField(db_column='Roles')  # Field name made lowercase.
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'User_Roles'
