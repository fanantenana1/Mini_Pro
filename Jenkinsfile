pipeline {
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
                echo '======================'
                echo '📁 Étape 1 : Clonage du code source'
                echo '======================'
                checkout scm
            }
        }

        stage('🔍 Analyse SonarQube Python') {
            steps {
                echo '🔍 Analyse du code Flask avec SonarQube Scanner CLI'
                withSonarQubeEnv('sonar') {
                    dir('flask_app') {
                        sh 'sonar-scanner -Dsonar.login=$SONAR_TOKEN'
                    }
                }
            }
        }
        
        stage('🧹 Docker Cleanup') {
            steps {
                echo '======================'
                echo '🧹 Étape 3 : Nettoyage Docker'
                echo '======================'
                sh '''
                    docker container prune -f
                    docker image prune -f
                    docker volume prune -f
                '''
            }
        }

        stage('🔨 Docker Build') {
            steps {
                echo '======================'
                echo '🔨 Étape 4 : Construction de l’image Docker'
                echo '======================'
                dir('flask_app') {
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('🧪 Tests unitaires') {
            steps {
                echo '======================'
                echo '🧪 Étape 5 : Exécution des tests unitaires'
                echo '======================'
                sh "docker run --rm ${DOCKER_IMAGE} pytest || echo '❌ Tests échoués'"
            }
        }

        stage('🧬 Test serveur Flask') {
            steps {
                echo '======================'
                echo '🧬 Étape 6 : Test du serveur Flask'
                echo '======================'
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
                echo '======================'
                echo '🛡️ Étape 7 : Vérification de Minikube'
                echo '======================'
                sh '''
                    echo "✅ Vérification du fichier KUBECONFIG"
                    test -f "$KUBECONFIG" || exit 1

                    echo "✅ Statut Minikube"
                    minikube status || exit 1

                    echo "✅ Nœuds Kubernetes"
                    kubectl get nodes || exit 1
                '''
            }
        }

        stage('🚀 Deploy to Kubernetes') {
            steps {
                echo '======================'
                echo '🚀 Étape 8 : Déploiement dans le cluster Kubernetes'
                echo '======================'
                sh '''
                    kubectl apply -f flask_app/kubernetes/deployment.yaml
                    kubectl apply -f flask_app/kubernetes/service.yaml
                '''
            }
        }

        stage('📦 Push Docker Hub') {
            steps {
                echo '======================'
                echo '📦 Étape 9 : Push vers Docker Hub'
                echo '======================'
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
                echo '======================'
                echo '📦 Étape 10 : Push vers Nexus'
                echo '======================'
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
                echo '======================'
                echo '🔎 Étape 11 : Vérification du dépôt Nexus'
                echo '======================'
                sh '''
                    curl -s -I ${NEXUS_REPO}/repository/maven-releases/com/example/salama-java/${IMAGE_TAG}/salama-java-${IMAGE_TAG}.jar \
                    || echo "❌ Artefact Nexus introuvable"
                '''
            }
        }

    }

    post {
        always {
            echo '======================'
            echo '🧼 Nettoyage final du pipeline'
            echo '======================'
            sh '''
                docker container prune -f
                docker image prune -f
                docker volume prune -f
            '''
        }
        failure {
            echo '❌ Pipeline échoué. Vérifie les logs pour plus de détails.'
        }
    }
}
