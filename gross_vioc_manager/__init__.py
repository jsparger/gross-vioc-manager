from flask import Flask
from flask_restful import reqparse, Resource, Api
import types
import os
import json
from distutils.dir_util import copy_tree
import vagrant
from subprocess import CalledProcessError

app = Flask(__name__)
api = Api(app)

# utility to allow route decorator on flask_restful Resource
def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper
api.route = types.MethodType(api_route, api)

# add parser
parser = reqparse.RequestParser()
parser.add_argument('content')

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

template = os.path.join(os.path.dirname(__file__), 'template')
valid_get_commands = ["status"]
valid_post_commands = ["destroy", "halt", "reload", "resume", "suspend", "up"]

@api.route("/vm/<hostname>/<command>")
class VM(Resource):
    def get(self, hostname, command):
        if command not in valid_get_commands:
            return ("Invalid command. Valid GET commands are: {}".format(valid_get_commands), 400)
        return self.execute(hostname, command)

    def post(self, hostname, command):
        if command not in valid_post_commands:
            return ("Invalid command. Valid POST commands are: {}".format(valid_post_commands), 400)
        return self.execute(hostname, command)

    def execute(self, hostname, command):
        try:
            # probably should sanitize the hostname before using it
            dest = app.instance_path + "/{}".format(hostname)
            copy_tree(template, dest)
        except OSError:
            return ("Problem creating VM directory", 500)
        with cd(dest):
            v = vagrant.Vagrant()
            method = getattr(v, command)
            try:
                result = method()
                message = result if result else "Calling {} on host {} was successful".format(command, hostname)
                return (message,200)
            except CalledProcessError:
                message = "Error calling {} on host {}".format(command, hostname)
                return (message, 500)
