import json
from flask import Flask, request
import prettytable
import traceback

app = Flask(__name__)

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/')
def index():
    return 'API'


@app.route('/get_distribution', methods=['POST'])
def get_distribution():

    try:
        data = json.loads(request.data)
        subjects = data['subjects']

        response_str = ''
        a_global = b_global = c_global = d_global = 0
        questions_number_global = 0

        for subject in subjects:

            subject_name = subject['subject_name']
            answer_keys = subject['answer_keys']
            questions_number_local = len(answer_keys)

            a_local = b_local = c_local = d_local = 0
            for answer_key in answer_keys:
                if answer_key == '1':
                    a_local += 1
                elif answer_key == '2':
                    b_local += 1
                elif answer_key == '3':
                    c_local += 1
                elif answer_key == '4':
                    d_local += 1
                else:
                    questions_number_local -= 1

            a_global += a_local
            b_global += b_local
            c_global += c_local
            d_global += d_local

            questions_number_global += questions_number_local

            table = prettytable.PrettyTable(
                ['n(a)', 'a%', 'n(b)', 'b%', 'n(c)', 'c%', 'n(d)', 'd%'])
            a_per = round((a_local*100)/questions_number_local, 2)
            b_per = round((b_local*100)/questions_number_local, 2)
            c_per = round((c_local*100)/questions_number_local, 2)
            d_per = round((d_local*100)/questions_number_local, 2)

            table.add_row([a_local, a_per, b_local, b_per,
                          c_local, c_per, d_local, d_per])

            response_str += f'Subject Name : {subject_name}\nNumber Of Questions :{questions_number_local}\n'
            response_str += f'{table.get_string()}\n\n\n'

        table = prettytable.PrettyTable(
            ['n(a)', 'a%', 'n(b)', 'b%', 'n(c)', 'c%', 'n(d)', 'd%'])

        a_per = round((a_global*100)/questions_number_global, 2)
        b_per = round((b_global*100)/questions_number_global, 2)
        c_per = round((c_global*100)/questions_number_global, 2)
        d_per = round((d_global*100)/questions_number_global, 2)

        table.add_row([a_global, a_per, b_global, b_per,
                       c_global, c_per, d_global, d_per])

        response_str += f'Overall : \nNumber Of Questions :{questions_number_global}\n'
        response_str += f'{table.get_string()}\n\n\n'

        return {'response': response_str}, 200

    except Exception as e:
        traceback.print_exc()
        return {'message': 'Bad request.'}, 400


if __name__ == '__main__':
    app.run()
