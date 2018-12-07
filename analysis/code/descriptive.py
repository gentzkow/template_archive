import git

repo = git.Repo('.', search_parent_directories=True)
print(repo.working_tree_dir)