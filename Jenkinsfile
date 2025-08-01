pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask_hello"
        IMAGE_TAG = "latest"
        TAR_NAME = "flask_hello.tar"
        KUBECONFIG_PATH = "/home/m3/.kube/config"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker image (local)') {
            steps {
                dir('flask_app') {
                    sh '''
                        docker build -t $IMAGE_NAME:$IMAGE_TAG .
                        docker save $IMAGE_NAME:$IMAGE_TAG -o $TAR_NAME
                    '''
                }
            }
        }

        stage('Inject image into Minikube Docker') {
            steps {
                dir('flask_app') {
                    sh '''
                        eval $(minikube docker-env)
                        docker load -i $TAR_NAME
                    '''
                }
            }
        }

        stage('Run Tests inside container') {
            steps {
                dir('flask_app') {
                    sh '''
                        docker run --rm $IMAGE_NAME:$IMAGE_TAG pytest test.py
                    '''
                }
            }
        }

        stage('Clean previous containers') {
            steps {
                sh '''
                    docker ps -q --filter "name=flask_prod" | grep -q . && docker stop flask_prod || true
                    docker ps -a -q --filter "name=flask_prod" | grep -q . && docker rm flask_prod || true
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                dir('flask_app/kubernetes') {
                    sh '''
                        export KUBECONFIG=$KUBECONFIG_PATH
                        kubectl apply -f .
                    '''
                }
            }
        }
    }

    post {
        always {
            sh '''
                export KUBECONFIG=$KUBECONFIG_PATH
                kubectl get pods
            '''
        }
    }
}
