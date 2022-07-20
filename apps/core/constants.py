
def result_success_list(value, self):
    serializer = self.get_serializer(value, many=True)
    json = {
        'data': serializer.data,
        'error': False,
        'message': 'Success',
        'code': 200
    }
    return json


def result_success_object(value, self):
    serializer = self.get_serializer(value)
    json = {
        'data': serializer.data,
        'error': False,
        'message': 'Success',
        'code': 200
    }
    return json