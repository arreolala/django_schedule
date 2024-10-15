from django.utils.deprecation import MiddlewareMixin  

class JWTAuthPrefixMiddleware(MiddlewareMixin):  
    def __call__(self, request):  
        auth_header = request.headers.get('Authorization', '')  
        if auth_header and not auth_header.startswith('Bearer '):  
            # Assuming only JWT tokens will pass through here  
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {auth_header}'  
        return self.get_response(request)  
