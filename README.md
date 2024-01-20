# Coordinate Canvas

Interactive canvas that allows you to draw 2D coordinates in a plane and output their corresponding coordinates to a JSON file.

> [!NOTE]
> All instructions in this README assume your Python 3.11.6+ installation is in your PATH and is aliased under `python`. If this is not the case, you will need to replace `python` with the alias or path that points to the correct Python executable.

## Installation

```bash
python -m pip install ccanvas  # Use dash instead of underscore!
```

## Usage

You can display the help message by running the following command:

```bash
python -m ccanvas --help  # Use underscore instead of dash!
```

Once the canvas has been opened, you will be able to click on any part of it and add a new coordinate. Lines can be switched using the numeric pad on the keyboard, as explained on the header of the window.

Once you have added all the desired coordinates, just press the "Escape" or "Q" keys or close the window. A JSON file will be generated containing all the coordinates you added. This is how the JSON structure looks like:

```json
{
    "line_1": {
        "x": [
            3.064516129032258,
            5.510752688172044,
            10.45698924731183,
            14.045698924731184,
            ...
        ],
        "y": [
            8.837828837828837,
            13.18015318015318,
            13.126873126873129,
            8.03862803862804,
            ...
        ]
    },
    "line_2": {
        ...
    },
    ...
}
```

### Data retrieval

JSON data can easily be retrieved with a few lines of code.

```python
import json

# Assuming the script is located in the same directory where the program is
#   being executed (if not, modify the path below):
with open("coordinates.json", mode="r", encoding="utf-8") as fp:
    data = json.load(fp)  # Loads all data in a dictionary.

# Ways to retrieve data:
line_1 = data["line_1"]
line_1_x = data["line_1"]["x"]
line_1_y = data["line_1"]["y"]
line_1_xy = [(x, y) for x, y in zip(data["line_1"].values())]  # Recommended!
```

## Contributing

If you are planning on contributing to the repository, take a look at the [contribution guidelines](./CONTRIBUTING.md).
