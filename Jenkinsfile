pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        echo 'hello'
        git(url: 'https://github.com/losaret/simple_django', branch: 'main')
      }
    }

    stage('build') {
      steps {
        echo 'this is build'
      }
    }

    stage('deploy') {
      steps {
        echo 'this is deploy'
      }
    }

  }
}