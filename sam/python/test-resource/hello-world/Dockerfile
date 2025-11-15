FROM public.ecr.aws/lambda/nodejs:20@sha256:b1c2e9719b5a432e23582a82c3986d0dadc41a5b3dd3660dbad6c88c8805c06d

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
