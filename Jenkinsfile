pipeline {
  agent any

  environment {
    DOCKERHUB_REPO = "azmeerasai/flask-mysql-demo"
    IMAGE_TAG = "${env.BUILD_NUMBER}"
    DOCKERHUB_CREDENTIALS = 'dockerhubs-creds'  // ✅ Use the actual Jenkins credential ID you added
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Image') {
      steps {
        script {
          echo "Building Docker image: ${DOCKERHUB_REPO}:${IMAGE_TAG}"
          docker.build("${DOCKERHUB_REPO}:${IMAGE_TAG}")
        }
      }
    }

    stage('Run Tests (smoke)') {
      steps {
        script {
          echo "Running smoke tests..."

          // Remove any existing test container
          bat 'docker rm -f temp_test || exit 0'

          def img = docker.image("${DOCKERHUB_REPO}:${IMAGE_TAG}")
          img.run("-d --name temp_test -p 5000:5000")

          // Wait for container to start
          bat "ping -n 6 127.0.0.1 >nul"

          // Check if the Flask app is responding
          bat 'curl --fail http://localhost:5000/ || (docker logs temp_test && exit 1)'

          // Clean up
          bat 'docker rm -f temp_test || exit 0'
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        script {
          echo "Pushing Docker image to Docker Hub..."

          // ✅ Fix: Add the Docker Hub URL explicitly and correct credentials reference
          docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
            def built = docker.image("${DOCKERHUB_REPO}:${IMAGE_TAG}")
            built.push()
            built.push("latest")
          }
        }
      }
    }
  }

  post {
    always {
      echo "Cleaning up workspace..."
      bat 'docker rm -f temp_test || exit 0'
      cleanWs()
    }
    failure {
      mail to: 'dev-team@example.com',
           subject: "Build failed: ${env.BUILD_URL}",
           body: "Build failed. Please check Jenkins logs for details."
    }
  }
}

