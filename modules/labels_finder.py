from kubernetes import client, config


class LabelsFinder():
    def __init__(self) -> None:
        '''
        help(kubernetes.config.incluster_config) 
        load_incluster_config(client_configuration=None, try_refresh_token=True)
            Use the service account kubernetes gives to pods to connect to kubernetes
            cluster. It's intended for clients that expect to be running inside a pod
            running on kubernetes. It will raise an exception if called from a process
            not running in a kubernetes environment.
        '''
        self.config = config.load_kube_config()
        self.v1_api_client = client.CoreV1Api()

    '''
    Find all pods in all namespaces that match the given dict labels.
    '''

    def get_labeled_pods(self, label_dict):
        pods = self.v1_api_client.list_pod_for_all_namespaces(watch=False)
        return self.get_match_lable_pods(pods, label_dict)

    def get_namespaced_pods(self, namespace, label_dict):
        pods = self.v1_api_client.list_namespaced_pod(namespace, watch=False)
        return self.get_match_lable_pods(pods, label_dict)

    def get_match_lable_pods(self, pods, label_dict):
        match_labels_pods = []
        for pod in pods.items:
            pod_labels = pod.metadata.labels
            if pod_labels is not None and self.is_subset(label_dict, pod_labels):
                match_labels_pods.append(pod)
        return match_labels_pods

    '''
    Boolean function for validate of dictA is usb elment of dictB
    '''

    def is_subset(self, dic_a, dic_b):
        return set(dic_a.items()).issubset(dic_b.items())
