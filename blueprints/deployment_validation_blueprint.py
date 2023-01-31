from flask import Blueprint, jsonify, request
from modules.labels_finder import LabelsFinder
import json


labels_finder = LabelsFinder()


def create_validate_deployment_blueprint(blueprint_name: str, app_context) -> Blueprint:
    blueprint = Blueprint(blueprint_name, __name__)

    @blueprint.route('/ValidateDeployment', methods=["POST"])
    def validate_deployment():
        request_param = request.get_json(force=True)
        # app_context.logger.info(f"Requesr payload {request_param}")
        # app_context.logger.info(f"Query Param namespace  : {request.args['namespace']}")
        # app_context.logger.info(f" lablel_key {request.args['lablel_key']}  lablel_value {request.args['lablel_value']}")
        label_dict = {request.args['lablel_key']: request.args['lablel_value']}
        # app_context.logger.info(label_dict)
        pods = labels_finder.get_namespaced_pods(
            request.args['namespace'], label_dict)
        payload_deployment_versions = request_param['helm_services']

        scan_data = {
            'diff_verstions': {},
            'not_in_running_state': {}
        }
        for pod in pods:
            # take care of sudecar issue !!!! -> more then one element inside spec.containers
            extract_pod_name = pod.metadata.name
            extract_microservice_name = pod.metadata.name.split("-")[0]  # userservice-6b88c7875-78sst -> userservice
            extract_microservice_version = pod.spec.containers[0].image.split(":")[1]
            try:
                expected_release_version = payload_deployment_versions[extract_microservice_name]
                if expected_release_version == extract_microservice_version:
                    app_context.logger.info(f'The release {extract_microservice_name} Pod {extract_pod_name} deployed with the correct version : {extract_microservice_version} .')
                else:
                    # app_context.logger.warning(f'The release {extract_microservice_name} Pod {extract_pod_name} expected version : {expected_release_version} differ from what currently deployed version : {extract_microservice_version} .')
                    scan_data['diff_verstions'][extract_pod_name] = {'expected_version': expected_release_version, 'currently_deployed': extract_microservice_version }
                app_context.logger.info(pod.status.phase)
                if pod.status.phase != 'Running':
                        app_context.logger.warning(f'The release {extract_microservice_name} Pod {extract_pod_name} not in running state.')
                        scan_data['not_in_running_state'][extract_pod_name] = {'pod_name': extract_pod_name}
            except KeyError :
                app_context.logger.info(f'The release {extract_microservice_name}  Pod {extract_pod_name}  not requested by payload test.')

        return jsonify(scan_data), 201

    return blueprint