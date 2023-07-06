# jobs-exporter

the dockerfile here will build a container that runs the python script inside this repo.

the kubernetes yaml here will stand up a usable deployment of the exporter with service monitoring included. ** this requires the regcred SPC to be created otherwise iamgePullSecrets wont resolve **

start dev service with `skaffold dev --port-forward`

helm chart in the `helm` folder, deployed with fluxcd