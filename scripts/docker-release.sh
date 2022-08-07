#!/usr/bin/env bash
REPOSITORY="${1:-edgerun}"
VERSION="${2:-$(git rev-parse --short HEAD)}"

image=$REPOSITORY/edge-chaos
version=$VERSION

basetag="${image}:${version}"

docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

export DOCKER_BUILD_KIT=1
export DOCKER_CLI_EXPERIMENTAL=enabled


# build container
echo "Build amd64"
docker build -t ${basetag}-amd64 -f ./bin/docker/Dockerfile.amd64 .

echo "Build arm32v7"
docker build -t ${basetag}-arm32v7 -f ./bin/docker/Dockerfile.arm32v7 .

echo "Build arm64v8"
docker build -t ${basetag}-arm64v8 -f ./bin/docker/Dockerfile.arm64v8 .



# push em all
docker push ${basetag}-amd64 &
docker push ${basetag}-arm32v7 &
docker push ${basetag}-arm64v8 &

wait

export DOCKER_CLI_EXPERIMENTAL=enabled

# create the manifest
docker manifest create -a ${basetag} \
  ${basetag}-amd64 \
  ${basetag}-arm32v7 \
  ${basetag}-arm64v8

# explicit annotations
docker manifest annotate ${basetag} ${basetag}-arm64v8 --os "linux" --arch "arm64" --variant "v8"
docker manifest annotate ${basetag} ${basetag}-arm32v7 --os "linux" --arch "arm" --variant "v7"

# ship it
docker manifest push --purge ${basetag}
