pipeline{
    agent{
        kubernetes{
            label "maor"
            idleMinutes 5
            yamlFile "build-pod.yaml"
            defaultContainer "ez-docker-helm-build"

        }
    }
    
    environment{
        GITHUB_CREDS="github"
        DOCKER_IMAGE="maorn132/project1"


    }

    stages{
        stage("chekout cod "){
            steps{
                checkout scm
            }
        }
        stage("build docker image"){

            steps{
                script{
                    dockerImage=docker.build("${DOCKER_IMAGE}:latest","--no-cache .")
                }
            }
        }



    }




}