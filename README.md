## RASA-AI-AGENT-CHALLENGE

Based on RASAS Quickstart project. Find here: 


**Set Up Environment:**
   - In the codespace, open the `.env` file from this repo and add your license key to that file.
     ```
     RASA_PRO_LICENSE='your_rasa_pro_license_key_here'
     ```
   - Set this environment variables by running 
     ```
     source .env
     ```
   - Activate your python environment by running
     ```
     source .venv/bin/activate
     ```

 **Train the Model:**
   - In the terminal, run:
     ```
     rasa train
     ```

**Talk to your Bot:**
   - In the terminal, run
     ```
     rasa inspect
     ```
     GitHub will show a notification, click on the green button to view the inspector where you can chat with your assistant.

c**Run Custom Actions:**
  In Rasa 3.10 and later, custom actions are automatically run as part of your running assistant. To double-check that this is set up correctly, ensure that your `endpoints.yml` file contains the following configuration:
   ```
   action_endpoint:
      actions_module: "actions" # path to your actions package
    ```
   Then re-run your assistant via `rasa inspect` every time you make changes to your custom actions.
