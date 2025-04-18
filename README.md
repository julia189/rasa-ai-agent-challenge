## RASA-AI-AGENT-CHALLENGE

This project is created for the RASA AI Agent Challenge 2024. 

### Use Cases:
- Find doctos and book appointments
- Query knowledge database 
- Find purchase best equipment 
- Connect to Baby tracker App and get latest information health, sleep time, feeding times
- Summarize videos on baby equipment, positive birthing stories

<img src="documentation/images/BabyAIAgent.png?raw=true">

**Set Up Environment:**
   - Create a `.env` file. Add the ```RASA_PRO_LICENSE``` and the following API Keys to the file:
      ```
      RASA_PRO_LICENSE='your_rasa_pro_license_key_here'
      OPENAI_API_KEY='your OPEN AI Key here'
      GOOGLE_API_KEY='your google API key here'
      YOUTUBE_API_KEY='your google API key here'
      SEARCH_ENGINE_ID='your search engine id here'
      OXYLABS_USERNAME='your oxylab username'
      OXYLABS_PASSWORD='your oxylab password'
     ```
   - Set these environment variables by running 
     ```
     source .env
     ```
   - Create and activate your python environment by running
     ```
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - Install the requirements by running
     ```
     pip install -r requirements.txt
     ```
 **RASA Commands:**
   - 
     ```
     rasa train  #trains the model
     rasa inspect, rasa inspect --debug #runs the inspector
     rasa run actions # runs the actions 
     ```

**Run Custom Actions:**
  In Rasa 3.10 and later, custom actions are automatically run as part of your running assistant. To double-check that this is set up correctly, ensure that your `endpoints.yml` file contains the following configuration:
   ```
   action_endpoint:
      actions_module: "actions" # path to your actions package
    ```
   Then re-run your assistant via `rasa inspect` every time you make changes to your custom actions.
