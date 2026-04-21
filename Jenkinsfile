pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'testforge-ai:latest'
        CONTAINER_NAME = 'testforge-test'
        REGISTRY = 'docker.io'
        SHARED_NETWORK = 'shared-network'
        OLLAMA_URL = 'http://ollama:11434/api/generate'
        TESTFORGE_URL = 'http://testforge-test:8000'
    }
    
    options {
        timeout(time: 30, unit: 'MINUTES')
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Checking out code from GitHub..."
                    checkout scm
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${DOCKER_IMAGE}"
                    sh '''
                        docker build -t ${DOCKER_IMAGE} .
                        echo "Docker image built successfully"
                    '''
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    echo "Running test suite..."
                    sh '''
                        docker run --rm \
                            --network ${SHARED_NETWORK} \
                            -v ${WORKSPACE}:/app \
                            ${DOCKER_IMAGE} \
                            python /app/build_script.py > test_output.log 2>&1 || true
                        
                        echo "Test output:"
                        cat test_output.log
                    '''
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    echo "Checking TestForge-AI health..."
                    sh '''
                        sleep 3
                        curl -s http://testforge-test:8000/health -w "\n" || echo "Health check failed"
                    '''
                }
            }
        }
        
        stage('Analyze Errors with Ollama') {
            steps {
                script {
                    echo "Sending test results to Ollama for AI analysis (this may take 5-10 minutes)..."
                    sh '''
                        timeout 600 docker run --rm \
                            --network ${SHARED_NETWORK} \
                            -v ${WORKSPACE}:/app \
                            ${DOCKER_IMAGE} \
                            python /app/full_pipeline.py > pipeline_output.log 2>&1 || true
                        
                        echo "Pipeline output:"
                        cat pipeline_output.log
                    '''
                }
            }
        }
        
        stage('Generate Test Cases') {
            steps {
                script {
                    echo "Generating test cases via TestForge-AI..."
                    sh '''
                        timeout 300 curl -s -X POST ${TESTFORGE_URL}/generate-tests \
                            -H "Content-Type: application/json" \
                            -d '{"feature_description": "User authentication with email validation and MFA support"}' \
                            -w "\n" || echo "TestForge-AI not available"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "Cleaning up workspace..."
                sh '''
                    mkdir -p reports
                    cp -f test_output.log reports/ 2>/dev/null || true
                    cp -f pipeline_output.log reports/ 2>/dev/null || true
                '''
                archiveArtifacts artifacts: 'reports/**/*.log', allowEmptyArchive: true
            }
        }
        
        success {
            echo "Pipeline executed successfully!"
        }
        
        failure {
            echo "Pipeline failed - check logs above"
        }
    }
}
