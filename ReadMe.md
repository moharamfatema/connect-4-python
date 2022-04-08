# Connect 4

## Project folder structure:

```
|_ src
    |_main.py
    |_model
    |   |_agent.py
    |   |_grid.py
    |   |_state
    |       |_state.py
    |       |_integer_state.py
    |       |_string_state.py
    |_view
    |   |_game.py
    |_img
```

## Requirements and Running the code

This code was tested on windows inside a python3 virtual environment (venv). To visualize the tree, `pydot` needs to be installed on the system and added to PATH in the envisronment variables.

To run the code, navigate to the root folder (that contains `src` and `out`) and run:

```bash
.\env\Scripts\activate
pip install -r requirements.txt
py .\src\main.py
```