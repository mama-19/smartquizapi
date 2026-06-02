pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                cleanWs()
                checkout scm
                echo '✅ Clone successful!'
                sh 'ls -la'
            }
        }
    }
}
