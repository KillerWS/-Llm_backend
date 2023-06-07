# Import flask and datetime module for showing date and time
from flask import Flask,request
import datetime
from flask_cors import CORS, cross_origin
from sentiment_analysis import resDict, ChatBot, labels, output_parser, chat, messages

x = datetime.datetime.now()

app = Flask(__name__)
#设置cors跨域请求
CORS(app, resources={r"/api/*": {"origins": "*"}})


#初始化数据结构
reponseData={'response_text': '', 'emotional_state': ''}

# Route for seeing a data
@app.route('/data', methods=['POST'])
@cross_origin()
def get_time():
    # Returning an api for showing in  reactjs
    return {
        'Name': "geek",
        "Age": "22",
        "Date": x,
        "programming": "python"
    }


#测试路由
@app.route('/test')
def testRoute():
    return {
        'Name': "geek",
        "Age": "22",
        "Date": x,
        "programming": "python"
    }
@app.route('/api/pet', methods=['POST'])
@cross_origin()
def get_reponseMessage():
    #处理json数据
    userInput = request.json['currentMessage']
    response_text, emotional_state = petBot.chat(userInput);
    reponseData['response_text'] = response_text
    reponseData['emotional_state'] = emotional_state
    return {
        'response_text': response_text,
        'emotional_state': emotional_state,
        'rawData':userInput
    }

# Running app
if __name__ == '__main__':
    # 启动聊天机器人
    petBot = ChatBot(labels, output_parser, chat)
    response_text, emotional_state = petBot.chat(messages[0].content)
    app.run(debug=True)



