import re
from flask import jsonify

class Validator: 
    def validate_str_to_change(arg):
        if not arg:
            return jsonify({"message":"Please enter a new value"}), 400
        else:  
            value = str(arg)
            charset = re.compile('[A-Za-z]')
            checkmatch_value = charset.match(value)
            if not checkmatch_value:
                return jsonify({'message':'The value must be letters'}), 400 
    

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

        variables = ['description', 'recipient_name', 'pickup_location', 'destination', 'recipient_mobile', 'weight']
        for variable in variables:
            if not parcel[variable]:
                # return jsonify({'message':f"Please enter the {variable}"}), 400
                messages.append(f"Please enter the {variable}")

            else:
                if not isinstance(parcel[variables[5]], int):
                    messages.append(f"Weight must be a number")
                    # return jsonify({'message':"Weight must be a number"}), 400
                if len(str(parcel[variables[4]])) != 10:
                    # return jsonify({'message':'Please enter a valid mobile contact'}), 400
                    messages.append('Please enter a valid mobile contact')
                    # print(parcel['recipient_mobile'])
                    
                string_variables = ['description', 'recipient_name', 'pickup_location', 'destination']
                for var in string_variables:
                    charset = re.compile('[A-Za-z]')
                    checkmatch = charset.match(str(parcel[var]))
                    if not checkmatch:
                        # return jsonify({'message':f"{var} must be letters"}), 400
                        messages.append(f"{var} must be letters")
            
        return error_dict

    def validate_user_login_credentials(user_name, user_password):
        if not user_password:
            return jsonify({'message':"Password required"}), 400
        if not user_name:
            return jsonify({'message':"User name required"}), 400
        else:
            uname = str(user_name)
            charset = re.compile('[A-Za-z]')
            checkmatch_username = charset.match(uname)
            if not checkmatch_username:
                return jsonify({'message':'User name must be letters'}), 400
               

    def validate_user_credentials(user_name, user_email, user_password, user_mobile):
        
        if not user_email:
            return jsonify({'message':"Email required"}), 400
        if not user_password:
            return jsonify({'message':"Password required"}), 400
        if not user_mobile:
            return jsonify({'message':"Mobile Contact required"}), 400
        else:
            if len(str(user_mobile)) != 10:
                return jsonify({'message':"Please enter a valid mobile contact"}), 400
        if not user_name:
            return jsonify({'message':"User name required"}), 400
        else:  
            uname = str(user_name)
            charset = re.compile('[A-Za-z]')
            checkmatch_username = charset.match(uname)
            if not checkmatch_username:
                return jsonify({'message':'User name must be letters'}), 400 
            
         
        

 
    

