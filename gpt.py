import openai
import time
import logging
class GPT:

    #constructor for GPT
    def __init__(self) -> None:
        FORMAT = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
        logging.basicConfig(filename='./logs/Logs.log',format=FORMAT, level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        OPEN_AI_KEY = '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' #Replace with your OPENAI API KEY 
        openai.api_key = OPEN_AI_KEY

    #function to make an api call to gpt with prompt
    def get_from_gpt(self, prompt, model="gpt-3.5-turbo"):
        while True:
            messages = [{"role": "user", "content": prompt}]
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    temperature=0,
                )
                return response.choices[0].message["content"]
            #GPT has an api call limit of 3 per minute.
            except openai.error.RateLimitError as e:
                self.logger.warning("Rate limit reached. Waiting for 1 minute...")                
                time.sleep(60) #wait for 60 seconds if limit reached
            except response.exceptions.RequestException as e:
                self.logger.error("Error while fetching manufacturer details from GPT: %s", e) 

    #function to get manufacturer details from GPT
    def get_manufacturer_details(self, manufacturer:str) -> str:
        prompt="2 lines on {} bike manfacturer include founded year".format(manufacturer)
        msg =self.get_from_gpt(prompt)
        print(msg)
        return msg

if __name__ == "__main__":
    gpt_instance= GPT()
    response=gpt_instance.get_manufacturer_details("Trek")
