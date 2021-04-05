# Blocky
Logic game with cute ducks

![Screenshot](/images/game_screenshot.png)

### Rules

- Ducks ain't that clever. After choosing a direction, they move until they hit the wall. Or something worse.

- They all want to move. No exceptions. Maybe dead ducks.

Hopefully you can help them find the swimming pools they are after.

### Development

Dependencies are in `requirements.txt`.

```bash
# Using pip
pip install -r requirements.txt

# Or using Conda
conda create --name <env_name> --file requirements.txt
```

### Running the game

```bash
PYTHONPATH=. python3 gui/editor.py
```

This will start the editor. From here, you can either create a new map,
open an already existing one, or start the game with `game -> start`.

### Running tests

You need [pytest](https://docs.pytest.org/en/stable/getting-started.html) to do that

```bash
py.test test
```

### License

Project is under MIT license. See `LICENSE` file for details.

