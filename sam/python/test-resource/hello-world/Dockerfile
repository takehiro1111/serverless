FROM public.ecr.aws/lambda/nodejs:24@sha256:2ec33a5ea4ce98465794f58422113560498bc0b2bed998afe3100e73a6fb0922

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
