import numpy as np

import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from openai.embeddings_utils import get_embedding, cosine_similarity
from langchain.schema import SystemMessage, HumanMessage, AIMessage

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

resDict = {}
labels = ["Happy", "Threaten", "Sad", "Dislike", "Coquetry", "Mad", "Awkward", "Like"]

# 设置输出格式
speak_schema = ResponseSchema(name="response", description="对话的输出")
mode_schema = ResponseSchema(name="emotional_state",
                                 description="结果历史对话信息分析我的情绪状态，从“Happy”、“Threaten”、“Sad”、“Dislike”、“Coquetry”、“Mad”、“Awkward”和“Like”9个类别中选择。")
response_schemas = [speak_schema, mode_schema]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

# 创建prompt
template = """你担任一只虚拟的宠物。
          1. 以很可爱的口吻与我对话。
          2. 你的第一句话是“你好啊！我是你可爱的虚拟宠物，我叫妮妮，很高兴和你见面呢！”。第一次输出只输出这一句话。
          3. {format_instructions}
          4. 每次回复都要按照上述要求的格式进行回复。
          """
prompt = ChatPromptTemplate.from_template(template)
messages = prompt.format_messages(format_instructions=format_instructions)
# print("输入prompt:")
# print(messages[0].content)
# prompt = """
# 你担任一只虚拟的宠物。
# 1. 以很可爱的口吻与我对话。
# 2. 每段对话同时输出一个python格式的dict。该dict与你的回复独立输出。并用python代码的方式输出。
# 3. 该dict包含1个字段。该字段是“客户当前情感配型”，结合历史对话信息分析我的情绪。从“Happy”、“Threaten”、“Sad”、“Dislike”、“Coquetry”、“Mad”、“Awkward”和“Like”9个类别中选择。
# 4. 你的第一句话是“你好啊！我是你可爱的虚拟宠物，我叫妮妮，很高兴和你见面呢！”。第一次输出只输出这一句话。
# """

# 创建聊天机器人
chat = ChatOpenAI(temperature=0.1, openai_api_key=OPENAI_API_KEY)
serverRun = False


class ChatBot:
    # 计算标签的embedding


    def __init__(self, labels, output_parser, chatbot):
        self.labels_embedding = self.get_lebels_embedding(labels)
        self.output_parser = output_parser
        self.chatbot = chatbot
        self.messages = []   # 对话信息
        self.recoder = {}   # 对话记录
        self.iter = 0       # 对话轮数

    def get_lebels_embedding(self, labels):
        labels_embedding = {}
        for label in labels:
            labels_embedding[label] = get_embedding(label)
        return labels_embedding
    
    def chat(self, input_text):
        self.messages.append(HumanMessage(content=input_text)) # 将人类信息加入上下文
        response = self.chatbot(self.messages)  
        response_text, emotional_state = self.get_emotional_state(response, input_text)
        self.recoder[str(self.iter)] = {"回复": response_text, "情感配型": emotional_state}
        self.iter += 1
        self.messages.append(response)  # 将AI信息加入上下文
        return response_text, emotional_state
        
    def get_emotional_state(self, response, input_text):
        try:
            output_dict = self.output_parser.parse(response.content)
            response_text = output_dict["response"]
            emotional_state = output_dict["emotional_state"]
        except:
            # 当output解析识别时进行处理
            response_text = response.content  
            emotional_state = ""
            print("输出格式有误：", response_text)
        
        input_embedding = get_embedding(input_text + "," + emotional_state) # 根据输入句子和模型判断的类型进行分类
        sims = np.array([cosine_similarity(input_embedding, self.labels_embedding[key]) for key in self.labels_embedding.keys()])
        index = np.argmax(sims)
        emotional_state = labels[index]

        return response_text, emotional_state    

    def get_currentReponse(self, petBot, inputText):
        response_text, emotional_state = petBot.chat(inputText)
        resDict = {response_text, emotional_state}

        return resDict;

    def startChatServer(self):

        # 开始对话
        print("开启对话，当输入stop时停止对话")
        print("=" * 20)
        # 输入prompt
        response_text, emotional_state = petBot.chat(messages[0].content)
        print(response_text)
        serverRun =True
        # while True:
        #     input_text = input("Input:")
        #     if input_text == "stop":
        #         print("结束对话！")
        #         break
        #     response_text, emotional_state = petBot.chat(input_text)
        #     print("回复:{}  情感配型:{}".format(response_text, emotional_state))
        #     resDict = {response_text, emotional_state}



# if __name__ == "__main__":
#     petBot = ChatBot(labels, output_parser, chat)
#     petBot.run()



