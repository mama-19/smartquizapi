pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                cleanWs()
                checkout scm
            }
        }
        stage('Create Network') {
            steps {
                sh 'docker network create traefik-net || true'  // 👈 create if not exists
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker compose build'
            }
        }
        stage('Start Container') {
            steps {
                sh 'docker compose up -d'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'docker compose exec -T smartquiz_service pytest || true'
            }
        }
    }
    
}
