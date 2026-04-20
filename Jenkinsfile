pipeline {
    agent any

    stages {

        stage('Check API Health') {
            steps {
                sh '''
                echo "Checking FastAPI health..."
                curl -s http://test-awesome:8000/health
                '''
            }
        }

        stage('Test TinyLlama via API') {
            steps {
                sh '''
                echo "Testing TinyLlama response..."

                response=$(curl -s http://test-awesome:8000/generate)

                echo "LLM Response:"
                echo $response

                if [[ "$response" != *"response"* ]]; then
                    echo "❌ TinyLlama not responding correctly"
                    exit 1
                fi
                '''
            }
        }
    }

    post {
        success {
            echo '✅ AI pipeline working perfectly'
        }
        failure {
            echo '❌ Something broke — investigate logs'
        }
    }
}
