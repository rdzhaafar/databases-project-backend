from restapi import restapi


@restapi.route("/")
@restapi.route("/home")
def greet():
    return "Hello, world"


