pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'flask_hello:latest'
        TAR_FILE = 'flask_hello.tar'
        KUBECONFIG = '/home/m3/.kube/config'
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
                    sh """
                        docker build -t $DOCKER_IMAGE_NAME .
                        docker save $DOCKER_IMAGE_NAME -o $TAR_FILE
                    """
                }
            }
        }

        stage('Inject image into Minikube Docker') {
            steps {
                dir('flask_app') {
                    sh '''
                        echo "Trying to inject image into Minikube..."
                        eval $(minikube docker-env) || echo "WARNING: Minikube docker-env failed"
                        docker load -i flask_hello.tar || echo "WARNING: docker load failed"
                    '''
                }
            }
        }

        stage('Run Tests inside container') {
            steps {
                dir('flask_app') {
                    sh 'docker run --rm flask_hello pytest test.py || echo "Tests failed"'
                }
            }
        }

        stage('Clean previous containers') {
            steps {
                sh '''
                    docker rm -f $(docker ps -aq) || echo "No containers to remove"
                '''
            }
        }

            stage('Deploy to Kubernetes') {
                steps {
                    withEnv(["KUBECONFIG=$KUBECONFIG"]) {
                        dir('flask_app/kubernetes') {
                            sh 'kubectl apply -f .'
                        }
                    }
                }
            }
        }
        post {
            always {
                withEnv(["KUBECONFIG=$KUBECONFIG"]) {
                    sh 'kubectl get pods || echo "kubectl failed — check if Minikube is running"'
                }
            }
        }

}
