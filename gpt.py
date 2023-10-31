import openai
import time
class GPT:

    def __init__(self) -> None:
        self.key = '' #replace with your OPENAI API KEY.
        openai.api_key = self.key

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
                print("Rate limit reached. Waiting for 1 minute...")
                time.sleep(60)

    def get_manufacturer_details(self, manufacturer:str) -> str:
        prompt="2 lines on {} bike manfacturer include founded year".format(manufacturer)
        msg =self.get_from_gpt(prompt)
        print(msg)
        return msg

if __name__ == "__main__":
    gpt_instance= GPT()
    response=gpt_instance.get_manufacturer_details("Trek")
