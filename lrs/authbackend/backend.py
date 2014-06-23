# import the User object
from django.contrib.auth.models import User
from django.contrib import auth
import xmlrpclib as xmlrpc 	#Used for authenticating against wordpress using xmlrpc client
import requests		#Used for authenticating against UMCLoudDj using requests that need to be installed to python.

# Name my backend 'MyCustomBackend'
class MyCustomBackend:

    # Create an authentication method
    # This is called by the standard Django login procedure

    def authenticate(self, username=None, password=None):

        try:
            print("Checking if user exists in local UM LRS DB")
            # Try to find a user matching your username
            user = User.objects.get(username=username)

	    #Check credentials on UMCloudDj
	    credentials = {'username':username, 'password':password}
  	    resp = requests.post("http://54.72.83.134:8010/checklogin/", data=credentials)
	    print("Printing test response code:")
            print(resp.status_code)
	    """
            #Check user credentials
            s = xmlrpc.ServerProxy('http://www.ustadmobile.com/xmlrpc.php')     #Getting the xmlrpc link for ustadmobile.com wordpress
            if s.wpse39662.login(username,password):                            #Returns true if user is successfully authenticated, False if not
	    """
	    if resp.status_code == 200:
                print("Username and Password check success against custom backend for user already in DB.")
                return user;
            else:
                print ("Username and Password against custom backend un successful for already created user in DB-UM-LRS")
		if user.is_superuser:
			print("User is an admin or a superuser.")
			#Authenticate user against local DB...
			#return user;
		else:
			print("User isn't a superuser/admin. Returning false")
			return None
                return None;

            return None

        except User.DoesNotExist:
            # No user was found, return None - triggers default login failed
	    print("User Does Not Exists in UM LRS DB")
	
	    #Check credentials on UMCloudDj
            credentials = {'username':username, 'password':password}
            resp = requests.post("http://54.72.83.134:8010/checklogin/", data=credentials)
            print("Printing test response code:")
            print(resp.status_code)

	    """
	    #Check user credentials
	    s = xmlrpc.ServerProxy('http://www.ustadmobile.com/xmlrpc.php')	#Getting the xmlrpc link for ustadmobile.com wordpress
	    if s.wpse39662.login(username,password):				#Returns true if user is successfully authenticated, False if not
	    """
	    if resp.status_code == 200:
	    	print("Username and Password check success for new user.")
		print("Checking new user in Django..")
		#Create user.
		user_count = User.objects.filter(username=username).count()
        	if user_count == 0:
			print ("User doesn't exist, creating user..")
			user = User(username=username, email=username)
    			#user.set_password(password)
    			user.save()
			print("User created!")
        		#return auth_and_login(request)
			return user;
    		else:
        		#Show message that the username/email address already exists in our database.
			print("Error in creating user. User already exists!")
        		return redirect("/login/")

	    else:
		print("Username and Password check unsuccessfull for new user. Not creating new user.")
		return None

            #return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
	print("In get_user")
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
	    print("User does not exist")
            return None
