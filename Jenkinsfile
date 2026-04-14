pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git 'https://github.com/dayacode12/testforge-ai.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t testforge-ai .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh '''
                docker rm -f testforge-container || true
                docker run -d -p 8000:8000 --name testforge-container testforge-ai
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline execution completed."
        }
    }
}
