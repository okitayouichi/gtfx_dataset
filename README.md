# gtfx_dataset: Effect-Applied Guitar Audio Dataset

This is a project for a guitar wet signal dataset consisting of similar performances of three different guitars.
This repository contains a dataset generation program.
This project is a part of the project "fx_estimate".
A dry signal dataset [gt_dataset](https://github.com/okitayouichi/gt_dataset) is required to generate this dataset and this dataset is intended to be used for an audio effect estimation project [dry_cond_fx_estimate](https://github.com/okitayouichi/dry_cond_fx_estimate).

## Dataset Overview

The dataset consists of electric guitar wet signals (i.e. effect-applied audio) and its labels.
A single effect is applied with various parameter settings.
Before the effect is applied, the loudness is normalized to an RMS value of 0.1.
See [gt_dataset](https://github.com/okitayouichi/gt_dataset) for information on dry signals.

## Setup

This program has only been tested on Ubuntu 20.04.6 LTS, and Python 3.11.0.
The root directory of this project (`gtfx_dataset`) must be directly under the root directory of the parent project `fx_estimate`.


First, in the src/ directory, create a file named `.env` with the following content:
```bash
PROJECT_PATH=/path/to/fx_estimate/
```
, where `/path/to/fx_estimate/` should be replaced with the path in your environment.
Then, run the following in command line:
```bash
cd src/
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt 
chmod u+x run.sh
```

## Dataset Generation
```bash
cd src/
./run.sh
```
If you want to delete the old dataset and regenerate it, run the above command with an option `-clean`.
