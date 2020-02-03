# Guide
Graphical User Interface for dot env files. 

Visual Interface for interacting with config. The idea was hatched to solve issues found making flask, django and other apps following the 7 factor guidelines. 

## QuickStart

Install the library.
`pip install guide`

Let the library create your config.py file 
`genv new`

The library assumes the directory you are in is the project root and where the `.env` will be located.
Todo: how to specify where the config file should be?

What we get is a decorator so we can set what configs are required. 
``` 
import guide

@guide.config(required=True)
def get_project_root() -> Path:
    return Path(__dir__)


def validate_project_root() -> None:
    result = get_project_root()
    if result is None:
        raise NotConfiguredCorrectly(f'Project Root not set')

```

What we really gets is a graphical user interface for our .env files. I always forget something when setting these so this helps fix that. 

`guide`

Todo: pictures of GUI

When saving, all the Validators are ran making sure they pass allowing for quick feedback. 

Todo: picture of GUI when Validators does not pass

You also get a view of the readme

Todo: pictures of GUI

Or tell the library where the `config.py` file is. 

