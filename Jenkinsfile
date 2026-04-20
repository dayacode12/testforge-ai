pipeline {
    agent any

    environment {
        IMAGE_NAME = "testforge-ai"
        CONTAINER_NAME = "testforge-container"
    }

    stages {

        stage('Build Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:latest .'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true

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
                curl -s http://$CONTAINER_NAME:8000/health
                '''
            }
        }

        stage('Test TinyLlama') {
            steps {
                sh '''
                response=$(curl -s http://$CONTAINER_NAME:8000/generate)

                echo "LLM Response:"
                echo $response

                echo $response | grep -q "response"

                if [ $? -ne 0 ]; then
                  echo "❌ TinyLlama failed"
                  exit 1
                fi
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Full AI pipeline working'
        }
        failure {
            echo '❌ Pipeline failed'
            sh 'docker logs $CONTAINER_NAME || true'
        }
    }
}
