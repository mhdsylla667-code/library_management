pipeline {
    agent any

    environment {
        COMPOSE_PROJECT = "library_ci_${BUILD_NUMBER}"
        TEST_DB          = "test_library_${BUILD_NUMBER}"
        ODOO_ADDONS_PATH = "/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons"
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
    }

    post {
        always {
            echo "🧹 Nettoyage de l'environnement de test..."
            sh '''
                docker compose -p $COMPOSE_PROJECT down -v || true
            '''
        }
        success {
            echo "🎉 Pipeline CI réussi — le module library_management est prêt à être déployé."
        }
        failure {
            echo "❌ Pipeline CI échoué — vérifiez les logs du stage concerné."
        }
    }
}
