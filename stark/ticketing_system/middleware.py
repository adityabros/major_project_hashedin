from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

class JWTUserDecode:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        
        data = {'token': token}
        try:
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
            request.user = user
        except ValidationError as v:
            print("validation error", v)

        return response