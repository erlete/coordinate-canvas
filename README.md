# Coordinate Canvas

Interactive canvas that allows the user to draw 2D points in a grid and output their corresponding coordinates to a JSON file.

## Installation

This repository uses the [matplotlib's event handlers](https://matplotlib.org/stable/users/explain/event_handling.html), as well as working [Git](https://git-scm.com/) and [Python](https://www.python.org/) clients.

_This installation tutorial assumes that the user's Git and Python clients are linked to the `git` and `python3` aliases, respectively._

### macOS / UNIX

```bash
# Make sure to move to a valid working directory!
git clone https://github.com/erlete/coordinate-canvas

# Virtual environment creation and activation (optional):
python3 -m venv .venv
source ./.venv/bin/activate

# Dependency installation:
python3 -m pip install matplotlib

# Program execution:
python3 main.py
```

### Windows

```cmd
:: Make sure to move to a valid working directory!
git clone https://github.com/erlete/coordinate-canvas

:: Dependency installation:
python3 -m pip install matplotlib

:: Program execution:
python3 main.py
```

## Usage

Having executed the `main.py` file, the user will be prompted for three parameters:

 - **Width**: the width of the canvas.
 - **Height**: the height of the canvas.
 - **Number of lines**: the amount of lines to draw.
 
Once said parameters are set, a `matplotlib` window will appear on screen. The user must now click on it in order to add a point to the canvas. When all points are set, the user must close the window so that the next one can appear.

This process will repeat as many times as specified in the "Number of lines" parameter declared at the beginning.

---

![1](https://user-images.githubusercontent.com/76848729/192160411-06671e46-7b84-4b53-958f-a2af7d56b21e.png)

---

![2](https://user-images.githubusercontent.com/76848729/192160414-ac5f9659-617d-4472-b952-4500849e4929.png)

---

Finally, a `coordinates.json` file will be created on the directory from which the script was executed. It will contain the `x` and `y` coordinates of every point drawn, indexed by the line number of the corresponding step:

```json
{
    "line_1": {
        "x": [
            2.782258064516129,
            5.624999999999999,
            8.850806451612904,
            13.548387096774192,
            15.786290322580644,
            16.491935483870968,
            15.181451612903224,
            12.399193548387096,
            8.830645161290324,
            6.108870967741935
        ],
        "y": [
            7.58141719198743,
            18.364792370355655,
            22.808193197622966,
            23.404259162256384,
            18.581543630222352,
            11.645503314488018,
            5.522280223253799,
            4.059209219153588,
            4.384336108953634,
            6.497660892653939
        ]
    },
    "line_2": {
        "x": [
            5.221774193548387,
            8.286290322580644,
            11.370967741935484,
            13.8508064516129,
            14.45564516129032,
            13.245967741935484,
            10.866935483870968,
            8.346774193548388,
            18.024193548387096
        ],
        "y": [
            10.561747015154527,
            17.55197514585554,
            19.827863374455866,
            19.827863374455866,
            11.157812979787945,
            6.931163412387336,
            7.743980636887453,
            8.936112566154293,
            9.261239455954339
        ]
    }
}
```

## Troubleshooting

This program does not always work with Visual Studio Code integrated shell. It can detect and handle events, yet it will be unable to represent drawn points on the canvas. It is highly recommended to execute the program in a native shell, such as bash, zsh or Windows command prompt.
