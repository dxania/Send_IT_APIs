import re

class Validator: 
    @staticmethod
    def validate_item(item):
        err_messages = []
        errors_dict = {'message(s)':err_messages}
        charset = re.compile('[A-Za-z]')
        if not item.get("item_name") or not item.get('item_weight'):
            err_messages.append('Item field is required')
        else:
            checkmatch = charset.match(item.get("item_name"))
            if not checkmatch:
                err_messages.append('Item name must be letters')
            if not isinstance(item.get('item_weight'), int):
                err_messages.append('Item weight must be a number')        
        return errors_dict

    @staticmethod
    def validate_parcel(parcel):
        messages = []
        error_dict = {'message(s)':messages}
        charset = re.compile('[A-Za-z]')
        checkmatch_recipientname = charset.match(parcel['recipient_name'])
        checkmatch_pickuplocation = charset.match(parcel['pickup_location'])
        checkmatch_destination = charset.match(parcel['destination'])

        # if not parcel['user_id']:
        #     messages.append('User ID is required')
        # elif not isinstance(parcel['user_id'], int):
        #     messages.append('Enter a valid user ID')     

        if not parcel['recipient_name']:
            messages.append('Please enter a recipient name')
        else:
            if not isinstance(parcel['recipient_name'], str):
                messages.append('Recipient name must be a string')
            elif not checkmatch_recipientname:
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
            elif not checkmatch_pickuplocation:
                    messages.append('Pickup location must be letters')

        if not parcel['destination']:
            messages.append('Please enter a destination')
        else:
            if not isinstance(parcel['destination'], str):
                messages.append('Destination must be a string')
            elif not checkmatch_destination:
                    messages.append('Destination must be letters')

        return error_dict


