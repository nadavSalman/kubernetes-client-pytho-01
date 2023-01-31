from flask import Blueprint, jsonify, request
from modules.labels_finder import LabelsFinder
import json

labels_finder = LabelsFinder()


def create_plods_labels_blueprint(blueprint_name: str, label_dict: str, resource_prefix: str, app_context) -> Blueprint:
    blueprint = Blueprint(blueprint_name, __name__)

    @blueprint.route(f'/{resource_prefix}', methods=["GET"])
    def get_pods_match_labels():
        request_param = request.get_json(force=True)
        request_param_namespace = request_param['namespace']
        pods = labels_finder.get_namespaced_pods(request_param_namespace,label_dict)
        # pods = labels_finder.get_labeled_pods(label_dict)

        app_context.logger.info(
            f"{len(pods)} POD's with match lable {label_dict}  found in .")
        parsed_pods_data = [
            {
                'name': pod.metadata.name,
                'namespace': pod.metadata.namespace,
                'image': pod.spec.containers[0].image
            }
            for pod in pods
        ]

        return jsonify(parsed_pods_data), 201

    return blueprint
