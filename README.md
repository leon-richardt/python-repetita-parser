# python-repetita-parser

A Python parser for the data format of the [REPETITA](https://github.com/svissicchio/Repetita) framework.
This module can parse topology and demand files either **separately** or **combine** them into problem instances.
The data can then be accessed via native Python objects.

## Usage
A usage example is provided in [`examples/demand-visualization`](./examples/demand-visualization/demand_visualization.py).
To try it, run the following commands:
```bash
$ cd examples/demand-visualization
$ python -m venv env && source env/bin/activate
$ pip install -r requirements.txt
$ python demand_visualization.py data/DeutscheTelekom.{graph,0000.demands}
```
This will parse and visualize some traffic distribution information about the passed REPETITA instance.


## Installation
Via pip:
```bash
pip install repetita-parser
```


## Data Format
REPETITA defines two file formats, one for topology files and another for demand files.
These formats are defined in the [REPETITA wiki](https://github.com/svissicchio/Repetita/wiki/Adding-Problem-Instances).
