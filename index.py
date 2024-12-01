from flask import Flask, request, render_template, send_file, make_response
import requests
from urllib.parse import urlparse
import json
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        # Extract the workflow ID from the URL
        workflow_id = url
        # Prepare the payload
        payload = {'workflow_id': workflow_id}
        # Make the POST request
        response = requests.post('https://www.comfyonline.app/api/query_workflow_detail_public', data=payload)
        # Extract the workflow data
        json_data = response.json()
        success = json_data['success']
        print(success)
        if not success:
            return make_response({
                'message': 'Couldnt fetch the workflow. Please check the URL and try again.',
                'what_to_do': 'Press the back button and try again.',
                'full_response': json_data

            }, 400)


        workflow_workflow = json_data['data']['workflow_data']['workflow_workflow']
        # If workflow_workflow is a string, parse it
        if isinstance(workflow_workflow, str):
            workflow_workflow = json.loads(workflow_workflow)
        # Convert to JSON string without extra quotes
        json_str = json.dumps(workflow_workflow, indent=4)
        # Send the JSON file for download
        return send_file(
            io.BytesIO(json_str.encode('utf-8')),
            mimetype='application/json',
            as_attachment=True,
            download_name=json_data['data']['workflow_data']['workflow_title']+'.json'
        )
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)