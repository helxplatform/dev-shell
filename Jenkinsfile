pipeline {
  agent {
    kubernetes {
      label  'kaniko-agent'
      yaml '''
        apiVersion: v1
        kind: Pod
        metadata:
          name: kaniko-agent
        spec:
          containers:
          - name: jnlp
            volumeMounts:
            - name: workspace
              mountPath: /home/jenkins/agent
          - name: kaniko
            command:
            - /busybox/cat
            image: gcr.io/kaniko-project/executor:debug
            imagePullPolicy: Always
            resources:
              requests:
                cpu: 1
                ephemeral-storage: "1G"
                memory: 4G
              limits:
                cpu: 1
                ephemeral-storage: "10G"
                memory: 16G
            tty: true
            volumeMounts:
            - name: jenkins-cfg
              mountPath: /kaniko/.docker
            - name: workspace
              mountPath: /home/jenkins/agent
          - name: tools
            command:
            - /bin/cat
            image: wateim/jenkins-tools:latest
            imagePullPolicy: Always
            tty: true
            volumeMounts:
            - name: workspace
              mountPath: /home/jenkins/agent
          initContainers:
          - name: init
            image: busybox:1.28
            command: ['chmod', '777', '/workspace']
            volumeMounts:
            - name: workspace
              mountPath: /workspace
          volumes:
           - name: jenkins-cfg
             projected:
               sources:
               - secret:
                   name: rencibuild-imagepull-secret
                   items:
                   - key: .dockerconfigjson
                     path: config.json
           - name: workspace
             ephemeral:
               volumeClaimTemplate:
                 spec:
                   accessModes: [ "ReadWriteOnce" ]
                   storageClassName: nvme-ephemeral
                   resources:
                     requests:
                       storage: 7G
      '''
    }
  }
  stages {
    stage('Build-Push') {
      environment {
        PATH = "/busybox:/kaniko:$PATH"
        DOCKERHUB_CREDS = credentials("${env.REGISTRY_CREDS_ID_STR}")
        DOCKER_REGISTRY = "${env.DOCKER_REGISTRY}"
      }
      steps {
        container(name: 'kaniko', shell: '/busybox/sh') {
          sh '''
          echo build
          cd apps/imagej
          /kaniko/executor --context . --destination helxplatform/dev-shell:$BRANCH_NAME
          '''
        }
      }
    }
  }
}
