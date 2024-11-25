# Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "fastapi-app"
        DOCKER_TAG = "${BUILD_NUMBER}"
        GCP_VM_IP = credentials('gcp-vm-ip')
        GCP_VM_USER = credentials('gcp-vm-user')
        SSH_KEY = credentials('gcp-ssh-key')
        GITHUB_TOKEN = credentials('github-token')
    }
    
    triggers {
        // Poll SCM setiap menit untuk perubahan
        pollSCM('* * * * *')
        // Webhook trigger
        githubPush()
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Clean workspace sebelum checkout
                cleanWs()
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
                    '''
                }
            }
        }
        
        stage('Deploy to GCP VM') {
            steps {
                script {
                    // Update source code di VM
                    sh """
                        ssh -i ${SSH_KEY} -o StrictHostKeyChecking=no ${GCP_VM_USER}@${GCP_VM_IP} '
                            cd /home/${GCP_VM_USER}/fastapi-app && \
                            git pull origin main && \
                            docker-compose -f docker/docker-compose.yml down && \
                            docker-compose -f docker/docker-compose.yml build --no-cache && \
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
                        sleep 30
                        curl -f http://${GCP_VM_IP}:8000/health || exit 1
                    """
                }
            }
        }
    }
    
    post {
        success {
            script {
                // Update GitHub deployment status
                sh """
                    curl -H "Authorization: token ${GITHUB_TOKEN}" \
                        -H "Accept: application/vnd.github.v3+json" \
                        -X POST \
                        -d '{"state": "success", "environment": "production"}' \
                        https://api.github.com/repos/OWNER/REPO/deployments/latest/statuses
                """
            }
        }
        failure {
            script {
                // Update GitHub deployment status
                sh """
                    curl -H "Authorization: token ${GITHUB_TOKEN}" \
                        -H "Accept: application/vnd.github.v3+json" \
                        -X POST \
                        -d '{"state": "failure", "environment": "production"}' \
                        https://api.github.com/repos/OWNER/REPO/deployments/latest/statuses
                """
            }
        }
    }
}