pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "fastapi-app"
        DOCKER_TAG = "${BUILD_NUMBER}"
        GCP_VM_IP = credentials('gcp-vm-ip')
        GCP_VM_USER = credentials('gcp-vm-user')
        SSH_KEY = credentials('gcp-ssh-key')
        DB_PASSWORD = credentials('db-password')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip install pytest
                    pytest tests/
                '''
            }
        }
        
        stage('Build and Push Docker Images') {
            steps {
                script {
                    sh '''
                        docker-compose -f docker/docker-compose.yml build
                        # If using private registry, add docker push commands here
                    '''
                }
            }
        }
        
        stage('Deploy to GCP VM') {
            steps {
                script {
                    // Create deployment directory
                    sh """
                        ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${GCP_VM_USER}@${GCP_VM_IP} '
                            mkdir -p ~/fastapi-app/docker
                        '
                    """
                    
                    // Copy necessary files
                    sh """
                        scp -i ${SSH_KEY} -o StrictHostKeyChecking=no \
                            docker/docker-compose.yml \
                            docker/Dockerfile \
                            ${GCP_VM_USER}@${GCP_VM_IP}:/home/${GCP_VM_USER}/fastapi-app/docker/
                            
                        scp -i ${SSH_KEY} -o StrictHostKeyChecking=no \
                            -r app \
                            main.py \
                            requirements.txt \
                            .env \
                            ${GCP_VM_USER}@${GCP_VM_IP}:/home/${GCP_VM_USER}/fastapi-app/
                    """
                    
                    // Deploy using docker-compose
                    sh """
                        ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${GCP_VM_USER}@${GCP_VM_IP} '
                            cd /home/${GCP_VM_USER}/fastapi-app && \
                            docker-compose -f docker/docker-compose.yml down && \
                            docker-compose -f docker/docker-compose.yml up -d
                        '
                    """
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    sh """
                        # Wait for services to be ready
                        sleep 30
                        # Check web service
                        curl -f http://${GCP_VM_IP}:8000/health || exit 1
                    """
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
            sh 'docker system prune -f'
        }
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed!'
            // Add notification steps here (email, Slack, etc.)
        }
    }
}
