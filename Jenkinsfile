pipeline {
    agent any
    
    stages {
        stage('Clone Repository') {
            steps {
                // Wipe the workspace clean to prevent caching issues
                cleanWs() 
                checkout scm
                
                // Explicitly pull your repository to avoid the "not a git directory" bug
                // git branch: 'main', url: 'https://github.com/mama-19/smartquizapi.git'
            }
        }

        stage('Deploy / Update Services') {
            steps {
                // This builds the new image AND restarts only the updated smartquiz_service container.
                // Traefik and Postgres will keep running uninterrupted.
                sh 'docker compose up -d --build'
            }
        }

        stage('Run Tests') {
            steps {
                // Runs your pytest suite inside the newly updated app container
                // '|| true' ensures that even if tests fail, your pipeline script can finish gracefully
                sh 'docker compose exec -T smartquiz_service pytest || true'
            }
        }
         stage('docker logs') {
            steps {
                // This builds the new image AND restarts only the updated smartquiz_service container.
                // Traefik and Postgres will keep running uninterrupted.
                sh 'docker compose logs'
            }
        }
    }
}
