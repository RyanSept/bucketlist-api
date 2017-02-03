import re


class Validation:
    '''Class for returning validation results'''

    def __init__(self):
        self.status = None
        self.message = ""


def validate_register(json):
    keys = ['email', 'first_name', 'last_name', 'password']
    validation = Validation()
    for field in keys:
        if field not in json.keys():
            validation.status = False
            validation.message = "Missing fields in request data. Include: " +\
                ", ".join(keys)
            return validation

    if len(json['password']) < 8:
        validation.status = False
        validation.message = "The password should be more than 8 characters."
        return validation

    match = re.match(
        '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
        json["email"]
    )

    if match is None:
        validation.status = False
        validation.message = "Email is invalid"
        return validation

    validation.status = True
    validation.status = "User successfully registered."
    return validation


def validate_bucketlist(json):
    validation = Validation()
    try:
        if not len(json['name']) > 0:
            validation.status = False
            validation.message = "The bucketlist name is too short."
        else:
            validation.status = True
            validation.message = "Bucketlist successfully created!"
        return validation
    except KeyError:
        validation.status = False
        validation.message = "You did not include a bucketlist name."
        return validation


def validate_item(json):
    validation = Validation()
    try:
        if 'name' not in json and 'done' not in json:
            validation.status = False
            validation.message = "Invalid data."
            return validation
        if 'name' in json and not len(json['name']) > 0:
            validation.status = False
            validation.message = "The item name is too short."
        elif 'done' in json and not json['done'] in ['true', 'false']:
            validation.status = False
            validation.message = "The item completion status should be either 'true' or 'false'."
        else:
            validation.status = True
            validation.message = "Item successfully created!"
        return validation
    except KeyError:
        validation.status = False
        validation.message = "You did not include the item name."
        return validation


def validate_limit_and_offset(limit, offset):
    validation = Validation()
    try:
        if limit is not None and offset is not None:
            limit = int(limit)
            offset = int(offset)
            validation.status = True
        else:
            validation.status = True
    except ValueError:
        validation.status = False
    return validation
