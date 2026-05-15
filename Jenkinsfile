pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        APP_NAME = "smartquizapi"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Show Workspace') {
            steps {
                echo "📁 Checking project files..."
                sh 'ls -la'
            }
        }

        stage('Stop Old Containers') {
            steps {
                echo "🛑 Stopping old containers..."
                sh 'docker compose down || true'
            }
        }

        stage('Build & Start Containers') {
            steps {
                echo "🐳 Building and starting Docker containers..."
                sh 'docker compose up -d --build'
            }
        }

        stage('Verify Running Containers') {
            steps {
                echo "✅ Checking running containers..."
                sh 'docker ps'
            }
        }
    }

    post {
        success {
            echo "🎉 Deployment successful! App is running."
        }

        failure {
            echo "❌ Deployment failed. Check logs."
            sh 'docker compose logs || true'
        }

        always {
            echo "🧹 Cleaning workspace..."
            cleanWs()
        }
    }
}