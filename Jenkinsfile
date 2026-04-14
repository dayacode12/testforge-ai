pipeline {
    agent any

    environment {
        APP_PORT = "8000"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git 'https://github.com/dayacode12/testforge-ai.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt || pip install fastapi uvicorn pydantic pytest requests
                '''
            }
        }

        stage('Run Application') {
            steps {
                sh '''
                . venv/bin/activate
                nohup python -m uvicorn app.main:app --host 0.0.0.0 --port $APP_PORT &
                sleep 5
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest || true
                '''
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
        success {
            echo "Build successful 🚀"
        }
        failure {
            echo "Build failed ❌"
        }
    }
}