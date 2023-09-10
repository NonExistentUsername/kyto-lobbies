import inspect


def inject_dependencies(handler: callable, dependencies: dict[str, any]) -> callable:
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)
