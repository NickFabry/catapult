This is my attempt to provide a decent template for python CLI based projects, with the sample name, envy. In order to use this, one should copy this entire directory structure to a new directory, EXCEPT /.venv . The purpose of /.venv is a location to store a python venv; by its nature, it is environment dependent, and thus should not be included in either git repositories or other syncing mechanisms. The .gitignore file excludes the /.venv directory.

So, to set up a new python project in venv, do the following:

- Copy the top level envy directory into your new project directory, or, clone it from the envy git repo.

- If you've cloned it, delete the .git directory so there is no association with the original template.

- Create a new repo in GitHub
(Click Stuff)

- Create a local git repo
echo "# project_name" >> README.md
git init
git add README.md
git commit -m "first commit"

- Now attach and push the git repo
git remote add origin https://github.com/NickFabry/project_name.git
git push -u origin master

The project file part is done. Now, we must set up a venv.

- Create the venv in the directory with the following command:
python -m venv --prompt project_name /path_to_project/project_name/venv

- Activate the virtual environment:
cd /path_to_project/project_name/venv; source bin/activate

- Install dependencies:
pip install pandas

- Put a soft link in bin to your main runner script:
ln -s bin/run_my_script project_name/main.py

- Deactivate the environment
deactivate



Hopefully you're done now!