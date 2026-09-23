pipeline {
    agent any

    tools {
        maven 'maven'
        dockerTool 'docker'
    }

    environment {
        DOCKER_USER = 'mhdsylla'
        IMAGE_NAME  = 'library_management'
        IMAGE_TAG   = 'latest'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Maven') {
            steps {
                sh 'mvn clean install'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t \({DOCKER_USER}/\){IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push Docker Image to DockerHub') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER_VAR',
                        passwordVariable: 'DOCKER_PASS_VAR'
                    )]) {
                        sh "echo \$DOCKER_PASS_VAR | docker login -u \$DOCKER_USER_VAR --password-stdin"
                        sh "docker push \({DOCKER_USER}/\){IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }
        success {
            echo 'Image publiée avec succès sur DockerHub !'
        }
        failure {
            echo 'Échec de la publication de l\'image Docker.'
        }
    }
}