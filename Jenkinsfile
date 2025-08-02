pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-app"
        DOCKER_TAG = "latest"
        DOCKER_REGISTRY = "localhost:5000"
        KUBECONFIG = "${HOME}/.kube/config"
    }

    stages {

        stage('Cleanup Docker') {
            steps {
                sh '''
                    docker container prune -f
                    docker image prune -f
                    docker volume prune -f
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $IMAGE_NAME:$DOCKER_TAG .
                    docker tag $IMAGE_NAME:$DOCKER_TAG $DOCKER_REGISTRY/$IMAGE_NAME:$DOCKER_TAG
                    docker push $DOCKER_REGISTRY/$IMAGE_NAME:$DOCKER_TAG
                '''
            }
        }

        stage('Verify Minikube & Permissions') {
            steps {
                sh '''
                    if ! minikube status | grep -q "Running"; then
                        minikube start --driver=docker
                    fi

                    if [ ! -r "$KUBECONFIG" ]; then
                        echo "Fixing kubeconfig permissions..."
                        sudo chown $USER $KUBECONFIG
                        chmod 600 $KUBECONFIG
                    fi

                    kubectl config use-context minikube
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl delete deployment flask-deploy --ignore-not-found=true
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                '''
            }
        }

        stage('Post-deploy Checks') {
            steps {
                sh '''
                    kubectl rollout status deployment/flask-deploy
                    kubectl get pods
                    kubectl get svc
                '''
            }
        }

    }

    post {
        always {
            echo "✔️ Pipeline terminé. Nettoyage..."
            sh '''
                docker container prune -f
                docker image prune -f
                docker volume prune -f
            '''
        }
        failure {
            echo "❌ Échec du pipeline."
        }
    }
}
