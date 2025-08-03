pipeline {
    agent any

    environment {
        HOME           = '/var/lib/jenkins'
        MINIKUBE_HOME  = '/var/lib/jenkins/.minikube'
        KUBECONFIG     = '/var/lib/jenkins/.kube/config'
        IMAGE_NAME     = 'flask-hello'
        IMAGE_TAG      = 'latest'
        DOCKER_IMAGE   = "${IMAGE_pipeline {
    agent any

    environment {
        HOME           = '/var/lib/jenkins'
        MINIKUBE_HOME  = '/var/lib/jenkins/.minikube'
        KUBECONFIG     = '/var/lib/jenkins/.kube/config'
        IMAGE_NAME     = 'flask-hello'
        IMAGE_TAG      = "v${BUILD_ID}"
        DOCKER_IMAGE   = "${IMAGE_NAME}:${IMAGE_TAG}"
        DOCKER_HUB     = "haaa012/${DOCKER_IMAGE}"
        SONARQUBE_ENV  = 'sonar'
        SONAR_TOKEN    = credentials('sonar-token')
        MAVEN_HOME     = tool name: 'maven', type: 'maven'
        NEXUS_REPO     = 'http://localhost:8082'
        NEXUS_CREDS    = 'nexus-creds'
    }

    stages {

        stage('📁 Checkout') {
            steps {
                checkout scm
            }
        }

        stage('🔍 Analyse SonarQube') {
            steps {
                withSonarQubeEnv(SONARQUBE_ENV) {
                    sh "${MAVEN_HOME}/bin/mvn sonar:sonar -Dsonar.projectKey=salama_java -Dsonar.login=${SONAR_TOKEN}"
                }
            }
        }

        stage('🧹 Docker Cleanup') {
            steps {
                sh '''
                    docker container prune -f
                    docker image prune -f
                    docker volume prune -f
                '''
            }
        }

        stage('🔨 Docker Build') {
            steps {
                dir('flask_app') {
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('🧪 Tests unitaires') {
            steps {
                sh "docker run --rm ${DOCKER_IMAGE} pytest || echo '❌ Tests échoués'"
            }
        }

        stage('🧬 Test serveur Flask') {
            steps {
                sh '''
                    docker run -d --name test-server -p 5000:5000 ${DOCKER_IMAGE}
                    sleep 5
                    curl -s http://localhost:5000 || echo "❌ Serveur Flask inaccessible"
                    docker stop test-server || true
                    docker rm test-server || true
                '''
            }
        }

        stage('🛡️ Minikube Check') {
            steps {
                sh '''
                    test -f "$KUBECONFIG" || exit 1
                    minikube status || exit 1
                    kubectl get nodes || exit 1
                '''
            }
        }

        stage('🚀 Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f flask_app/kubernetes/deployment.yaml
                    kubectl apply -f flask_app/kubernetes/service.yaml
                '''
            }
        }

        stage('📦 Push Docker Hub') {
            steps {
                withDockerRegistry(credentialsId: 'docker-hub-creds', url: '') {
                    sh '''
                        docker tag ${DOCKER_IMAGE} ${DOCKER_HUB}
                        docker push ${DOCKER_HUB}
                    '''
                }
            }
        }

        stage('📦 Push vers Nexus') {
            steps {
                script {
                    docker.withRegistry(NEXUS_REPO, NEXUS_CREDS) {
                        def appImage = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                        appImage.push("${IMAGE_TAG}")
                    }
                }
            }
        }

        stage('🔎 Nexus Check') {
            steps {
                sh '''
                    curl -s -I ${NEXUS_REPO}/repository/maven-releases/com/example/salama-java/${IMAGE_TAG}/salama-java-${IMAGE_TAG}.jar || echo "❌ Artefact Nexus manquant"
                '''
            }
        }

    }

    post {
        always {
            echo '✅ Pipeline terminé — nettoyage...'
            sh '''
                docker container prune -f
                docker image prune -f
                docker volume prune -f
            '''
        }
        failure {
            echo '❌ Pipeline échoué. Vérifie les logs.'
        }
    }
}
NAME}:${IMAGE_TAG}"
        DOCKER_HUB     = "haaa012/${IMAGE_NAME}:${IMAGE_TAG}"
        SONARQUBE_ENV = 'sonar'                           // Nom du serveur Sonar dans Jenkins
        SONAR_TOKEN = credentials('sonar-token')          // Token Sonar (stocké dans Jenkins Credentials)
        MAVEN_HOME = tool name: 'maven', type: 'maven'    // Nom de Maven configuré dans Jenkins        
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

        stage('Push to Nexus') {
            steps {
                script {
                    docker.withRegistry('http://localhost:8082', 'nexus-creds') {
                        def appImage = docker.build("flask_app:1.0")
                        appImage.push("1.0")
                    }
                }
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
