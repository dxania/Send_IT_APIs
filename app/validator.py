import re

class Validator: 
    @staticmethod
    def validate_item(item):
        errors_list = []
        if not item.get("item_name") or not item.get('item_weight'):
            errors_list.append({'message':'Item field is required'})
        else:
            charset = re.compile('[A-Za-z]')
            checkmatch = charset.match(item.get("item_name"))
            if not checkmatch:
                errors_list.append({'message':'Item name must be letters'})
            if not isinstance(item.get('item_weight'), int):
                errors_list.append({'message':'Item weight must be a number'})
        
        return errors_list

    @staticmethod
    def validate_parcel(parcel):
        error_list = []
        charset = re.compile('[A-Za-z]')
        if not parcel['user_id']:
            error_list.append({'message':'User ID is required'})
        else:
            if not isinstance(parcel['user_id'], int):
                error_list.append({'message':'Enter a valid user ID'})

        if not parcel['destination'] or parcel['destination'].isspace():
            error_list.append({'message':'Destination is required'})
        else:
            checkmatch = charset.match(parcel['destination'])
            if not checkmatch:
                error_list.append({'message':'Destination must be letters'})

        if not parcel['recipient_name'] or parcel['recipient_name'].isspace():
            error_list.append({'message':'Recipient name is required'})
        else:
            checkmatch1 = charset.match(parcel['recipient_name'])
            if not checkmatch1:
                error_list.append({'message':'Recipient name must be letters'})

        if not parcel['recipient_mobile']:
            error_list.append({'message':'Recipient mobile contact is required'})
        else:
            if not isinstance(parcel['recipient_mobile'],int):
                error_list.append({'message':'Recipient mobile contact must be numbers'})
            else:
                if len(str(parcel['recipient_mobile'])) != 10:
                    error_list.append({'message':'Please enter a valid mobile contact'})

        if not parcel['pickup_location'] or parcel['pickup_location'].isspace():
            error_list.append({'message':'Pickup location is required'})
        else:
            checkmatch2 = charset.match(parcel['pickup_location'])
            if not checkmatch2:
                error_list.append({'message':'Pickup location must be letters'})

        return error_list


