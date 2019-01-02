class Parcel():
    """Parcels class defining the parcel model"""
    def __init__(self, user_id, user_name, parcel):    
        self.user_id = user_id
        self.user_name = user_name
        self.description = parcel['description']
        self.pickup_location = parcel['pickup_location']
        self.destination = parcel['destination']
        self.recipient_name = parcel['recipient_name']
        self.recipient_mobile = parcel['recipient_mobile']
        self.weight = parcel['weight']
        self.total_price = parcel['total_price']

    @staticmethod
    def get_delivery_price(weight):
        """Get total delivery price based on weight of a parcel"""
        if isinstance(weight, int):
            # if weight<500:
            #     delivery_price = 10000
            # elif 501<weight<1000:
            #     delivery_price = 100000
            # else: 
            #     delivery_price = 1000000
            # return delivery_price
            if weight<50:
                delivery_price = 10000
            elif 51<weight<100:
                delivery_price = 30000
            elif 101<weight<150:
                delivery_price = 60000
            elif 151<weight<200:
                delivery_price = 90000
            elif 201<weight<250:
                delivery_price = 150000
            elif 251<weight<300:
                delivery_price = 200000
            else: 
                delivery_price = 500000
            return delivery_price

    @staticmethod
    def to_dict(parcel):
        """Convert the parcel object to a dictionary"""
        parcel_dict = {
            "parcel_id": parcel[0],
            "description": parcel[1],
            "created_by": parcel[3],
            "recipient_name": parcel[4],
            "recipient_mobile": parcel[5],
            "pickup_location" : parcel[6],
            "destination": parcel[7],
            "weight": parcel[8],
            "total_price":parcel[9],
            "status": parcel[10],
            "present_location": parcel[11],
            "date_created":parcel[12]
        }
        return parcel_dict