import inspect


class _InitializeArguments:
    def __init__(self, function, **kwargs):
        self.function = function
        self.init_arguments = kwargs


    @property
    def arguments(self):
        sig_values = list(inspect.signature(self.function).parameters.values())
        return sig_values


    def __call__(self, *args, **kwargs):
        # Default arguments to None
        input_args = {k.name: None for k in self.arguments}

        # Build input keyword arguments
        for arg_value, arg in zip(args, self.arguments):
            input_args[arg.name] = arg.default(arg_value) if arg.default not in [arg.empty, None] else arg_value
        
        for arg_name, arg_value, arg in zip(kwargs.items(), kwargs.values(), self.arguments):
            input_args[arg_name] = arg.default(arg_value) if arg.default not in [arg.empty, None] else arg_value

        # Call the function
        return self.function(**input_args)


def InitializeArguments(**kwargs):
    def wrapper(function):
        return _InitializeArguments(function, **kwargs)
    return wrapper