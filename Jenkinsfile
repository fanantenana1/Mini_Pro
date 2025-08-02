pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "flask_hello:latest"
        DOCKERHUB_USER = "ton_dockerhub"
        KUBECONFIG = '/home/m3/.kube/config'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Image in Minikube') {
            steps {
                script {
                    withEnv(["DOCKER_TLS_VERIFY=", "DOCKER_HOST=",
                             "DOCKER_CERT_PATH=", "MINIKUBE_ACTIVE_DOCKERD=minikube"]) {
                        sh 'eval $(minikube docker-env) && docker build -t $DOCKER_IMAGE ./flask_app'
                    }
                }
            }
        }

        stage('Test Container') {
            steps {
                sh 'docker run --rm -v $PWD/flask_app:/app -w /app $DOCKER_IMAGE pytest test.py'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withEnv(["KUBECONFIG=$KUBECONFIG"]) {
                    sh 'kubectl apply -f flask_app/kubernetes/deployment.yaml'
                    sh 'kubectl apply -f flask_app/kubernetes/service.yaml'
                }
            }
        }
    }

    post {
        always {
            withEnv(["KUBECONFIG=$KUBECONFIG"]) {
                sh 'kubectl get pods'
            }
        }
    }
}
