pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "srishti3718/backend"
        DOCKER_TAG = "latest"
        KUBE_NAMESPACE = "multitier-app"
        DEPLOYMENT_NAME = "backend"
        CONTAINER_NAME = "backend"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/srishti1837/Kubernetes.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% ./backend"
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    bat """
                    echo %PASS% | docker login -u %USER% --password-stdin
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    bat "docker push %DOCKER_IMAGE%:%DOCKER_TAG%"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    bat """
                    kubectl set image deployment/%DEPLOYMENT_NAME% %CONTAINER_NAME%=%DOCKER_IMAGE%:%DOCKER_TAG% -n %KUBE_NAMESPACE%
                    kubectl rollout status deployment/%DEPLOYMENT_NAME% -n %KUBE_NAMESPACE%
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Deployment successful'
        }
        failure {
            echo '❌ Deployment failed'
        }
    }
}
