pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "flask_hello:latest"
        KUBECONFIG = "/var/lib/jenkins/.kube/config"
        MINIKUBE_HOME = "/var/lib/jenkins"
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
                    // Charger correctement l'environnement Docker de Minikube
                    def dockerEnv = sh(script: "sudo -u jenkins minikube docker-env --shell bash", returnStdout: true).trim()
                    sh """
                        ${dockerEnv}
                        docker build -t ${DOCKER_IMAGE} ./flask_app
                    """
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
                withEnv(["KUBECONFIG=${env.KUBECONFIG}"]) {
                    sh 'kubectl apply -f flask_app/kubernetes/deployment.yaml'
                    sh 'kubectl apply -f flask_app/kubernetes/service.yaml'
                }
            }
        }
    }

    post {
        always {
            withEnv(["KUBECONFIG=${env.KUBECONFIG}"]) {
                sh 'kubectl get pods'
            }
        }
    }
}
