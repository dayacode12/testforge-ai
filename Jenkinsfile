pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'testforge-ai:latest'
        CONTAINER_NAME = 'testforge-test'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh '''
                    docker stop $CONTAINER_NAME || true
                    docker rm $CONTAINER_NAME || true
                '''
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                    docker run -d \
                    --name $CONTAINER_NAME \
                    -p 8001:8000 \
                    $DOCKER_IMAGE
                '''
            }
        }

stage('Health Check') {
    steps {
        sh '''
            echo "Waiting for service..."

            for i in {1..10}; do
                curl -s http://testforge-test:8000/health && exit 0
                echo "Retry $i/10..."
                sleep 2
            done

            echo "Health check failed"
            exit 1
        '''
    }
}

        stage('Run AI Analysis (Optional)') {
            steps {
                sh '''
                    echo "Skipping Ollama network dependency for stability"
                '''
            }
        }

        stage('Generate Test Cases') {
            steps {
                sh '''
                    curl -s -X POST http://localhost:8001/generate-tests \
                    -H "Content-Type: application/json" \
                    -d '{"feature_description":"User login system"}' || true
                '''
            }
        }
    }

    post {
        always {
            echo "Archiving logs"
        }

        success {
            echo "Pipeline SUCCESS 🚀"
        }

         failure {
        sh '''
            echo "==== CONTAINER LOGS ===="
            docker logs testforge-test || true
        '''
    }
    }
}
