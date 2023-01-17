from flask import Flask
from kubernetes import client, config
from modules.labels_finder import LabelsFinder
from blueprints.pods_labels_blueprint import create_plods_labels_blueprint


scan_labels = [{'product': 'Attenti'},{'status': 'unhealthy'}]

def main():
    labels_finder = LabelsFinder()
    # print(len(labels_finder.get_labeled_pods({'product': 'Attenti'})))
    # print(len(labels_finder.get_labeled_pods({'status': 'unhealthy'})))
   

def create_app() -> Flask:
    app = Flask(__name__)

    for label in scan_labels:
        sub_endpoint = ''.join(list(map(lambda x: x[0].upper()+x[1:]  ,[[k,v] for k,v in label.items()][0]))) # {'status': 'unhealthy'} -> StatusUnhealthy 
        app.logger.info(sub_endpoint)
        app.logger.info(label)

        app.register_blueprint(
            create_plods_labels_blueprint(
                blueprint_name=sub_endpoint,
                label_dict=label,
                resource_prefix=sub_endpoint,
                app_context=app,
            ),
            url_prefix='/api'
        )
    
    return app


if __name__ == '__main__':
    # main()
    app = create_app()
    
    app.run(host="127.0.0.1", port=5000, debug=True)






'''
------------------
GET
Active labels scan
/ActiveScanLabels

------------------
GET
Product Attenti
/productAttenti
Modular aproach with blueprints. Create endpoint for each pairs of labels.
Eaxmple  :
Labels Active Search : {'critical': 'true'} , {'environment': 'prod'} , {'environment': 'dev'}
prefix_url = /podsLabel
/podsLabel/CriticalTrue
/podsLabel/EnvironmentProd
/podsLabel/environmentDev
------------------

POST
Add Release Notes
/AddReleaseNotes?name&vertion
Query Params :
- name
- vertion
------------------
GET
Inspect Namespace Release
/Inspect Namespace Release
------------------
'''