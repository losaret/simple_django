def remote=[:]
remote.name = 'site'

pipeline {
    agent any

    environment {
        // Укажите переменные окружения для подключения к удаленному Docker-серверу
        DOCKER_HOST = credentials('remote_host_id') //user and host of remote server, like user@remote-server
        DOCKER__HOST_IP = credentials('host_ip_id') //only ip of remote server
        REMOTE_REPO_PATH = 'simple_django' // /path/to/remote/repo
        COMPOSE_FILE = 'compose.prod.yaml'
    }

    parameters {
        choice(
            name: 'BUILD_STRUCTURE',
            choices: ['web','all'],
            description: 'Select which services to rebuild'            
        )
    }
     
    stages {
        stage('Create knownHost file') {
            steps {
                script {
                    sh(script: '''
                        known_hosts_file="/var/jenkins_home/.ssh/known_hosts"
                        if ! grep -q "$DOCKER_HOST_IP" "$known_hosts_file"; then
                        ssh-keyscan -H $DOCKER_HOST_IP >> "$known_hosts_file"
                        fi
                        ''')
                }
            }
        }
        
        stage ('Check Remote Git Status') {
            steps {
                script{
                    withCredentials([sshUserPrivateKey(credentialsId: 'server-ssh', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'userName')]) {
                        remote.host = env.DOCKER__HOST_IP
                        remote.user = userName
                        remote.identityFile = identity
                        remote.knownHosts = "/var/jenkins_home/.ssh/known_hosts"
                        def remoteStatus = sshCommand(remote: remote, command: """
                            cd ${env.REMOTE_REPO_PATH} && \
                            git fetch origin && \
                            git rev-list --count HEAD..@{u}
                        """
                        ).trim()
                        env.GIT_BEHIND = remoteStatus.toInteger() > 0? '1' : '0'
                        echo "GIT_BEHIND = ${env.GIT_BEHIND}"
                        // Если есть изменения, выводим их в лог
                        if (env.GIT_BEHIND == '0' ) {
                            echo "No changes detected in the remote repository."
                        } else {
                            echo "There are changes detected in the remote repository."
                        }
                    }
                }
            }
        }

        stage('Check Remote Docker Connection') {
            steps {
                sshagent(['server-ssh']){
                    script {
                        // Используем docker.withServer для подключения к удаленному Docker-серверу
                        docker.withServer("ssh://${env.DOCKER_HOST}", 'server-ssh') {
                            // Проверяем подключение к удаленному Docker-серверу
                            try {
                                echo 'Connected to Docker server at ${env.DOCKER_HOST}'
                            } catch (Exception e) {
                                error "Failed to connect to the remote Docker server: ${e.message}"
                            }
                            def containers = sh(script: 'docker ps', returnStdout: true).trim()
                            echo "Running containers:\n${containers}"
                        }
                    }
                }
            }
        }

        stage('Pull Changes From Git'){
           when {
                expression { return env.GIT_BEHIND == '1' }
           }
           steps {
                script{
                    withCredentials([sshUserPrivateKey(credentialsId: 'server-ssh', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'userName')]) {
                        remote.host = env.DOCKER__HOST_IP
                        remote.user = userName
                        remote.identityFile = identity
                        remote.knownHosts = "/var/jenkins_home/.ssh/known_hosts"
                        sshCommand(remote: remote, command: "cd ${env.REMOTE_REPO_PATH} && git pull")
                    }
                }
            }
        }

        stage('Rebuild Structure'){
            when {
                expression { return env.GIT_BEHIND == '1' }
           }
           steps {
                script{
                    withCredentials([sshUserPrivateKey(credentialsId: 'server-ssh', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'userName')]) {
                        remote.host = env.DOCKER__HOST_IP
                        remote.user = userName
                        remote.identityFile = identity
                        remote.knownHosts = "/var/jenkins_home/.ssh/known_hosts"
                        if (params.BUILD_STRUCTURE == 'web'){
                            sshCommand(remote:remote, command: """
                            cd ${env.REMOTE_REPO_PATH} && \
                            docker compose -f ${env.COMPOSE_FILE} stop web && \
                            docker compose -f ${env.COMPOSE_FILE} build web && \
                            docker compose -f ${env.COMPOSE_FILE} start web
                            """)
                        }
                        if (params.BUILD_STRUCTURE == 'all'){
                            sshCommand(remote:remote, command: """
                            cd ${env.REMOTE_REPO_PATH} && \
                            docker compose -f ${env.COMPOSE_FILE} down && \
                            docker compose -f ${env.COMPOSE_FILE} up --rebuild
                            """)
                        }
                    }
                }
            }
        }
    }
}