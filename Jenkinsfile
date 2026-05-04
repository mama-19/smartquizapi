pipeline {
    agent any

    environment {
        IMAGE_NAME   = "smartquizapi"
        COMPOSE_DIR  = "/var/smartquiz_saas_sandbox/smartquizapi"
        POSTGRES_DIR = "/var/smartquiz_saas_sandbox/postgres"
        TRAEFIK_DIR  = "/var/smartquiz_saas_sandbox/traefik"
    }

    triggers {
        githubPush()
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Cloning smartquizapi..."
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building image: ${IMAGE_NAME}:${BUILD_NUMBER}"
                sh """
                    docker build \
                        -t ${IMAGE_NAME}:${BUILD_NUMBER} \
                        -t ${IMAGE_NAME}:latest \
                        .
                """
            }
        }

        stage('Ensure Infrastructure') {
            steps {
                echo "Making sure postgres and traefik are up..."
                sh """
                    cd ${POSTGRES_DIR} && docker-compose up -d
                    cd ${TRAEFIK_DIR}  && docker-compose up -d
                """
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying smartquizapi:${BUILD_NUMBER}..."
                sh """
                    cd ${COMPOSE_DIR}
                    docker-compose down --remove-orphans
                    docker-compose up -d
                """
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 5
                    for i in $(seq 1 10); do
                        STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/health || true)
                        if [ "$STATUS" = "200" ]; then
                            echo "Health check passed!"
                            exit 0
                        fi
                        echo "Attempt $i — status: $STATUS, retrying in 3s..."
                        sleep 3
                    done
                    echo "Health check failed"
                    exit 1
                '''
            }
        }

        stage('Cleanup') {
            steps {
                sh 'docker image prune -f'
                cleanWs()
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful — build #${BUILD_NUMBER}"
        }
        failure {
            echo "❌ Pipeline failed — build #${BUILD_NUMBER}"
        }
    }
}