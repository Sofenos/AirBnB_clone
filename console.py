#!/usr/bin/python3

"""AirBnB Clone - Command Line """

import cmd
from models.place import Place
from models.review import Review
from models import storage
from models.state import State
from models.base_model import BaseModel
from models.city import City
from models.amenity import Amenity
from models.user import User

import json
import shlex


class HBNBCommand(cmd.Cmd):
    """ Holberton command prompt to access models data """
    prompt = '(hbnb) '
    class_names = {
        "BaseModel": BaseModel,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "User": User,
        "Review": Review
    }

    def default(self, arg):
        """
        Called on an input line when the command prefix is not recognized.
        If this method is not overridden
        """
        methods_dict = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update
        }
        commands = arg.strip().split(".")
        if len(commands) != 2:
            cmd.Cmd.default(self, arg)
            return
        class_name = commands[0]
        command = commands[1].split("(")[0]
        line = ""
        if (command == "update" and commands[1].split("(")[1][-2] == "}"):
            data_inputs = commands[1].split("(")[1].split(",", 1)
            data_inputs[0] = shlex.split(data_inputs[0])[0]
            line = "".join(data_inputs)[0:-1]
            line = class_name + " " + line
            self.do_update_using_class(line.strip())
            return
        try:
            data_inputs = commands[1].split("(")[1].split(",")
            for n in range(len(data_inputs)):
                if (n != len(data_inputs) - 1):
                    line = line + " " + shlex.split(data_inputs[n])[0]
                else:
                    line = line + " " + shlex.split(data_inputs[n][0:-1])[0]
        except IndexError:
            data_inputs = ""
            line = ""
        line = class_name + line
        if (command in methods_dict.keys()):
            methods_dict[command](line.strip())

    def do_quit(self, arg):
        """
        Quit command to exit the program

        Usage: quit

        Return:
            True
        """
        return True

    def do_EOF(self, arg):
        """
        EOF command to exit the program when the user inputs EOF (Ctrl+D)

        Usage: EOF or CTRL+D

        Return:
            True
        """
        print("")
        return True

    def emptyline(self):
        """
        Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        Return:
            None
        """
        pass

    def do_nothing(self, arg):
        """ Does nothing """
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it (to the JSON file)
        and prints the id

        Usage: create <class name>

        Args:
            arg (str): class name of the instance to create

        Return:
            None
        """
        if not arg:
            print("** class name missing **")
            return
        line = shlex.split(arg)
        if line[0] not in HBNBCommand.class_names.keys():
            print("** class doesn't exist **")
            return
        new_inst = HBNBCommand.class_names[line[0]]()
        new_inst.save()
        print(new_inst.id)

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id (save the change
        into the JSON file)

        Usage: destroy <class name> <id>

        Args:
            arg (str): class name and id of the instance to destroy

        Return:
            None
        """
        args_command = shlex.split(arg)
        if len(args_command) == 0:
            print("** class name missing **")
            return
        if args_command[0] not in HBNBCommand.class_names.keys():
            print("** class doesn't exist **")
            return
        if len(args_command) <= 1:
            print("** instance id missing **")
            return
        inst_dicts = storage.all()
        key = "{}.{}".format(args_command[0], args_command[1])
        if key in inst_dicts:
            del inst_dicts[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_show(self, arg):
        """
        Prints the string representation of an instance based on the class
        name and id

        Usage: show <class name> <id>

        Return:
            None
        """
        args_command = shlex.split(arg)
        if len(args_command) == 0:
            print("** class name missing **")
            return
        if args_command[0] not in HBNBCommand.class_names.keys():
            print("** class doesn't exist **")
            return
        if len(args_command) <= 1:
            print("** instance id missing **")
            return
        inst_dicts = storage.all()
        key = "{}.{}".format(args_command[0], args_command[1])
        if key in inst_dicts:
            obj_instance = str(inst_dicts[key])
            print(obj_instance)
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """
        Prints all string representation of all instances based or not on the
        class name

        Usage: all 

        Args:
            arg (str): class name of the instance to show or nothing
        """
        data_json = []
        inst_dicts = storage.all()
        if not arg:
            for key in inst_dicts:
                data_json.append(str(inst_dicts[key]))
            print(json.dumps(data_json))
            return
        command_arg = shlex.split(arg)
        if command_arg[0] in HBNBCommand.class_names.keys():
            for key in inst_dicts:
                if command_arg[0] in key:
                    data_json.append(str(inst_dicts[key]))
            print(json.dumps(data_json))
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file)

        Usage: update <class name> <id> <attribute name> "<attribute value>"

        Args:
            arg (str): class name, id, attribute name and attribute value of
            the instance to update
        """
        if not arg:
            print("** class name missing **")
            return
        arg_command = shlex.split(arg)
        insts_dicts = storage.all()
        if arg_command[0] not in HBNBCommand.class_names.keys():
            print("** class doesn't exist **")
            return
        if (len(arg_command) == 1):
            print("** instance id missing **")
            return
        try:
            key = arg_command[0] + "." + arg_command[1]
            insts_dicts[key]
        except KeyError:
            print("** no instance found **")
            return
        if (len(arg_command) == 2):
            print("** attribute name missing **")
            return
        if (len(arg_command) == 3):
            print("** value missing **")
            return
        inst = insts_dicts[key]
        if hasattr(inst, arg_command[2]):
            data_type = type(getattr(inst, arg_command[2]))
            setattr(inst, arg_command[2], data_type(arg_command[3]))
        else:
            setattr(inst, arg_command[2], arg_command[3])
        storage.save()

    def do_update_using_class(self, arg):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute 
        """
        if not arg:
            print("** class name missing **")
            return
        data_dictionary = "{" + arg.split("{")[1]
        data_arg = shlex.split(arg)
        objs_dict = storage.all()
        if data_arg[0] not in HBNBCommand.class_names.keys():
            print("** class doesn't exist **")
            return
        if (len(data_arg) == 1):
            print("** instance id missing **")
            return
        try:
            key = data_arg[0] + "." + data_arg[1]
            objs_dict[key]
        except KeyError:
            print("** no instance found **")
            return
        if (data_dictionary == "{"):
            print("** attribute name missing **")
            return

        data_dictionary = data_dictionary.replace("\'", "\"")
        data_dictionary = json.loads(data_dictionary)
        inst = objs_dict[key]
        for my_key in data_dictionary:
            if hasattr(inst, my_key):
                data_type = type(getattr(inst, my_key))
                setattr(inst, my_key, data_dictionary[my_key])
            else:
                setattr(inst, my_key, data_dictionary[my_key])
        storage.save()

    def do_count(self, arg):
        """
        Retrieve the number of instances of a class

        Usage: <class name>.count()


        """
        counter = 0
        objects_dict = storage.all()
        for key in objects_dict:
            if (arg in key):
                counter += 1
        print(counter)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
