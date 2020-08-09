from flask_restful import Resource


class VersionHandler(Resource):

    def get(self):
        return '0.0.1'
