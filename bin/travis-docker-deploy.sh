set -ex

# Manage the image build from Travis CI
# This assumes that the image is initially built with the "build" tag.

# Skip deployments in PRs
if [ $TRAVIS_PULL_REQUEST != "false" ]; then
    exit 0;
fi

# Only build DEPLOY_DOCKER_IMAGE is explicitly set in .travis.yml.
if [ $DEPLOY_DOCKER_IMAGE == "false" ]; then
    echo "Skipping docker build. \$DEPLOY_DOCKER_IMAGE=false";
    exit 0;
fi

docker login -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD"

# Create tag; latest for master; otherwise use branch name
if [ "$TRAVIS_BRANCH" == "master" ]; then
    TAG="latest";

else
    # need to sanitize any "/" from git branches
    TAG=`echo "$TRAVIS_BRANCH" | sed "s/\//-/"`;
fi

# Only deploy the `latest` image
if [ ${TAG} == "latest" ]; then
    # Tag and push the branch-based name
    docker tag ${IMAGE_NAME}:build ${IMAGE_NAME}:${TAG}
    docker push ${IMAGE_NAME}:${TAG}

else
    echo "Skipping docker push (not 'latest')"
fi
