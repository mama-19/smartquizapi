pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {
        stage('GitHub Link Test') {
            steps {
                echo "🚀 Jenkins successfully received the signal from GitHub!"
                echo "Build Number: ${env.BUILD_NUMBER}"
                echo "Branch: ${env.BRANCH_NAME}"
            }
        }
        
        stage('Verify Files') {
            steps {
                echo "Checking if code was actually pulled..."
                sh 'ls -la'
            }
        }
    }

    post {
        success {
            echo "✅ Connection Verified: GitHub is talking to Jenkins."
        }
        always {
            cleanWs()
        }
    }
}