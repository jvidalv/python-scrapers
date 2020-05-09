pipeline {
  agent { docker { image 'python:3.8.2' } }
  stages {
    stage('build') {
      steps {
        withEnv(["HOME=${env.WORKSPACE}"]) {
            sh 'pip install --user -r requirements.txt'
        }
      }
    }
  }
}