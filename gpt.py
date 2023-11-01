import openai
import time
import logging
class GPT:

    def __init__(self) -> None:
        FORMAT = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
        logging.basicConfig(filename='./logs/Logs.log',format=FORMAT, level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        OPEN_AI_KEY = '' #Replace with your APIKEY 
        openai.api_key = OPEN_AI_KEY

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
            except openai.error.RateLimitError as e:
                self.logger.warning("Rate limit reached. Waiting for 1 minute...")                
                time.sleep(60)
            except response.exceptions.RequestException as e:
                self.logger.error("Error while fetching manufacturer details from GPT: %s", e) 

    def get_manufacturer_details(self, manufacturer:str) -> str:
        prompt="2 lines on {} bike manfacturer include founded year".format(manufacturer)
        msg =self.get_from_gpt(prompt)
        print(msg)
        return msg

if __name__ == "__main__":
    gpt_instance= GPT()
    response=gpt_instance.get_manufacturer_details("Trek")
