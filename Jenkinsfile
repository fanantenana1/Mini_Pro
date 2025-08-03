pipeline {
    agent any

    environment {
        HOME           = '/var/lib/jenkins'
        MINIKUBE_HOME  = '/var/lib/jenkins/.minikube'
        KUBECONFIG     = '/var/lib/jenkins/.kube/config'
        IMAGE_NAME     = 'flask-hello'
        IMAGE_TAG      = 'latest'
        DOCKER_IMAGE   = "${IMAGE_NAME}:${IMAGE_TAG}"
        DOCKER_HUB     = "haaa012/${IMAGE_NAME}:${IMAGE_TAG}"
        MAVEN_HOME     = '/opt/maven'
        SONARQUBE_ENV  = 'SonarQubeEnv'
        SONAR_TOKEN    = credentials('sonar-token')
    }

    stages {

        stage('📁 Checkout') {
            steps {
                checkout scm
            }
        }

        stage('🧹 Cleanup Docker') {
            steps {
                sh '''
                    docker container prune -f
                    docker image prune -f
                    docker volume prune -f
                '''
            }
        }

        stage('🔍 Analyse SonarQube') {
            steps {
                withSonarQubeEnv(SONARQUBE_ENV) {
                    sh "${MAVEN_HOME}/bin/mvn sonar:sonar -Dsonar.projectKey=salama_java -Dsonar.login=${SONAR_TOKEN}"
                }
            }
        }

        stage('🔨 Build Docker image') {
            steps {
                dir('flask_app') {
                    sh 'docker build -t ${DOCKER_IMAGE} .'
                }
            }
        }

        stage('🧪 Tests unitaires') {
            steps {
                sh 'echo "Tests à insérer ici..."'
                // Exemple : docker run --rm ${DOCKER_IMAGE} pytest
            }
        }

        stage('🧬 Test serveur Flask') {
            steps {
                sh '''
                    docker run -d --name test-server -p 5000:5000 ${DOCKER_IMAGE}
                    sleep 5
                    curl -sI http://localhost:5000 || echo "❌ Serveur KO"
                    docker stop test-server || true
                    docker rm test-server || true
                '''
            }
        }

        stage('🛡️ Verify Minikube Access') {
            steps {
                sh '''
                    ls -ld "$MINIKUBE_HOME"
                    ls -l "$KUBECONFIG"
                    minikube status
                    kubectl version --client
                    kubectl get nodes
                '''
            }
        }

        stage('🚀 Deploy to Kubernetes') {
            when {
                expression { fileExists(env.KUBECONFIG) }
            }
            steps {
                sh '''
                    kubectl apply -f flask_app/kubernetes/deployment.yaml
                    kubectl apply -f flask_app/kubernetes/service.yaml
                '''
            }
        }

        stage('🔎 Post-deploy Checks') {
            steps {
                sh '''
                    kubectl get pods
                    kubectl get services
                '''
            }
        }

        stage('📦 Push vers Docker Hub') {
            steps {
                withDockerRegistry(credentialsId: 'docker-hub-creds', url: '') {
                    sh '''
                        docker tag ${DOCKER_IMAGE} ${DOCKER_HUB}
                        docker push ${DOCKER_HUB}
                    '''
                }
            }
        }

        stage('📤 Déployer vers Nexus') {
            steps {
                sh "${MAVEN_HOME}/bin/mvn deploy -DaltDeploymentRepository=nexus::default::http://localhost:8081/repository/maven-releases/"
            }
        }
    }

    post {
        always {
            echo '🧼 Nettoyage final...'
            sh '''
                docker container prune -f
                docker image prune -f
                docker volume prune -f
            '''
        }

        failure {
            echo '❌ Échec du pipeline.'
        }
    }
}
