pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    stages {

        stage('Checkout Code') {
            steps {
                git 'https://github.com/dayacode12/testforge-ai.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install fastapi uvicorn pydantic pytest
                '''
            }
        }

        stage('Run App') {
            steps {
                sh '''
                . venv/bin/activate
                nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
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
    }
}
