pipeline {
    agent any

    environment {
        IMAGE_NAME = "testforge-ai"
        CONTAINER_NAME = "testforge-container"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:latest .'
            }
        }

        stage('Stop Existing Container') {
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
                docker run -d --name $CONTAINER_NAME \
                --network shared-network \
                -p 8002:8000 \
                $IMAGE_NAME:latest
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                sleep 5
                curl http://$CONTAINER_NAME:8000/health
                '''
            }
        }

        stage('Test TinyLlama') {
            steps {
                sh '''
                response=$(curl -s http://$CONTAINER_NAME:8000/generate)
                echo $response

                if [[ "$response" != *"response"* ]]; then
                  echo "LLM response failed"
                  exit 1
                fi
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline passed - AI system working'
        }
        failure {
            echo '❌ Pipeline failed - check logs'
            sh 'docker logs $CONTAINER_NAME || true'
        }
    }
}
