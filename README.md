|![](https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Warning.svg/156px-Warning.svg.png) | This project is no longer supported.
|---|---|

# Trivy image validator

Trivy Image Validator automatically detect security issues and block before a Kubernetes pod starts.

This repository contains an admission controller that can be configured as a ValidatingWebhook in a k8s cluster. Kubernetes will send requests to the admission server when a Pod creation is initiated. The admission controller checks the image using trivy.

Inspirated by knqyf263 and his wok on trivy-enforcer.


## :warning: Deprecation and Archive Notice

This chart is Deprecated and do not maintained eny more. Use [trivy-operator](https://github.com/devopstales/trivy-operator) instead.

### Deploy
```yaml
kubectl create ns validation
kubens validation

kubectl apply -f deploy/kubernetes/trivy-image-validator.yaml
kubectl apply -f deploy/kubernetes/vwc.yaml
kubectl apply -f deploy/kubernetes/test-deploy.yaml
```
OR
```
helm repo add devopstales https://devopstales.github.io/helm-charts
helm upgrade --install trivy-image-validator devopstales/trivy-image-validator \
--namespace trivy-image-validator \
--create-namespace
```


### Example Deploy:
You can define policy, by adding annotation to the pod trough the deployment:

```yaml
spec:
  ...
  template:
    metadata:
      annotations:
        trivy.security.devopstales.io/medium: "5"
        trivy.security.devopstales.io/low: "10"
        trivy.security.devopstales.io/critical: "2"
...
```

### Build
```yaml
./gen_certs.sh
./build_image.sh

kubectl create ns validation
kubens validation

kubectl apply -f deploy/kubernetes/trivy-image-validator.yaml
kubectl apply -f deploy/kubernetes/vwc.yaml
kubectl apply -f deploy/kubernetes/test-deploy.yaml
```
