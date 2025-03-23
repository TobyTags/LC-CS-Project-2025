from flask import Flask, render_template, jsonify, send_from_directory, request, redirect, url_for
import os # this allows me to create new directories (folders) to save files and graphs to
import shutil #this is for deleting data

#importing functions from different python files here
import Python.Parse as Parse
import Python.GraphGeneration as GraphGeneration

from Python.OverAllGraphsGeneration import main3
from Python.StateGraphs import StateGraphs
from Python.DataBaseSave import CSV_Save


app = Flask(__name__) 

# Path to the folder containing the saved graphs
GRAPH_FOLDER = os.path.join(os.getcwd(), 'graphs')
app.config['GRAPH_FOLDER'] = GRAPH_FOLDER

@app.route('/')
def index():
    # this creates the graphs folder if it does not already exist
    graphs_dir = os.path.join(app.root_path, 'graphs')
    if not os.path.exists(graphs_dir):
        os.makedirs(graphs_dir, exist_ok=True)

    # this creates the CleanedData folder if it does not already exist
    graphs_dir = os.path.join(app.root_path, 'CleanedData')
    if not os.path.exists(graphs_dir):
        os.makedirs(graphs_dir, exist_ok=True)

    # List all .jpg images in the graphs directory - this allows the index page to load the graphs
    image_files = [f for f in os.listdir(GRAPH_FOLDER) if f.endswith('.jpg')]
    return render_template('index.html', images=image_files)

@app.route('/run-scripts', methods=['POST'])
def run_scripts():
    try:
        # Run the Python scripts
        Parse.main1()
        GraphGeneration.main2()

        # Fetch the images from the graphs folder
        image_files = [f for f in os.listdir(GRAPH_FOLDER) if f.endswith('.jpg')]

        return jsonify({
            "message": "Scripts executed successfully!",
            "images": [f"/graphs/{img}" for img in image_files]
        })

    except Exception as e:
        return jsonify({
            "message": "Scripts executed successfully!",
            "images": [f"/graphs/{img}" for img in image_files]
        })


@app.route('/graphs/<path:filename>')
def get_image(filename):
    return send_from_directory(app.config['GRAPH_FOLDER'], filename)


@app.route('/process_variable')
def process_variable():
    state = request.args.get('variable')
    print("Received state:", state)

    # generates the graphs for the given state
    StateGraphs(state)
    
    # Redirect to the state page using the correct endpoint name
    return redirect(url_for('state_page', state=state))

@app.route('/graphs/<path:filename>')
def graphs(filename):

    return send_from_directory(os.path.join(app.root_path, 'graphs'), filename)


@app.route('/state/<state>')
def state_page(state):

    #this allows all of the different pages for each state use the same html file, it does this by passing the html file the name of the state based on whatever US state that it needs to be.
    return render_template('StateDataPages/state.html', state=state)

@app.route('/OverallGraphs')
def OverallGraphs():
    return render_template('OverallGraphs/OverallGraphs.html')


@app.route('/run_overall_graphs')
def run_overall_graphs():
    
    print("calling main 3")
    main3()

    return jsonify(status='success')



@app.route('/delete_data')
def delete_data():
    try:
        # Delete the CleanedData folder if it exists
        cleaned_data_dir = "CleanedData"
        if os.path.exists(cleaned_data_dir):
            shutil.rmtree(cleaned_data_dir)
        
        # Delete the graphs folder if it exists
        graphs_dir = "graphs"
        if os.path.exists(graphs_dir):
            shutil.rmtree(graphs_dir)
        
        return jsonify({"status": "success", "message": "CleanedData and graphs folders deleted."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



@app.route('/DataTracker')
def DataTracker():

    #this var "cleaned_data_exists" is set to true or false based on weather the file 'processed_hcny_all_tables.csv' is actauly there
    cleaned_data_exists = os.path.exists("CleanedData/processed_hcny_all_tables.csv")
    
    # this returns the result. (Either true or false)
    return jsonify({"Data": cleaned_data_exists})


#this is for getting the data from the html form, and giving it to the python script that will add it it the local database (im using a csv file)
@app.route('/DataBase', methods=['POST'])
def DataBase():
    try:

        data = request.get_json()  # fetching the data sent from the javascript call

        CSV_Save(data)
        
        return jsonify({'message': 'Data successfully saved!'})
    except Exception as e:
        return jsonify({'error': str(e)})

    

if __name__ == '__main__':
    app.run(debug=True)
