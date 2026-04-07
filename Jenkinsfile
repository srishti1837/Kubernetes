pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "your-dockerhub-username/backend"
        DOCKER_TAG = "latest"
        KUBE_NAMESPACE = "multitier-app"
        DEPLOYMENT_NAME = "backend"
        CONTAINER_NAME = "backend"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/your-username/your-repo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $DOCKER_IMAGE:$DOCKER_TAG ."
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                        sh """
                        echo $PASS | docker login -u $USER --password-stdin
                        """
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh "docker push $DOCKER_IMAGE:$DOCKER_TAG"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh """
                    kubectl set image deployment/$DEPLOYMENT_NAME \
                    $CONTAINER_NAME=$DOCKER_IMAGE:$DOCKER_TAG \
                    -n $KUBE_NAMESPACE

                    kubectl rollout status deployment/$DEPLOYMENT_NAME -n $KUBE_NAMESPACE
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
