#!/usr/bin/env python
import os
import time
import subprocess as sp
from prometheus_client import start_http_server, Gauge
#
class Jobs:
    def __init__(self):
        self.projects_path = os.environ.get('JOBS_PATH', '/mnt/flame_archive')
        self.projects_list = [ x for x in os.listdir(self.projects_path)]
        self.projects = self.get_projects()
    def get_project_size(self,project_path):
        cmd = ['/bin/du','-s',project_path]
        runit = sp.Popen(cmd,stdout=sp.PIPE,stderr=sp.PIPE)
        out,err = runit.communicate()
        return out.decode().strip().split('\t')[0]
    def get_projects(self):
        return [Project(name=project,size=self.get_project_size(os.path.join(self.projects_path,project)),path=os.path.join(self.projects_path,project)) for project in self.projects_list]
    def remove_unwanted_labelsets(self,metrics: Gauge):
        metrics_labelsets = [x for x in metrics._metrics.keys()]
        active_labelsets = [(p.path,p.name) for p in self.projects]
        # remove active_labelsets from metrics_labelsets
        for x in active_labelsets:
            if x in metrics_labelsets:
                metrics_labelsets.remove(x)
        # if anything is left in the list, remove them
        if len(metrics_labelsets) > 0:
            print(f"purging old metrics {metrics_labelsets}")
            [projectsizemetric.remove(x[0],x[1]) for x in metrics_labelsets]


class Project:
    def __init__(self,name,size,path):
        self.name = name
        self.size = size
        self.path = path
        self.collect()
    def collect(self):
        try:
            projectsizemetric.labels(self.path,self.name).set(self.size)
        except:
            print(self.__dict__)


projectsizemetric = Gauge('carbon_vfx_projects', 'VFX project directory size',labelnames=['path','projectname'])
start_http_server(int(os.environ.get('EXPORTER_PORT',9100)))
while True:
    jobs = Jobs()
    jobs.remove_unwanted_labelsets(projectsizemetric)
    time.sleep(30)