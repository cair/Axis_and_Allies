This is the first release of Axis and Allies engine.

Some notes about the current release:

The board, has to be a square (nxm) and it has to be divisible with the number of nations. (6x5 / 2 = 15 tiles each)  
Units are not allowed to move diagonally.  
Only infantry and tanks are implemented.  
No water tiles.  
No technologies included.  
No purchase of industry.  

# Install
```bash
pip install git+https://github.com/cair/Axis_and_Allies.git
```

# Running Examples
```bash
python -m axis_and_allies.demostration_game
python -m axis_and_allies.example
```

# Tournament Web Interface
The tournament web interface features a small `tornado` driven web app, that feature the following:
* Create unique submission id for each bot
* Submission files can be deleted (python only, or full submission)
* Multi-File upload
* Dynamic loading of your bot class (Configured during the manifest setup)

## Submitting
1. Visit the website at `http://<host-url>:8889/#!/upload`
2. Enter your submission id. If none exists, click `Generate Upload ID`
3. Click `Select files` in the file upload pane
4. Select your bot-files, and click `OK (submit)`
5. Edit the manifest using the text-area field.
    * entrypoint: The filename of the bot class
    * class_name: Name of the class inside `entrypoint`
    * class_arguments: dictionary of parameters sent to the class constructor
    * project_name: Your project name
    * email: Your email
    * version: Your bot version
    * author: Your name
6. Click `Save Manifest` to save the edited manifest
7. Now, you can run your bot in the tournament. The tournamnet wil appear at the bottom when all matches is completed.

## Edit a Submission
1. Enter the previously generated submission id
2. Your submission should now be loaded and you can do necessary changes.
3. You can delete all python files in the submission by clicking `Delete Python Files`
4. You can delete the submission by clicking `Delete Submission`  