stage('Clone Repository') {
    steps {
        cleanWs()
        checkout scm   // ← must come AFTER cleanWs
        sh 'ls -la'
    }
}
