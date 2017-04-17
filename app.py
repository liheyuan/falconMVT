from wsgiref import simple_server
import falcon
from middleware import auth_middleware
from api import account_api, test_api 

api = falcon.API(middleware=[
auth_middleware.AuthMiddleware()
])
# url for user
api.add_route('/account/login', account_api.LoginResource())
api.add_route('/test/noneedauth', test_api.TestNoNeedAuthResource())
api.add_route('/test/needauth', test_api.TestNeedAuthResource())

if __name__ == "__main__":
    httpd = simple_server.make_server('', 8000, api)
    httpd.serve_forever()
