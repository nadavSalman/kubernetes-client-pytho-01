from kubernetes import client, config

class LabelsFinder():
    def __init__(self) -> None:
        self.config = config.load_kube_config()
        self.v1_api = client.CoreV1Api()


    '''
    Find all pods in all namespaces that match the given dict labels.
    '''
    def get_labeled_pods(self,label_dict):
        pods = self.v1_api.list_pod_for_all_namespaces(watch=False)
        match_labels_pods = []
        for pod in pods.items:
            pod_labels = pod.metadata.labels
            if pod_labels is not None and self.is_subset(label_dict,pod_labels) :
                match_labels_pods.append(pod)
        return match_labels_pods

    '''
    Boolean function for validate of dictA is usb elment of dictB
    '''
    def is_subset(self,dic_a,dic_b):
        return set(dic_a.items()).issubset(dic_b.items())
    
