pipeline {
    agent any

    stages {

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t testforge-ai:latest .
                '''
            }
        }

        stage('Stop Existing Container') {
            steps {
                sh '''
                docker rm -f testforge-container || true
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker run -d \
                --name testforge-container \
                -p 8000:8000 \
                testforge-ai:latest
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                sleep 5
                curl -f http://localhost:8000/docs || exit 1
                '''
            }
        }
    }

    post {
        success {
            echo "✅ TestForge AI pipeline deployed successfully"
        }

        failure {
            echo "❌ Pipeline failed - check logs"
            sh 'docker logs testforge-container || true'
        }
    }
}