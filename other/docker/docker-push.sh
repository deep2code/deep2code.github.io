#!/bin/sh

# docker tag deep2code:v1 39.100.245.179:5000/deep2code:v1

# docker push 39.100.245.179:5000/deep2code:v1

docker tag deep2code:amd64 39.100.245.179:5000/deep2code:amd64

docker push 39.100.245.179:5000/deep2code:amd64
