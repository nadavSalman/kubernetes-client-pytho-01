curl --location --request POST 'localhost:5000/api/ValidateDeployment?namespace=prod&lablel_key=product&lablel_value=Attenti' \
--header 'Content-Type: application/json' \
--data-binary '@/Users/nsalman/dev-me/kubernetes-client-pytho-01/input-files/yaml.json'