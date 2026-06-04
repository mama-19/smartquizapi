pipeline {
    agent any

    environment {
        IMAGE_NAME = "youmara/smartquiz"
        TAG = "v1"
    }

    stages {

        stage('Clone Repository') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t $IMAGE_NAME:$TAG ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push $IMAGE_NAME:$TAG
                    '''
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh 'docker compose up -d --build'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker compose exec -T smartquiz_service pytest || true'
            }
        }

        stage('Logs') {
            steps {
                sh 'docker compose logs'
            }
        }
    }
}
