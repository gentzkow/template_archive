# GentzkowLabTemplate

### Requirements

The following are required to run the base template:
* Python 3.x
* LaTex

The template assumes that Python 3.x is installed and your 
Python executable is `python3`. If not, the setup script will produce
an error and prompt you to update `local_env.sh` with the correct
name of your Python executable.

### Setup

```sh
# Clone the repo, cd into it
git clone https://github.com/gentzkow/GentzkowLabTemplate
cd GentzkowLabTemplate

# Run setup script to create local settings file local_env.sh,
# and check that local executables are correctly installed.
bash setup.sh

# Run the `make.sh` script at the root of the repository to 
# check that the template runs without error
bash make.sh
```

### Using this as a template

To create a new repository from this t

Click `Use this template` to create your own repo. For more info, see [this](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).

### License

See [here](https://github.com/arjunsrini/TunaTemplate/blob/main/LICENSE.txt).
