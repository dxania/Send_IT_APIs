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
    

    def validate_parcel(parcel):
        messages = []
        error_dict = {'message(s)':messages}

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

    def validate_user_credentials(*args):
        for arg in args:
            if not arg:
                return jsonify({'message':"User name/password required"}), 400
            else:
                if not isinstance(arg, str):
                    return jsonify({'message':"User name/password must be strings"}), 400
                else:    
                    charset = re.compile('[A-Za-z]')
                    checkmatch = charset.match(arg)
                    if not checkmatch:
                        return jsonify({'message':'User name/password must be letters'}), 400

 
    

