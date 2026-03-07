FROM public.ecr.aws/lambda/nodejs:20@sha256:5643651ce243fcd5b6209cd5ac348cb2e66a7a9eb8f050c470ad4d19e993c5e4

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
