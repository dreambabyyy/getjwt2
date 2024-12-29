from flask import Flask, request

app = Flask(__name__)
token_list = []
@app.route('/post')
def main():
    global token_list
    token = request.args.get('token')
    token_list.append(token)
    return 'successfull'

@app.route('/get')
def main_():
    global token_list
    if not str(len(token_list)) == "0":
       for get_one in token_list:
           token_list.remove(get_one)
           break
       return str(get_one)
    else:
       return 'None'
@app.route('/total')
def total():
    global token_list
    return f"{token_list} \n\nTotal:  {str(len(token_list))} "
app.run(port=5000)

