from flask import Flask, url_for, jsonify, request
from kubernetes import client, config
from modules.labels_finder import LabelsFinder
from blueprints.pods_labels_blueprint import create_plods_labels_blueprint
from blueprints.deployment_validation_blueprint import create_validate_deployment_blueprint

api_vertion = "api"
scan_labels = [{'product': 'Attenti'}, {'status': 'unhealthy'}]


def create_app() -> Flask:
    app = Flask(__name__)
    app.logger.info('Loagin labels endpoints :')
    for label in scan_labels:
        sub_endpoint = ''.join(
            list(map(lambda x: x[0].upper()+x[1:], [[k, v] for k, v in label.items()][0])))  # {'status': 'unhealthy'} -> StatusUnhealthy
 
        app.register_blueprint(
            create_plods_labels_blueprint(
                blueprint_name=sub_endpoint,
                label_dict=label,
                resource_prefix=sub_endpoint,
                app_context=app,
            ),
            url_prefix=f'/{api_vertion}'
        )

    app.register_blueprint(
        create_validate_deployment_blueprint(
            blueprint_name='validate_deployment',
            app_context=app
        ),
        url_prefix=f'/{api_vertion}'
    )
    # @app.route('/ValidateDeployment', methods=["POST"])
    # def validate_deployment():
    #     request_param = request.get_json(force=True)

    #     return jsonify(request_param['helm_services']), 201

    return app


if __name__ == '__main__':
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
/ValidateleaseNotes?name&vertion
Query Params :
- name
- vertion
------------------
GET
Inspect Namespace Release
/Inspect Namespace Release
------------------
'''
