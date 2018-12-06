import re
from flask import jsonify

class Validator: 
    def validate_str_to_change(arg):
        if not arg:
            return jsonify({"message":f"Please enter a new value"}), 400
        if not isinstance(arg, str):
            return jsonify({"message":f"The value must be a string"}), 400
        if not arg.isalpha():
            return jsonify({"message":f"The value must be letters"}), 400

    def validate_status(parcel, status):
        statuses = ['pending','intransit','cancelled', 'delivered']
      
        if parcel[9] == 'cancelled' or parcel[9] == 'delivered':
            return jsonify({'message':'The parcel was either cancelled or delivered, status can not be changed'}), 400
        else:
            if status not in statuses:
                return jsonify({"message":f"Status can only be {statuses}"}), 400
            else:
                if parcel[9] == 'intransit' and status == statuses[0]:
                    return jsonify({'message':'The parcel is already in transit, status cannot be changed to pending'}), 400
                if parcel[9] == 'pending' and status ==  statuses[3]:
                    return jsonify({'message':'The parcel is yet to be delivered, consider updating to intransit'}), 400
    

    def validate_parcel(parcel):
        messages = []
        error_dict = {'message':messages}

        variables = ['recipient_name', 'pickup_location', 'destination', 'recipient_mobile', 'weight']
        for variable in variables:
            if not parcel[variable]:
                messages.append(f"Please enter the {variable}")

        string_variables = ['recipient_name', 'pickup_location', 'destination']
        for variable in string_variables:
            if not isinstance(parcel[variable], str):
                messages.append(f"{variable} must be a string")
            else:
                charset = re.compile('[A-Za-z]')
                checkmatch = charset.match(parcel[variable])
                if not checkmatch:
                    messages.append(f"{variable} must be letters")

        int_variables = ['recipient_mobile', 'weight']
        for variable in int_variables:
            if not isinstance(parcel[variable],int):
                messages.append(f"{variable} must be numbers")
            elif len(str(parcel['recipient_mobile'])) != 10:
                messages.append('Please enter a valid mobile contact')

        return error_dict

    def validate_user_login_credentials(user_name, user_password):
        if not user_name:
            return jsonify({'message':"User name required"}), 400
        if not user_password:
            return jsonify({'message':"Password required"}), 400
        else:
            uname = str(user_name)
            charset = re.compile('[A-Za-z]')
            checkmatch_username = charset.match(uname)
            if not checkmatch_username:
                return jsonify({'message':'User name must be letters'}), 400
               

    def validate_user_credentials(user_name, user_email, user_password):
        if not user_name:
            return jsonify({'message':"User name required"}), 400
        if not user_email:
            return jsonify({'message':"Email required"}), 400
        if not user_password:
            return jsonify({'message':"Password required"}), 400
        else:  
            uname = str(user_name)
            charset = re.compile('[A-Za-z]')
            checkmatch_username = charset.match(uname)
            if not checkmatch_username:
                return jsonify({'message':'User name must be letters'}), 400 
         
        

 
    

