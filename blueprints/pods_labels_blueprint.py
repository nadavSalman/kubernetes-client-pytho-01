from flask import Blueprint, jsonify, request
from modules.labels_finder import LabelsFinder
import json
labels_finder = LabelsFinder()

def create_plods_labels_blueprint(blueprint_name: str, label_dict: str, resource_prefix: str,app_context) -> Blueprint:
    blueprint = Blueprint(blueprint_name, __name__)

    @blueprint.route(f'/{resource_prefix}', methods=["GET"])
    def get_pods_match_labels():
        pods = labels_finder.get_labeled_pods({'product': 'Attenti'})
        # app_context.logger.info(dir(l[0].spec.containers))
        # app_context.logger.info(l[0].spec.containers[0].image)
        parsed_pods_data = [
            {
                'name':pod.metadata.name,
                'namespace':pod.metadata.namespace,
                'image':pod.spec.containers[0].image
            }
            for pod in pods
        ]
        app_context.logger.info(parsed_pods_data)
        
        return jsonify(parsed_pods_data), 201

    return blueprint

