pipeline{
    agent{
        kubernetes{
            label "maor"
            idleMinutes 5
            yamlFile "build-pod.yaml"
            defaultContainer "ez-docker-helm-build"

        }
    }
    /////////try 1 to marge
    
    environment{
        GITHUB_CREDS="gitHub"
        DOCKER_IMAGE="maorn132/project1"
        GITHUB_API_URL="https://api.github.com"
        GITHUB_REPO="maornaim/project1"
        GITHUB_TOKEN=credentials("gitHub")

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
        stage("push docker image"){
            when{
                branch "main" 
            }
            steps{
                script{
                    docker.withRegistry("https://registry.hub.docker.com","docker-creds"){
                        dockerImage.push("latest")
                    }
                }
            }

        }
        stage("creat merge request"){
            when {
                not {
                    branch "main"
                }
            }
            steps{
                withCredentials([string(credentialsId: 'gitHub', variable: 'GITHUB_TOKEN')]) {
                    script {
                        def branchName = env.BRANCH_NAME
                        def pullRequestTitle = "Merge ${branchName} into main"
                        def pullRequestBody = "Automatically generated merge request for branch ${branchName}"

                        sh """
                            curl -X POST -H "Authorization: token ${GITHUB_TOKEN}" \
                            -d '{ "title": "${pullRequestTitle}", "body": "${pullRequestBody}", "head": "${branchName}", "base": "main" }' \
                            ${GITHUB_API_URL}/repos/${GITHUB_REPO}/pulls
                        """
                    }
                }
                
            }
        }



    }




}