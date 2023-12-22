# TunaTemplate

A simplified version of [`gentzkow/template`](https://github.com/gentzkow/template).

In honor of Tuna 🍣 🐈

### Building this repo

```sh
# clone the repo, cd into it
git clone https://github.com/arjunsrini/TunaTemplate
cd TunaTemplate

# load the shmake submodule
git submodule init
git submodule update

# build the project
bash make.sh
```
<!-- 2. At the root of your repo, create a file called `config.yaml` with contents like the file `setup/example_config.yaml`. -->

<!-- or `make` from the root of the repo. To build an a submodule (e.g. `analysis`), type `make` while your current working directory is `your-path-to-repo/analysis`. -->

### Using this as a template

Click `Use this template` to create your own repo. For more info, see [this](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).

### Notes

#### [`shmake`](https://github.com/arjunsrini/shmake)

Included as a git submodule, this is a shell version of [`gslab_make`](https://github.com/gslab-econ/gslab_make).

### License

See [here](https://github.com/arjunsrini/TunaTemplate/blob/main/LICENSE.txt).
