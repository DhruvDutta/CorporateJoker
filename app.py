from flask import Flask,render_template, request,Response
import json
import torch
import openai,uuid
import pandas as pd
import numpy as np
app=Flask(__name__)

def set_openai_key(key):
    openai.api_key = key
    
class Example:
    def __init__(self, inp, out):
        self.input = inp
        self.output = out
        self.id = uuid.uuid4().hex

    def get_input(self):
        return self.input

    def get_output(self):
        return self.output

    def get_id(self):
        return self.id

    def as_dict(self):
        return {
            "input": self.get_input(),
            "output": self.get_output(),
            "id": self.get_id(),
        }


class GPT:
    def __init__(self,
                 engine='davinci',
                 temperature=0.5,
                 max_tokens=100,
                 input_prefix="input: ",
                 input_suffix="\n",
                 output_prefix="",
                 output_suffix="",
                 append_output_prefix_to_query=False):
        self.examples = {}
        self.engine = engine
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.input_prefix = input_prefix
        self.input_suffix = input_suffix
        self.output_prefix = output_prefix
        self.output_suffix = output_suffix
        self.append_output_prefix_to_query = append_output_prefix_to_query
        self.stop = (output_suffix + input_prefix).strip()

    def add_example(self, ex):
        assert isinstance(ex, Example), "Please create an Example object."
        self.examples[ex.get_id()] = ex

    def delete_example(self, id):
        if id in self.examples:
            del self.examples[id]

    def get_example(self, id):
        return self.examples.get(id, None)

    def get_all_examples(self):
        return {k: v.as_dict() for k, v in self.examples.items()}

    def get_prime_text(self):
        return "".join(
            [self.format_example(ex) for ex in self.examples.values()])

    def get_engine(self):
        return self.engine

    def get_temperature(self):
        return self.temperature

    def get_max_tokens(self):
        return self.max_tokens

    def craft_query(self, prompt):
        q = self.get_prime_text(
        ) + self.input_prefix + prompt + self.input_suffix
        if self.append_output_prefix_to_query:
            q = q + self.output_prefix
        return q

    def submit_request(self, prompt):
        response = openai.Completion.create(engine=self.get_engine(),
                                            prompt=self.craft_query(prompt),
                                            max_tokens=self.get_max_tokens(),
                                            temperature=self.get_temperature(),
                                            top_p=1,
                                            n=1,
                                            stream=False,
                                            stop=self.stop)
        return response

    def get_top_reply(self, prompt):
        response = self.submit_request(prompt)
        return response['choices'][0]['text']

    def format_example(self, ex):
        return self.input_prefix + ex.get_input(
        ) + self.input_suffix + self.output_prefix + ex.get_output(
        ) + self.output_suffix

openai.api_key = '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'
jokes = pd.read_csv('static/jokes.csv')


@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        text=request.get_data()
        text = text.decode(encoding="utf-8")
        text = text[5:]
        
        print(text)
        if text == 'random':
            rand = np.random.randint(0,high=len(jokes),size=1)
            ques = jokes['Question'][rand[0]]
            model = torch.load("static/jokePredictor")
            output = model.submit_request(ques)
            response={'output':ques+" : "+output.choices[0].text}
            return Response(json.dumps( response ))
        else:
            model = torch.load("static/jokePredictor")
            output = model.submit_request(text)
            output=output.choices[0].text
            response={'output':output}
            return Response(json.dumps( response ))
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
        
        
