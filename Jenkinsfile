def remote=[:]
remote.name = 'site'
remote.allowAnyHosts = true

pipeline {
    agent any

    environment {
        // Укажите переменные окружения для подключения к удаленному Docker-серверу
        DOCKER_HOST = credentials('remote_host_id') //user and host of remote server, like user@remote-server
        DOCKER__HOST_IP = credentials('host_ip_id') //only ip of remote server
        REMOTE_REPO_PATH = 'simple_django' // /path/to/remote/repo
    }
     
    stages {

        stage ('Check Remote Git Status') {
            steps {
                script{
                    withCredentials([sshUserPrivateKey(credentialsId: 'server-ssh', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'userName')]) {
                        remote.host = env.DOCKER__HOST_IP
                        remote.user = userName
                        remote.identityFile = identity
                        def remoteStatus = sshCommand(remote: remote, command: "cd ${REMOTE_REPO_PATH} && git status -s")
                        // Если есть изменения, выводим их в лог
                        if (remoteStatus) {
                            echo "There are changes in the remote repository: ${remoteStatus}"
                        } else {
                            echo "No changes detected in the remote repository."
                        }
                        // Сохраняем статус в переменную
                        env.CHANGES_DETECTED = remoteStatus ? 'true' : 'false'
                    }
                }
            }
        }

        stage('Check Remote Docker Connection') {
            steps {
                sshagent(['server-ssh']){
                    script {
                        // Используем docker.withServer для подключения к удаленному Docker-серверу
                        docker.withServer('ssh://${env.DOCKER_HOST}', 'server-ssh') {
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
    }
}