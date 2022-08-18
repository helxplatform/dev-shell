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
            - name: agent
              mountPath: /home/jenkins/agent
          - name: kaniko
            command:
            - /busybox/cat
            image: containers.renci.org/acis/kaniko/executor:no-copy-debug
            imagePullPolicy: Always
            resources:
              requests:
                cpu: 1
                ephemeral-storage: 512M
                memory: 4G
              limits:
                cpu: 1
                ephemeral-storage: 512M
                memory: 4G
            tty: true
            volumeMounts:
            - name: agent
              mountPath: /home/jenkins/agent
            - name: jenkins-cfg
              mountPath: /kaniko/.docker
            - name: kaniko
              mountPath: /kaniko
            - name: workspace
              mountPath: /workspace
          - name: tools
            command:
            - /bin/cat
            image: containers.renci.org/helxplatform/build-tools
            imagePullPolicy: Always
            tty: true
            volumeMounts:
            - name: agent
              mountPath: /home/jenkins/agent
          initContainers:
          - name: init
            env:
              - name: VOLUMES
                value: /workspace-x:/agent-x
              - name: KANIKO_DIR
                value: /kaniko-x
            image: containers.renci.org/helxplatform/build-init:latest
            command: ['/app/setup.py' ]
            volumeMounts:
            - name: agent
              mountPath: /agent-x
            - name: kaniko
              mountPath: /kaniko-x
            - name: workspace
              mountPath: /workspace-x
          volumes:
           - name: agent
             ephemeral:
               volumeClaimTemplate:
                 spec:
                   accessModes: [ "ReadWriteOnce" ]
                   storageClassName: nvme-ephemeral
                   resources:
                     requests:
                       storage: 7G
           - name: jenkins-cfg
             projected:
               sources:
               - secret:
                   name: rencibuild-imagepull-secret
                   items:
                   - key: .dockerconfigjson
                     path: config.json
           - name: kaniko
             ephemeral:
               volumeClaimTemplate:
                 spec:
                   accessModes: [ "ReadWriteOnce" ]
                   storageClassName: nvme-ephemeral
                   resources:
                     requests:
                       storage: 2G
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
        container(name: 'tools', shell: '/bin/sh') {
          sh '''
          echo generate targets
          python /app/kaniko_destination.py --docker_repository=helxplatform/dev-shell --branch_name=$BRANCH_NAME --commit_id=$GIT_COMMIT --path=. > ../destinations.txt
          '''
        }
        container(name: 'kaniko', shell: '/busybox/sh') {
          sh '''
          echo build 
          echo destinations arguments:
          cat ../destinations.txt
          executor `cat ../destinations.txt`
          '''
        }
      }
    }
  }
}
