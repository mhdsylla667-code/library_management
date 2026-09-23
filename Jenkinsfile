pipeline {
    agent any

    environment {
        COMPOSE_PROJECT  = "library_ci_${BUILD_NUMBER}"
        TEST_DB          = "test_library_${BUILD_NUMBER}"
        ODOO_ADDONS_PATH = "/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons"
        DOCKER_USER      = 'mhdsylla'
        IMAGE_NAME       = 'library_management'
        IMAGE_TAG        = "${BUILD_NUMBER}"
    }

    stages {

        // ── 1. Récupération du code source ───────────────────────────
        stage('Checkout') {
            steps {
                checkout scm
                echo "✅ Code source récupéré depuis GitHub"
            }
        }

        // ── 2. Analyse statique du code Python (flake8) ──────────────
        stage('Lint') {
            steps {
                sh '''
                    echo "🔍 Analyse statique du module..."
                    if ! command -v flake8 &> /dev/null; then
                        pip3 install --break-system-packages --quiet flake8 || true
                    fi
                    flake8 addons/library_management \
                        --max-line-length=120 \
                        --exclude=__pycache__,*.pyc \
                        --statistics || true
                    echo "✅ Lint terminé"
                '''
            }
        }

        // ── 3. Démarrage de la base de données de test ───────────────
        stage('Start DB') {
            steps {
                sh '''
                    echo "🐘 Démarrage de PostgreSQL..."
                    docker compose -p $COMPOSE_PROJECT up -d db
                    echo "⏳ Attente que Postgres soit prêt (15s)..."
                    sleep 15
                    echo "✅ Base de données prête"
                '''
            }
        }

        // ── 4. Installation du module + tests ────────────────────────
        stage('Install & Test') {
            steps {
                sh '''
                    echo "🚀 Installation et test du module library_management..."
                    docker compose -p $COMPOSE_PROJECT run --rm web \
                        odoo -d $TEST_DB \
                        --addons-path=$ODOO_ADDONS_PATH \
                        -i library_management \
                        --test-tags /library_management \
                        --stop-after-init \
                        --log-level=test
                    echo "✅ Module installé et testé avec succès"
                '''
            }
        }

        // ── 5. Construction de l'image Docker ────────────────────────
        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "🐳 Construction de l'image Docker..."
                    docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG} \
                               ${DOCKER_USER}/${IMAGE_NAME}:latest
                    echo "✅ Image construite : ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                '''
            }
        }

        // ── 6. Publication sur DockerHub ─────────────────────────────
        stage('Push to DockerHub') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER_VAR',
                        passwordVariable: 'DOCKER_PASS_VAR'
                    )]) {
                        sh '''
                            echo "📤 Publication sur DockerHub..."
                            echo $DOCKER_PASS_VAR | docker login -u $DOCKER_USER_VAR --password-stdin
                            docker push ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                            docker push ${DOCKER_USER}/${IMAGE_NAME}:latest
                            echo "✅ Image publiée sur DockerHub"
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo "🧹 Nettoyage de l'environnement de test..."
            sh '''
                docker compose -p $COMPOSE_PROJECT down -v || true
                docker logout || true
            '''
        }
        success {
            echo "🎉 Pipeline CI réussi — image ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG} publiée sur DockerHub."
        }
        failure {
            echo "❌ Pipeline CI échoué — vérifiez les logs du stage concerné."
        }
    }
}
