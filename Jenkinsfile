pipeline {
    agent any
    
    stages {
        stage('Clone Repository') {
            steps {
                cleanWs() 
                checkout scm
                // Verify code is here
                sh 'ls -la ${WORKSPACE}'
            }
        }

        stage('Deploy / Update Services') {
            steps {
                // Must cd into WORKSPACE so docker-compose finds your code
                sh '''
                    cd ${WORKSPACE}
                    ls -la                          
                    docker compose down
                    docker compose build --no-cache
                    docker compose up -d
                '''
            }
        }

        stage('Verify Container') {
            steps {
                sh '''
                    docker ps | grep smartquiz
                    docker compose logs --tail=50
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    cd ${WORKSPACE}
                    docker compose exec -T smartquiz_service pytest || true
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Deployed successfully!'
        }
        failure {
            sh 'cd ${WORKSPACE} && docker compose logs --tail=100'
            echo '❌ Deployment failed!'
        }
    }
}
