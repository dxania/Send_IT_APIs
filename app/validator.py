import re
from flask import jsonify

class Validator: 
    @staticmethod
    def validate_str_to_change(arg):
        if not arg:
            return jsonify({"message":"Please enter a new value"}), 200
        if not isinstance(arg, str):
            return jsonify({"message":"The value must be a string"}), 200
        if not arg.isalpha():
            return jsonify({"message":"The value must be a letters"}), 200
    
    
    @staticmethod
    def validate_parcel(parcel):
        messages = []
        error_dict = {'message(s)':messages}
        charset = re.compile('[A-Za-z]')

        if not parcel['recipient_name']:
            messages.append('Please enter a recipient name')
        else:
            if not isinstance(parcel['recipient_name'], str):
                messages.append('Recipient name must be a string')
            else:
                checkmatch_recipientname = charset.match(parcel['recipient_name'])
                if not checkmatch_recipientname:
                    messages.append('Recipient name must be letters')

        if not parcel['recipient_mobile']:
            messages.append('Please enter the recipients mobile contact')
        else:
            if not isinstance(parcel['recipient_mobile'],int):
                messages.append('Recipients mobile contact must be numbers')
            elif len(str(parcel['recipient_mobile'])) != 10:
                    messages.append('Please enter a valid mobile contact')

        if not parcel['pickup_location']:
            messages.append('Please enter a pickup location')
        else:
            if not isinstance(parcel['pickup_location'], str):
                messages.append('Pickup location must be a string')
            else:
                checkmatch_pickuplocation = charset.match(parcel['pickup_location'])
                if not checkmatch_pickuplocation:
                    messages.append('Pickup location must be letters')

        if not parcel['destination']:
            messages.append('Please enter a destination')
        else:
            if not isinstance(parcel['destination'], str):
                messages.append('Destination must be a string')
            else:
                checkmatch_destination = charset.match(parcel['destination'])
                if not checkmatch_destination:
                    messages.append('Destination must be letters')

        return error_dict

    @staticmethod
    def validate_username(user_name):
        if not user_name:
            return jsonify({'message':'User name is required'}), 200
        else:
            if not isinstance(user_name, str):
                return jsonify({'message':'User name must be a string'}), 200
            else:
                charset = re.compile('[A-Za-z]')
                checkmatch = charset.match(user_name)
                if not checkmatch:
                    return jsonify({'message':'User name must be letters'}), 200
                

    @staticmethod
    def validate_password(password):       
        if not password:
            return jsonify({'message':'Password is required'}), 200
        else:
            if not isinstance(password, str):
                return jsonify({'message':'Password must be a string'}), 200
            else:
                charset2 = re.compile('[A-Za-z0-9]')
                checkmatch = charset2.match(password)
                if not checkmatch:
                    return jsonify({'message':'Password should be letters and/or numbers'}), 200


