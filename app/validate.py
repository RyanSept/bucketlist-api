import re


def validate_register(json):
    keys = ['email', 'first_name', 'last_name', 'password']

    for field in keys:
        if field not in json.keys():
            return (False,
                    "Missing fields in request data. Include: " +
                    ", ".join(keys)
                    )

    if len(json['password']) < 8:
        return (False, "The password should be more than 8 characters.")

    match = re.match(
        '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
        json["email"]
    )

    if match is None:
        return (False, "Email is invalid")

    return (True, "User successfully registered.")


