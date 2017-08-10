Tulsa Public Schools
====================
DSSG is working with Tulsa Public Schools to identify students who will not be on grade-level reading proficiency by end of third grade. Read more about the project <a href="https://dssg.uchicago.edu/2016/07/19/tulsa-public-schools/">here</a>.


Project Manager: Chad Kenney

Technical Mentors: Ali Vanderveld, Kevin Wilson

Fellows: Monica Alexander, Charlotte Huang, Max Klein



Setup
=================
## Git repository

To clone this git repository, type the following into the terminal:

```
pip install git+ssh://git@github.com/dssg/tulsa.git
```

This should clone the repository and include downloading any Python requirements necessary.

## Database credentials

Next, database configuration files need to be set up in the `/tulsa/configs` folder <a href="https://github.com/dssg/tulsa/tree/master/configs">here</a>. Database credentials should be populated into the .example files, in both JSON and default_profile format. 

## ETL

In `/tulsa/tulsa/etl` folder, `Drakefile` (<a href="https://github.com/dssg/tulsa/blob/master/tulsa/etl/Drakefile">here</a>) is responsible for running the ETL process end-to-end. There are a few environment variables that need to be set like this:
```
ENVPYTHON = /path/to/python
DBCREDS = /tulsa/configs/dbcreds.json
DBDEFAULTPROFILE = /tulsa/configs/default_profile
ETLDIR = /tulsa/tulsa/etl
MAPCORRECTIONS = /tulsa/configs/map_corrections.json
STATEDIR = /path/to/Drake/state
```
Once set up, `Drakefile` should run and populate the specified database with clean data, based on the original datasets. 

## Model parameters

Before running the model, the learn parameters (such as labels, feature groups, and methods) should be specified. There is an example JSON file in the `tulsa/configs` folder <a href="https://github.com/dssg/tulsa/blob/master/configs/learn_params.json">here</a>.

## Command line interface

Once ready to run, `/tulsa/tulsa/learn/cli_hypervisor.py` should be run with these arguments:
```
Usage: cli_hypervisor.py [OPTIONS] DBCREDS PARAMS_FILE

Options:
  --log-level TEXT       set to "info" to avoid debugging information
  --log-location TEXT    location to store log
  --state-location TEXT  location to store state_file keeping track of run
                         numbers
                         usually where drake is doing this too
  --run-name TEXT        the name to give this run, will be suffixed with a
                         unique id too
  --regenerate           regenerate label and features, not read from Database
  --report               save reports to CSVs after modeling
  --help                 Show this message and exit.
```
  
An example of running the command line script might be the following:

```
python tulsa/tulsa/learn/cli_hypervisor.py tulsa/configs/dbcreds.json tulsa/configs/learn_params.json --log-level debug --log-location=/path/to/logs/tulsa_model.log --run-name run1 --regenerate --report
```


Data Pipeline
=============
Once the environment is set up, changes can be made to the pipeline. 

## New datasets

Filenames that are to be uploaded must be specified in `tulsa/configs/file_to_table_name.json` (<a href="https://github.com/dssg/tulsa/blob/master/configs/file_to_table_name.json">here</a>), mapped to what the table name in the database should be. If there is an Excel file to be uploaded, the end-result table name will be the sheet name appended onto what's specified in this JSON file (e.g. an Excel file mapped to "table_name" would be named "table_name_sheet1" in the table). Files should be added to the data directory.

With every new dataset, there should also be an associated cleanup script added to `tulsa/tulsa/etl/Drakefile`. Once done, Drake can run and will be able to upload all specified datasets from the data directory into the `raw_data` schema of a Postgres database. From there, the cleanup script should clean the raw data and upload to the `clean_data` schema. 

##Label/feature generation

Generating labels or features are done in the `tulsa/tulsa/learn/features.py` <a href="https://github.com/dssg/tulsa/blob/master/tulsa/learn/features.py">file</a>. Each label/feature must have an associated function and be mapped in the `feat_fun` dictionary at the end of the file. Additionally, labels and features should have a specified imputation strategy mapping in `imp_fun` dictionary in the `tulsa/tulsa/learn/prepare.py` <a href="https://github.com/dssg/tulsa/blob/master/tulsa/learn/prepare.py">file</a>. If adding a feature, it must also be added to the feature group dictionary in the `tulsa/tulsa/learn/feature_groups.py` <a href="https://github.com/dssg/tulsa/blob/master/tulsa/learn/feature_groups.py">file</a> in order to be referenced from the parameters file. 

## Results

The results of models will be written to the `results` schema. Specific standard metrics in the model parameters file will be written to `results.results` table. Feature importance, cross-tab metrics, and y prediction probabilities are written after every model run. Feature importance is written to `results.feat_imp` table. Cross-tab metrics are written to `results.feat_crosstab` table. Predicted probabilities for students are written to the `results.y_preds` table. 


## How to add Labels and Features:
### Add a label
In order to make a new label:
+ make a function that accepts a database engine connection, and returns a student-term dataframe and a column of labels.
+ this student-term dataframe is the basis of the contract for features. they all must be perfectly aligned so they could be column concatenated on the right to the labels which are in the order of the stu-term df.
+ add the label name and the funaction that makes the label to the constant `feat_fun` dictionary in `features.py`.
+ you must create a blank table `features.[column_name]`. Hopefully in the future you can auto-create this table.

### Add a feature

+ make entries in
  + `features.py` - how to make the feature
    + this is a function that accept a `db engine` and returns a column -- exactly 1 column -- that is perfectly aligned with the stuterm dataframe that it accepts as an argument
  + `feature_groups.py` -- which groups it belongs to
    + a list of n many groups. the params file specifices which groups will be used. 
  + `prepare.py` -- a NaN imputation strategy
    + how to fill NaN's typical choices are `impute_zeros` (fill zeros) and `impute_iden` (do nothing), and `impute_mean` (take the mean of other values). If you have a categorical variable that needs dummifying use `cat_binarizer` (which will take care of that).


## Architcture choices I'd make differently if I did it again.
+ `results_list` gets returned from `fit_model_and_metrics`, but later on we switched to returning DataFrame from `fit_model_and_metrics` and our metrics results would be more elegantly handled this way.
+ to keep track of `run_name`s we touch a file in the `state_dir` but if I didn't code that part late at night, I would have had a table in postgres keep track of it.
+ `cli_hypervisor.py` takes arguments from both a json params file, and commandline arguments. Two different locations to keep track of. Maybe reading everything from file would be easier. Plus I might switch to yaml for readablity.
