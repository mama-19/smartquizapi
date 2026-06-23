pipeline {
    agent any
    environment {
        IMAGE_NAME = "youmara/smartquiz"
        TAG = "${BUILD_NUMBER}"
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
                sh "docker build -t $IMAGE_NAME:$TAG -t $IMAGE_NAME:latest ."
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
                        docker push $IMAGE_NAME:latest
                        docker logout
                    '''
                }
            }
        }
        stage('Deploy with Docker Compose') {
            steps {
                // pull the image we already built, don't rebuild
                sh 'docker compose up -d'
            }
        }
        stage('Run Tests') {
            steps {
                // fail the build if tests fail
                sh 'docker compose exec -T smartquiz_service pytest'
            }
        }
    }
    post {
        always {
            sh 'docker image prune -f'
        }
        success {
            echo "Build $BUILD_NUMBER deployed successfully"
        }
        failure {
            echo "Build $BUILD_NUMBER failed"
        }
    }
}
